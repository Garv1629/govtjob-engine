import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, Integer, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class JobSource(Base):
    __tablename__ = "job_sources"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False) # e.g. SSC, UPSC, NCS
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    base_url: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(100), default="Central Government")
    
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    priority: Mapped[int] = mapped_column(Integer, default=1) # 1 = Highest
    schedule_interval_minutes: Mapped[int] = mapped_column(Integer, default=30)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
