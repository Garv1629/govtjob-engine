import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Integer, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class WorkflowInstance(Base):
    __tablename__ = "workflow_instances"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id"), nullable=True, index=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=True, index=True)
    application_id: Mapped[str] = mapped_column(String(36), ForeignKey("applications.id"), nullable=True, index=True)

    current_state: Mapped[str] = mapped_column(String(50), default="DISCOVERED", index=True)
    current_step: Mapped[str] = mapped_column(String(100), default="DISCOVERY", index=True)
    user_decision: Mapped[str] = mapped_column(String(50), nullable=True)

    context_data: Mapped[dict] = mapped_column(JSON, default=dict)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    last_error: Mapped[str] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    checkpoints: Mapped[list["WorkflowCheckpoint"]] = relationship(
        "WorkflowCheckpoint",
        back_populates="workflow",
        cascade="all, delete-orphan"
    )


class WorkflowCheckpoint(Base):
    __tablename__ = "workflow_checkpoints"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_id: Mapped[str] = mapped_column(String(36), ForeignKey("workflow_instances.id"), nullable=False, index=True)
    step_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    state: Mapped[str] = mapped_column(String(50), nullable=False)
    checkpoint_data: Mapped[dict] = mapped_column(JSON, default=dict)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    workflow: Mapped["WorkflowInstance"] = relationship("WorkflowInstance", back_populates="checkpoints")
