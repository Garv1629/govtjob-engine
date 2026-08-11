from typing import Dict, Set, Optional, List, Tuple
from datetime import datetime, timezone
from app.modules.workflow.enums import WorkflowState, WorkflowStep
from app.core.logging import logger
from app.core.exceptions import BaseCustomException


class InvalidStateTransitionError(BaseCustomException):
    """Exception raised when an invalid workflow state transition is attempted."""
    def __init__(self, current_state: WorkflowState, target_state: WorkflowState, reason: str = ""):
        message = f"Invalid state transition from '{current_state.value}' to '{target_state.value}'."
        if reason:
            message += f" Reason: {reason}"
        super().__init__(message=message, status_code=400)
        self.current_state = current_state
        self.target_state = target_state


class TransitionRecord:
    def __init__(
        self,
        from_state: WorkflowState,
        to_state: WorkflowState,
        step: WorkflowStep,
        reason: Optional[str] = None
    ):
        self.from_state = from_state
        self.to_state = to_state
        self.step = step
        self.reason = reason
        self.timestamp = datetime.now(timezone.utc)

    def to_dict(self) -> Dict:
        return {
            "from_state": self.from_state.value,
            "to_state": self.to_state.value,
            "step": self.step.value,
            "reason": self.reason,
            "timestamp": self.timestamp.isoformat()
        }


class StateMachine:
    """
    State machine enforcing valid lifecycle state transitions for Government Job Application Workflows.
    """

    ALLOWED_TRANSITIONS: Dict[WorkflowState, Set[WorkflowState]] = {
        WorkflowState.DISCOVERED: {
            WorkflowState.PROCESSING,
            WorkflowState.FAILED,
            WorkflowState.CANCELLED,
        },
        WorkflowState.PROCESSING: {
            WorkflowState.ANALYZED,
            WorkflowState.FAILED,
            WorkflowState.CANCELLED,
        },
        WorkflowState.ANALYZED: {
            WorkflowState.WAITING_FOR_USER,
            WorkflowState.FAILED,
            WorkflowState.CANCELLED,
        },
        WorkflowState.WAITING_FOR_USER: {
            WorkflowState.AUTOMATION_RUNNING,
            WorkflowState.WAITING_FOR_USER,  # Remind re-schedule
            WorkflowState.CANCELLED,          # Ignore
            WorkflowState.FAILED,
        },
        WorkflowState.AUTOMATION_RUNNING: {
            WorkflowState.WAITING_FOR_MANUAL_ACTION,
            WorkflowState.SUBMITTED,
            WorkflowState.FAILED,
            WorkflowState.CANCELLED,
        },
        WorkflowState.WAITING_FOR_MANUAL_ACTION: {
            WorkflowState.RESUMED,
            WorkflowState.CANCELLED,
            WorkflowState.FAILED,
        },
        WorkflowState.RESUMED: {
            WorkflowState.AUTOMATION_RUNNING,
            WorkflowState.SUBMITTED,
            WorkflowState.FAILED,
            WorkflowState.CANCELLED,
        },
        WorkflowState.SUBMITTED: {
            WorkflowState.COMPLETED,
            WorkflowState.FAILED,
        },
        WorkflowState.FAILED: {
            WorkflowState.PROCESSING,
            WorkflowState.AUTOMATION_RUNNING,
            WorkflowState.RESUMED,
            WorkflowState.CANCELLED,
        },
        WorkflowState.CANCELLED: {
            WorkflowState.PROCESSING,
            WorkflowState.DISCOVERED,
        },
        WorkflowState.COMPLETED: {
            WorkflowState.PROCESSING, # Allow re-trigger if requested
        }
    }

    def __init__(self, initial_state: WorkflowState = WorkflowState.DISCOVERED):
        self.current_state: WorkflowState = initial_state
        self.history: List[TransitionRecord] = []

    def can_transition_to(self, target_state: WorkflowState) -> bool:
        """Checks whether transitioning to target_state is valid from current_state."""
        allowed = self.ALLOWED_TRANSITIONS.get(self.current_state, set())
        return target_state in allowed

    def transition_to(
        self,
        target_state: WorkflowState,
        step: WorkflowStep,
        reason: Optional[str] = None
    ) -> TransitionRecord:
        """
        Executes transition to target_state if permitted, recording history and logging transition.
        """
        if not self.can_transition_to(target_state):
            logger.error(
                f"[StateMachine] Invalid transition attempted: {self.current_state.value} -> {target_state.value} at step {step.value}"
            )
            raise InvalidStateTransitionError(
                current_state=self.current_state,
                target_state=target_state,
                reason=reason or f"Transition not allowed from step {step.value}"
            )

        from_state = self.current_state
        self.current_state = target_state
        record = TransitionRecord(
            from_state=from_state,
            to_state=target_state,
            step=step,
            reason=reason
        )
        self.history.append(record)

        logger.info(
            f"[StateMachine] Transitioned: {from_state.value} -> {target_state.value} [Step: {step.value}] {f'Reason: {reason}' if reason else ''}"
        )
        return record

    def get_history(self) -> List[Dict]:
        return [record.to_dict() for record in self.history]
