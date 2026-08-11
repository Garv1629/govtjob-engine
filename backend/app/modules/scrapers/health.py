import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.db.repositories import ScraperHealthRepository
from app.core.logging import logger


class ScraperHealthMonitor:
    """Tracks scraper telemetry, execution status, response times, and failure counts."""

    @staticmethod
    def record_success(db: Session, source_code: str, response_time_ms: float, jobs_found: int) -> None:
        repo = ScraperHealthRepository(db)
        health = repo.get_by_source_code(source_code)
        now = datetime.now(timezone.utc)

        if not health:
            repo.create({
                "source_code": source_code,
                "status": "HEALTHY",
                "last_success_at": now,
                "consecutive_failures": 0,
                "failure_count": 0,
                "avg_response_time_ms": response_time_ms,
                "total_jobs_found": jobs_found,
                "last_run_jobs_found": jobs_found
            })
        else:
            # Update moving average response time
            new_avg = (health.avg_response_time_ms + response_time_ms) / 2 if health.avg_response_time_ms > 0 else response_time_ms
            repo.update(health.id, {
                "status": "HEALTHY",
                "last_success_at": now,
                "consecutive_failures": 0,
                "avg_response_time_ms": round(new_avg, 2),
                "total_jobs_found": health.total_jobs_found + jobs_found,
                "last_run_jobs_found": jobs_found,
                "last_error_message": None
            })
        logger.info(f"[{source_code}] Telemetry recorded: HEALTHY ({jobs_found} jobs, {response_time_ms:.2f}ms)")

    @staticmethod
    def record_failure(db: Session, source_code: str, error_message: str) -> None:
        repo = ScraperHealthRepository(db)
        health = repo.get_by_source_code(source_code)
        now = datetime.now(timezone.utc)

        if not health:
            repo.create({
                "source_code": source_code,
                "status": "FAILED",
                "last_failure_at": now,
                "failure_count": 1,
                "consecutive_failures": 1,
                "last_error_message": error_message
            })
        else:
            consecutive = health.consecutive_failures + 1
            new_status = "DEGRADED" if consecutive < 3 else "FAILED"
            repo.update(health.id, {
                "status": new_status,
                "last_failure_at": now,
                "failure_count": health.failure_count + 1,
                "consecutive_failures": consecutive,
                "last_error_message": error_message
            })
        logger.error(f"[{source_code}] Telemetry recorded: FAILURE - {error_message}")
