import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class AutomationSession(Base):
    __tablename__ = "automation_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    application_id: Mapped[str] = mapped_column(String(36), index=True, nullable=False)
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id", ondelete="CASCADE"), index=True, nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    source_code: Mapped[str] = mapped_column(String(50), nullable=False)
    
    current_state: Mapped[str] = mapped_column(String(50), default="INITIALIZED")
    manual_action_reason: Mapped[str] = mapped_column(String(255), nullable=True) # OTP, CAPTCHA, PAYMENT
    
    cookies: Mapped[dict] = mapped_column(JSON, default=dict)
    state_payload: Mapped[dict] = mapped_column(JSON, default=dict)
    latest_screenshot_path: Mapped[str] = mapped_column(String(500), nullable=True)
    receipt_path: Mapped[str] = mapped_column(String(500), nullable=True)
    audit_logs: Mapped[list] = mapped_column(JSON, default=list)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
