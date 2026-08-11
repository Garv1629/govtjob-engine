import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class EligibilityResult(Base):
    __tablename__ = "eligibility_results"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id", ondelete="CASCADE"), index=True, nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    
    status: Mapped[str] = mapped_column(String(30), nullable=False) # ELIGIBLE, PARTIALLY_ELIGIBLE, NOT_ELIGIBLE
    overall_score: Mapped[float] = mapped_column(Float, default=0.0)
    
    scores: Mapped[dict] = mapped_column(JSON, nullable=False) # Age, Qualification, Experience, Medical, Document scores
    reasons: Mapped[list] = mapped_column(JSON, nullable=False)
    matched_rules: Mapped[list] = mapped_column(JSON, nullable=False)
    failed_rules: Mapped[list] = mapped_column(JSON, nullable=False)
    missing_documents: Mapped[list] = mapped_column(JSON, nullable=False)
    recommendations: Mapped[list] = mapped_column(JSON, nullable=False)
    
    evaluated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        index=True
    )
