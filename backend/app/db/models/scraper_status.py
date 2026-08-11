import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Integer, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class ScraperStatus(Base):
    __tablename__ = "scraper_statuses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False) # e.g. SSC, UPSC
    source_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    last_run_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    last_status: Mapped[str] = mapped_column(String(30), default="IDLE") # IDLE, RUNNING, SUCCESS, ERROR
    total_jobs_found: Mapped[int] = mapped_column(Integer, default=0)
    last_error: Mapped[str] = mapped_column(Text, nullable=True)
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
