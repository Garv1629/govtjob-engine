import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Integer, DateTime, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_code: Mapped[str] = mapped_column(String(50), index=True, nullable=False) # e.g. SSC, UPSC, IBPS
    organization: Mapped[str] = mapped_column(String(255), nullable=False)
    department: Mapped[str] = mapped_column(String(255), nullable=True)
    advt_number: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    job_title: Mapped[str] = mapped_column(String(255), nullable=False)
    
    total_vacancies: Mapped[int] = mapped_column(Integer, default=0)
    vacancies_breakdown: Mapped[dict] = mapped_column(JSON, default=dict)
    pay_level: Mapped[str] = mapped_column(String(50), nullable=True)
    grade_pay: Mapped[str] = mapped_column(String(50), nullable=True)
    salary_summary: Mapped[str] = mapped_column(String(255), nullable=True)
    
    min_age: Mapped[int] = mapped_column(Integer, nullable=True)
    max_age: Mapped[int] = mapped_column(Integer, nullable=True)
    age_relaxation_rules: Mapped[dict] = mapped_column(JSON, default=dict)
    qualifications: Mapped[dict] = mapped_column(JSON, default=dict)
    experience_required: Mapped[dict] = mapped_column(JSON, default=dict)
    fees: Mapped[dict] = mapped_column(JSON, default=dict)
    
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    last_date: Mapped[datetime] = mapped_column(DateTime, index=True, nullable=False)
    
    selection_process: Mapped[dict] = mapped_column(JSON, default=dict)
    syllabus: Mapped[dict] = mapped_column(JSON, default=dict)
    physical_standards: Mapped[dict] = mapped_column(JSON, default=dict)
    medical_standards: Mapped[dict] = mapped_column(JSON, default=dict)
    
    pdf_url: Mapped[str] = mapped_column(Text, nullable=False)
    apply_url: Mapped[str] = mapped_column(Text, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    applications: Mapped[list["Application"]] = relationship("Application", back_populates="job")
    notifications: Mapped[list["Notification"]] = relationship("Notification", back_populates="job")
