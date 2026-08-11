import time
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.modules.scrapers.base import BaseScraper
from app.modules.scrapers.schemas import GovernmentJob
from app.modules.scrapers.registry import ScraperPluginRegistry
from app.modules.scrapers.retry import execute_with_retry
from app.modules.scrapers.health import ScraperHealthMonitor
from app.db.repositories import (
    JobRepository,
    JobSourceRepository,
    ScraperHealthRepository,
    DiscoveryLogRepository
)
from app.utils.helpers import generate_content_hash
from app.core.logging import logger


class JobDiscoveryEngine:
    """
    Core Government Job Monitoring & Discovery Engine.
    Executes plugins, dedups via content hashes, tracks updates/withdrawals, records telemetry and discovery logs.
    """

    def __init__(self, db: Session):
        self.db = db
        self.job_repo = JobRepository(db)
        self.source_repo = JobSourceRepository(db)
        self.log_repo = DiscoveryLogRepository(db)

    async def initialize_sources_in_db(self) -> None:
        """Syncs all registered plugin metadata into job_sources database table."""
        plugins = ScraperPluginRegistry.get_all_plugins()
        for p in plugins:
            existing = self.source_repo.get_by_code(p.source_code)
            if not existing:
                self.source_repo.create({
                    "code": p.source_code,
                    "name": p.source_name,
                    "base_url": p.base_url,
                    "category": p.category,
                    "is_enabled": p.is_enabled,
                    "priority": p.priority,
                    "schedule_interval_minutes": p.schedule_interval_minutes
                })
            else:
                self.source_repo.update(existing.id, {
                    "is_enabled": p.is_enabled,
                    "priority": p.priority,
                    "schedule_interval_minutes": p.schedule_interval_minutes
                })

    async def run_scraper(self, plugin: BaseScraper) -> Dict[str, Any]:
        """Runs single scraper plugin with lifecycle hooks, exponential backoff, deduping, and persistence."""
        source_code = plugin.source_code
        logger.info(f"[{source_code}] Starting Job Discovery Run...")
        start_time = time.time()
        
        try:
            # 1. Initialize plugin
            await plugin.initialize()
            
            # 2. Health Check
            is_healthy = await plugin.health_check()
            if not is_healthy:
                raise Exception(f"Health check failed for portal: {plugin.base_url}")

            # 3. Fetch jobs with retry engine
            raw_listings = await execute_with_retry(
                func=plugin.fetch_jobs,
                max_retries=3,
                initial_delay=1.0,
                source_code=source_code
            )

            discovered_new = 0
            updated_jobs = 0
            duplicates_skipped = 0

            for raw_item in raw_listings:
                # 4. Fetch details
                raw_data = await plugin.fetch_notifications(raw_item)
                
                # 5. Normalize
                job_schema: GovernmentJob = plugin.normalize(raw_data)
                
                # 6. Validate
                if not plugin.validate(job_schema):
                    logger.warning(f"[{source_code}] Skipping invalid job payload: {job_schema.title}")
                    continue

                # 7. Deduplication & Hash Computation
                c_hash = generate_content_hash(job_schema.organization, job_schema.advt_number, job_schema.title)
                
                existing_job = self.job_repo.get_by_content_hash(c_hash)
                existing_by_advt = self.job_repo.get_by_advt_and_source(source_code, job_schema.advt_number)

                if not existing_job and not existing_by_advt:
                    # New Discovery
                    db_job = self.job_repo.create({
                        "source_code": source_code,
                        "title": job_schema.title,
                        "department": job_schema.department,
                        "organization": job_schema.organization,
                        "advt_number": job_schema.advt_number,
                        "notification_url": job_schema.notification_url,
                        "apply_url": job_schema.apply_url,
                        "pdf_url": job_schema.pdf_url,
                        "published_date": job_schema.published_date,
                        "last_date": job_schema.last_date,
                        "raw_html": job_schema.raw_html,
                        "status": "ACTIVE",
                        "content_hash": c_hash,
                        "vacancies": job_schema.vacancies,
                        "pay_scale": job_schema.pay_scale
                    })
                    
                    self.log_repo.create({
                        "source_code": source_code,
                        "action": "DISCOVERED_NEW",
                        "advt_number": job_schema.advt_number,
                        "job_title": job_schema.title,
                        "content_hash": c_hash,
                        "details": {"job_id": db_job.id, "last_date": str(job_schema.last_date)}
                    })
                    discovered_new += 1
                elif existing_by_advt and existing_by_advt.content_hash != c_hash:
                    # Updated Notification
                    self.job_repo.update(existing_by_advt.id, {
                        "title": job_schema.title,
                        "last_date": job_schema.last_date,
                        "content_hash": c_hash,
                        "status": "UPDATED"
                    })
                    
                    self.log_repo.create({
                        "source_code": source_code,
                        "action": "UPDATED_NOTIFICATION",
                        "advt_number": job_schema.advt_number,
                        "job_title": job_schema.title,
                        "content_hash": c_hash,
                        "details": {"job_id": existing_by_advt.id, "new_title": job_schema.title}
                    })
                    updated_jobs += 1
                else:
                    # Duplicate
                    self.log_repo.create({
                        "source_code": source_code,
                        "action": "DUPLICATE_SKIPPED",
                        "advt_number": job_schema.advt_number,
                        "job_title": job_schema.title,
                        "content_hash": c_hash,
                        "details": {"reason": "Content hash matched existing record"}
                    })
                    duplicates_skipped += 1

                # Custom Plugin Save lifecycle hook
                await plugin.save(job_schema)

            elapsed_ms = (time.time() - start_time) * 1000
            total_found = len(raw_listings)
            
            # Record Health Telemetry
            ScraperHealthMonitor.record_success(
                db=self.db,
                source_code=source_code,
                response_time_ms=elapsed_ms,
                jobs_found=total_found
            )
            
            return {
                "source_code": source_code,
                "status": "SUCCESS",
                "elapsed_ms": round(elapsed_ms, 2),
                "total_found": total_found,
                "discovered_new": discovered_new,
                "updated_jobs": updated_jobs,
                "duplicates_skipped": duplicates_skipped
            }

        except Exception as e:
            elapsed_ms = (time.time() - start_time) * 1000
            error_msg = str(e)
            ScraperHealthMonitor.record_failure(self.db, source_code, error_msg)
            return {
                "source_code": source_code,
                "status": "FAILED",
                "elapsed_ms": round(elapsed_ms, 2),
                "error": error_msg
            }
        finally:
            await plugin.shutdown()

    async def run_all_active_scrapers(self) -> List[Dict[str, Any]]:
        """Runs all enabled scraper plugins in order of priority."""
        await self.initialize_sources_in_db()
        enabled_plugins = ScraperPluginRegistry.get_enabled_plugins()
        results = []
        for plugin in enabled_plugins:
            res = await self.run_scraper(plugin)
            results.append(res)
        return results
