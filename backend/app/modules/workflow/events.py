import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from app.modules.workflow.enums import WorkflowState, WorkflowStep, UserDecision


class WorkflowEvent(BaseModel):
    """Base class for all strongly-typed orchestrator events."""
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    workflow_id: str
    event_type: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    payload: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


# Strongly Typed Events as specified in Architecture Requirements

class JobDiscoveredEvent(WorkflowEvent):
    event_type: str = "JobDiscovered"
    job_id: str
    source_code: str
    title: str
    url: str

# Shorthand alias class for exact naming compatibility
JobDiscovered = JobDiscoveredEvent


class JobUpdatedEvent(WorkflowEvent):
    event_type: str = "JobUpdated"
    job_id: str
    changes: Dict[str, Any]

JobUpdated = JobUpdatedEvent


class JobIgnoredEvent(WorkflowEvent):
    event_type: str = "JobIgnored"
    job_id: str
    reason: Optional[str] = "User clicked Ignore"

JobIgnored = JobIgnoredEvent


class JobApprovedEvent(WorkflowEvent):
    event_type: str = "JobApproved"
    job_id: str
    user_id: str

JobApproved = JobApprovedEvent


class NotificationDownloadedEvent(WorkflowEvent):
    event_type: str = "NotificationDownloaded"
    pdf_url: str
    local_path: Optional[str] = None


class NotificationExtractedEvent(WorkflowEvent):
    event_type: str = "NotificationExtracted"
    extracted_text_length: int
    fields_found: int


class JSONValidatedEvent(WorkflowEvent):
    event_type: str = "JSONValidated"
    is_valid: bool
    schema_version: str = "1.0"


class EligibilityCompletedEvent(WorkflowEvent):
    event_type: str = "EligibilityCompleted"
    user_id: str
    status: str  # ELIGIBLE, PARTIALLY_ELIGIBLE, NOT_ELIGIBLE
    overall_score: float

EligibilityCompleted = EligibilityCompletedEvent


class SummaryGeneratedEvent(WorkflowEvent):
    event_type: str = "SummaryGenerated"
    summary_length: int
    key_takeaways_count: int

SummaryGenerated = SummaryGeneratedEvent


class ReminderScheduledEvent(WorkflowEvent):
    event_type: str = "ReminderScheduled"
    reminder_at: datetime


class AutomationStartedEvent(WorkflowEvent):
    event_type: str = "AutomationStarted"
    application_id: str
    source_code: str

AutomationStarted = AutomationStartedEvent


class ManualActionRequiredEvent(WorkflowEvent):
    event_type: str = "ManualActionRequired"
    session_id: str
    reason: str
    screenshot_path: Optional[str] = None

ManualActionRequired = ManualActionRequiredEvent


class AutomationResumedEvent(WorkflowEvent):
    event_type: str = "AutomationResumed"
    session_id: str

AutomationResumed = AutomationResumedEvent


class ApplicationSubmittedEvent(WorkflowEvent):
    event_type: str = "ApplicationSubmitted"
    application_id: str
    application_number: Optional[str] = None
    receipt_url: Optional[str] = None

ApplicationSubmitted = ApplicationSubmittedEvent


class ApplicationFailedEvent(WorkflowEvent):
    event_type: str = "ApplicationFailed"
    application_id: str
    error_message: str

ApplicationFailed = ApplicationFailedEvent


class WorkflowCompletedEvent(WorkflowEvent):
    event_type: str = "WorkflowCompleted"
    final_state: WorkflowState = WorkflowState.COMPLETED
    duration_seconds: float

WorkflowCompleted = WorkflowCompletedEvent


class WorkflowCancelledEvent(WorkflowEvent):
    event_type: str = "WorkflowCancelled"
    reason: str

WorkflowCancelled = WorkflowCancelledEvent


class StateTransitionEvent(WorkflowEvent):
    event_type: str = "StateTransition"
    from_state: WorkflowState
    to_state: WorkflowState
    step: WorkflowStep
    reason: Optional[str] = None
