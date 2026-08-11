from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from app.modules.workflow.enums import WorkflowState, UserDecision, WorkflowStep


class WorkflowTriggerInput(BaseModel):
    user_id: str
    source_code: str = "SSC"
    organization: str
    advt_number: str
    job_title: str
    pdf_url: str
    apply_url: str
    total_vacancies: int = 0
    last_date: Optional[datetime] = None
    extra_meta: Dict[str, Any] = Field(default_factory=dict)


class UserDecisionInput(BaseModel):
    decision: UserDecision  # IGNORE, REMIND, APPLY
    reminder_datetime: Optional[datetime] = None
    reminder_hours: Optional[int] = None
    notes: Optional[str] = None


class ManualActionResumeInput(BaseModel):
    confirmation_payload: Dict[str, Any] = Field(
        default_factory=dict,
        description="Credentials, OTP, payment confirmation, or verification token"
    )


class WorkflowResponse(BaseModel):
    workflow_id: str
    job_id: Optional[str] = None
    user_id: Optional[str] = None
    application_id: Optional[str] = None
    current_state: str
    current_step: str
    user_decision: Optional[str] = None
    is_completed: bool
    is_failed: bool
    last_error: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    context_data: Dict[str, Any] = Field(default_factory=dict)


class WorkflowHistoryOutput(BaseModel):
    workflow_id: str
    current_state: str
    timeline: List[Dict[str, Any]]
