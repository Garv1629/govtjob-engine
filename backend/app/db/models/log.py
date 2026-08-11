import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class Log(Base):
    __tablename__ = "system_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    level: Mapped[str] = mapped_column(String(20), index=True, nullable=False) # INFO, WARNING, ERROR, CRITICAL
    module: Mapped[str] = mapped_column(String(100), index=True, nullable=False) # Scraper, AI, Automator
    message: Mapped[str] = mapped_column(Text, nullable=False)
    extra_data: Mapped[dict] = mapped_column(JSON, default=dict)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
