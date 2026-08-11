import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Integer, DateTime, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class DiscoveryLog(Base):
    __tablename__ = "discovery_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_code: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False) # DISCOVERED_NEW, UPDATED_NOTIFICATION, WITHDRAWN_JOB, DUPLICATE_SKIPPED
    
    advt_number: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    job_title: Mapped[str] = mapped_column(String(255), nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    
    details: Mapped[dict] = mapped_column(JSON, default=dict)
    discovered_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
