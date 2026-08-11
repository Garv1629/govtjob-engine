import uuid
from datetime import datetime, timezone, date
from sqlalchemy import String, Boolean, DateTime, Date, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), unique=True, nullable=False)
    
    dob: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    category: Mapped[str] = mapped_column(String(20), nullable=False) # UR, OBC, SC, ST, EWS
    is_pwbd: Mapped[bool] = mapped_column(Boolean, default=False)
    pwbd_type: Mapped[str] = mapped_column(String(100), nullable=True)
    is_ex_serviceman: Mapped[bool] = mapped_column(Boolean, default=False)
    state_of_domicile: Mapped[str] = mapped_column(String(100), nullable=False)
    
    qualifications: Mapped[dict] = mapped_column(JSON, default=dict) # Degree, Univ, %, Year
    experiences: Mapped[dict] = mapped_column(JSON, default=dict) # History, months
    physical_attributes: Mapped[dict] = mapped_column(JSON, default=dict) # Height, Vision
    encrypted_vault: Mapped[str] = mapped_column(String(2000), nullable=True) # Sensitive PII

    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship("User", back_populates="profile")
