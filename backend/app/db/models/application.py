import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Float, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    
    status: Mapped[str] = mapped_column(String(50), default="INITIATED", index=True) 
    # INITIATED, LOGIN_SUCCESS, FORM_FILLED, DOCS_UPLOADED, PAUSED_BEFORE_PAYMENT, SUBMITTED, FAILED
    
    application_number: Mapped[str] = mapped_column(String(100), nullable=True)
    payment_status: Mapped[str] = mapped_column(String(50), default="UNPAID")
    payment_amount: Mapped[float] = mapped_column(Float, default=0.0)
    
    receipt_pdf_url: Mapped[str] = mapped_column(Text, nullable=True)
    screenshot_urls: Mapped[dict] = mapped_column(JSON, default=list)
    execution_logs: Mapped[dict] = mapped_column(JSON, default=list)
    error_message: Mapped[str] = mapped_column(Text, nullable=True)
    
    submitted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    job: Mapped["Job"] = relationship("Job", back_populates="applications")
    user: Mapped["User"] = relationship("User", back_populates="applications")
