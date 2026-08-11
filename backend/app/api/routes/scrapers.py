from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.api.schemas.common import APIResponse
from app.modules.scrapers.registry import ScraperPluginRegistry
from app.modules.scrapers.engine import JobDiscoveryEngine
from app.db.repositories import ScraperHealthRepository, DiscoveryLogRepository, JobSourceRepository

router = APIRouter(prefix="/scrapers", tags=["Job Source Engine & Plugins"])


@router.get("/plugins", response_model=APIResponse[List[dict]])
def list_plugins():
    """Lists all registered scraper plugins with metadata, status, priority, and schedules."""
    ScraperPluginRegistry.discover_plugins()
    plugins = ScraperPluginRegistry.get_all_plugins()
    payload = [
        {
            "source_code": p.source_code,
            "source_name": p.source_name,
            "base_url": p.base_url,
            "category": p.category,
            "priority": p.priority,
            "schedule_interval_minutes": p.schedule_interval_minutes,
            "is_enabled": p.is_enabled
        }
        for p in plugins
    ]
    return APIResponse(data=payload, message="Scraper plugins retrieved successfully")


@router.post("/run", response_model=APIResponse[List[dict]])
async def run_scrapers(
    source_code: Optional[str] = Query(None, description="Specific source code to run e.g. SSC, UPSC, NCS"),
    db: Session = Depends(get_db)
):
    """Triggers job discovery engine run across plugins."""
    ScraperPluginRegistry.discover_plugins()
    engine = JobDiscoveryEngine(db)
    
    if source_code:
        plugin = ScraperPluginRegistry.get_plugin(source_code)
        if not plugin:
            raise HTTPException(status_code=404, detail=f"Plugin '{source_code}' not found.")
        res = await engine.run_scraper(plugin)
        results = [res]
    else:
        results = await engine.run_all_active_scrapers()

    return APIResponse(data=results, message="Job discovery execution completed")


@router.get("/health", response_model=APIResponse[List[dict]])
def get_scrapers_health(db: Session = Depends(get_db)):
    """Retrieves health monitor telemetry, average response times, and failure counts."""
    repo = ScraperHealthRepository(db)
    health_records = repo.get_all()
    payload = [
        {
            "source_code": h.source_code,
            "status": h.status,
            "last_success_at": h.last_success_at,
            "last_failure_at": h.last_failure_at,
            "failure_count": h.failure_count,
            "consecutive_failures": h.consecutive_failures,
            "avg_response_time_ms": h.avg_response_time_ms,
            "total_jobs_found": h.total_jobs_found,
            "last_run_jobs_found": h.last_run_jobs_found,
            "last_error_message": h.last_error_message
        }
        for h in health_records
    ]
    return APIResponse(data=payload, message="Scraper health telemetry retrieved")


@router.post("/{source_code}/enable", response_model=APIResponse[dict])
def toggle_scraper(source_code: str, enabled: bool = Query(...), db: Session = Depends(get_db)):
    """Enables or disables a specific scraper plugin."""
    success = ScraperPluginRegistry.set_plugin_enabled(source_code, enabled)
    if not success:
        raise HTTPException(status_code=404, detail=f"Plugin '{source_code}' not found.")
    
    # Sync with DB
    repo = JobSourceRepository(db)
    source = repo.get_by_code(source_code.upper())
    if source:
        repo.update(source.id, {"is_enabled": enabled})

    return APIResponse(
        data={"source_code": source_code.upper(), "is_enabled": enabled},
        message=f"Scraper '{source_code}' state updated to enabled={enabled}"
    )


@router.post("/{source_code}/priority", response_model=APIResponse[dict])
def set_priority(source_code: str, priority: int = Query(..., ge=1), db: Session = Depends(get_db)):
    """Sets priority ranking for a specific scraper plugin."""
    success = ScraperPluginRegistry.set_plugin_priority(source_code, priority)
    if not success:
        raise HTTPException(status_code=404, detail=f"Plugin '{source_code}' not found.")

    repo = JobSourceRepository(db)
    source = repo.get_by_code(source_code.upper())
    if source:
        repo.update(source.id, {"priority": priority})

    return APIResponse(
        data={"source_code": source_code.upper(), "priority": priority},
        message=f"Scraper '{source_code}' priority set to {priority}"
    )


@router.get("/logs", response_model=APIResponse[List[dict]])
def get_discovery_logs(limit: int = 50, db: Session = Depends(get_db)):
    """Retrieves recent job discovery logs (NEW, UPDATED, SKIPPED, WITHDRAWN)."""
    repo = DiscoveryLogRepository(db)
    logs = repo.get_recent(limit=limit)
    payload = [
        {
            "id": l.id,
            "source_code": l.source_code,
            "action": l.action,
            "advt_number": l.advt_number,
            "job_title": l.job_title,
            "content_hash": l.content_hash,
            "details": l.details,
            "discovered_at": l.discovered_at
        }
        for l in logs
    ]
    return APIResponse(data=payload, message="Discovery logs retrieved")
