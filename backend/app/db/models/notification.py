import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id"), nullable=False)
    
    eligibility_status: Mapped[str] = mapped_column(String(30), nullable=False) # ELIGIBLE, PARTIALLY_ELIGIBLE, NOT_ELIGIBLE
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    match_reasons: Mapped[dict] = mapped_column(JSON, default=list)
    missing_requirements: Mapped[dict] = mapped_column(JSON, default=list)
    
    telegram_message_id: Mapped[str] = mapped_column(String(100), nullable=True)
    user_action: Mapped[str] = mapped_column(String(30), default="PENDING") # PENDING, APPLY_CLICKED, IGNORED, REMIND_LATER
    
    sent_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    job: Mapped["Job"] = relationship("Job", back_populates="notifications")
