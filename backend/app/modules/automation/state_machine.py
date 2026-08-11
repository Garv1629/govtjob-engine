from enum import Enum
from typing import List


class AutomationState(str, Enum):
    INITIALIZED = "INITIALIZED"
    LOGGED_IN = "LOGGED_IN"
    FORM_IN_PROGRESS = "FORM_IN_PROGRESS"
    WAITING_FOR_MANUAL_ACTION = "WAITING_FOR_MANUAL_ACTION"
    READY_TO_SUBMIT = "READY_TO_SUBMIT"
    SUBMITTED = "SUBMITTED"
    FAILED = "FAILED"
    RECOVERABLE_ERROR = "RECOVERABLE_ERROR"


class AutomationStateMachine:
    """Manages legal state transitions for the Browser Application Engine."""

    VALID_TRANSITIONS = {
        AutomationState.INITIALIZED: [AutomationState.LOGGED_IN, AutomationState.WAITING_FOR_MANUAL_ACTION, AutomationState.FAILED],
        AutomationState.LOGGED_IN: [AutomationState.FORM_IN_PROGRESS, AutomationState.WAITING_FOR_MANUAL_ACTION, AutomationState.FAILED],
        AutomationState.FORM_IN_PROGRESS: [AutomationState.WAITING_FOR_MANUAL_ACTION, AutomationState.READY_TO_SUBMIT, AutomationState.RECOVERABLE_ERROR, AutomationState.FAILED],
        AutomationState.WAITING_FOR_MANUAL_ACTION: [AutomationState.FORM_IN_PROGRESS, AutomationState.READY_TO_SUBMIT, AutomationState.FAILED],
        AutomationState.READY_TO_SUBMIT: [AutomationState.SUBMITTED, AutomationState.WAITING_FOR_MANUAL_ACTION, AutomationState.FAILED],
        AutomationState.RECOVERABLE_ERROR: [AutomationState.FORM_IN_PROGRESS, AutomationState.FAILED],
        AutomationState.SUBMITTED: [],
        AutomationState.FAILED: [AutomationState.INITIALIZED]
    }

    def __init__(self, initial_state: AutomationState = AutomationState.INITIALIZED):
        self.current_state = initial_state

    def transition_to(self, new_state: AutomationState) -> bool:
        allowed = self.VALID_TRANSITIONS.get(self.current_state, [])
        if new_state in allowed:
            self.current_state = new_state
            return True
        else:
            raise ValueError(f"Invalid state transition from {self.current_state} to {new_state}")
