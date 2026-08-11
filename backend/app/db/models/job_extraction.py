import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Float, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class JobExtraction(Base):
    __tablename__ = "job_extractions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id", ondelete="CASCADE"), index=True, nullable=False)
    
    extraction_version: Mapped[str] = mapped_column(String(20), default="1.0.0")
    llm_provider: Mapped[str] = mapped_column(String(50), nullable=False) # e.g. OpenAI, Mock
    llm_model_used: Mapped[str] = mapped_column(String(100), nullable=False) # e.g. gpt-4o, gpt-3.5-turbo
    
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0)
    raw_text: Mapped[str] = mapped_column(Text, nullable=True)
    extracted_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    
    processing_time_ms: Mapped[float] = mapped_column(Float, default=0.0)
    ocr_time_ms: Mapped[float] = mapped_column(Float, default=0.0)
    llm_time_ms: Mapped[float] = mapped_column(Float, default=0.0)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        index=True
    )
