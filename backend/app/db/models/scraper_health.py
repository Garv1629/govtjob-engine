import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class ScraperHealth(Base):
    __tablename__ = "scraper_health"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    
    status: Mapped[str] = mapped_column(String(30), default="IDLE") # IDLE, RUNNING, HEALTHY, DEGRADED, FAILED
    last_success_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    last_failure_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    failure_count: Mapped[int] = mapped_column(Integer, default=0)
    consecutive_failures: Mapped[int] = mapped_column(Integer, default=0)
    
    avg_response_time_ms: Mapped[float] = mapped_column(Float, default=0.0)
    total_jobs_found: Mapped[int] = mapped_column(Integer, default=0)
    last_run_jobs_found: Mapped[int] = mapped_column(Integer, default=0)
    last_error_message: Mapped[str] = mapped_column(Text, nullable=True)
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
