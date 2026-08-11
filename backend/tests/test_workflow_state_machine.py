import pytest
from app.modules.workflow.state_machine import StateMachine, InvalidStateTransitionError
from app.modules.workflow.enums import WorkflowState, WorkflowStep


def test_state_machine_initial_state():
    sm = StateMachine()
    assert sm.current_state == WorkflowState.DISCOVERED
    assert len(sm.get_history()) == 0


def test_valid_state_transitions():
    sm = StateMachine(initial_state=WorkflowState.DISCOVERED)

    # 1. DISCOVERED -> PROCESSING
    rec1 = sm.transition_to(WorkflowState.PROCESSING, WorkflowStep.JOB_DISCOVERED)
    assert sm.current_state == WorkflowState.PROCESSING
    assert rec1.from_state == WorkflowState.DISCOVERED
    assert rec1.to_state == WorkflowState.PROCESSING

    # 2. PROCESSING -> ANALYZED
    sm.transition_to(WorkflowState.ANALYZED, WorkflowStep.GENERATE_SUMMARY)
    assert sm.current_state == WorkflowState.ANALYZED

    # 3. ANALYZED -> WAITING_FOR_USER
    sm.transition_to(WorkflowState.WAITING_FOR_USER, WorkflowStep.WAIT_USER_DECISION)
    assert sm.current_state == WorkflowState.WAITING_FOR_USER

    # 4. WAITING_FOR_USER -> AUTOMATION_RUNNING (User selected APPLY)
    sm.transition_to(WorkflowState.AUTOMATION_RUNNING, WorkflowStep.AUTOMATION_START)
    assert sm.current_state == WorkflowState.AUTOMATION_RUNNING

    # 5. AUTOMATION_RUNNING -> SUBMITTED
    sm.transition_to(WorkflowState.SUBMITTED, WorkflowStep.AUTOMATION_SUBMIT)
    assert sm.current_state == WorkflowState.SUBMITTED

    # 6. SUBMITTED -> COMPLETED
    sm.transition_to(WorkflowState.COMPLETED, WorkflowStep.COMPLETE_WORKFLOW)
    assert sm.current_state == WorkflowState.COMPLETED

    assert len(sm.get_history()) == 6


def test_invalid_state_transition_raises_error():
    sm = StateMachine(initial_state=WorkflowState.DISCOVERED)
    
    # Direct transition from DISCOVERED -> SUBMITTED is invalid
    with pytest.raises(InvalidStateTransitionError):
        sm.transition_to(WorkflowState.SUBMITTED, WorkflowStep.AUTOMATION_SUBMIT)


def test_user_decision_ignore_transition():
    sm = StateMachine(initial_state=WorkflowState.WAITING_FOR_USER)
    sm.transition_to(WorkflowState.CANCELLED, WorkflowStep.WAIT_USER_DECISION, reason="User IGNORED job")
    assert sm.current_state == WorkflowState.CANCELLED


def test_manual_action_pause_and_resume_transitions():
    sm = StateMachine(initial_state=WorkflowState.AUTOMATION_RUNNING)
    
    # AUTOMATION_RUNNING -> WAITING_FOR_MANUAL_ACTION
    sm.transition_to(WorkflowState.WAITING_FOR_MANUAL_ACTION, WorkflowStep.AUTOMATION_MANUAL_PAUSE)
    assert sm.current_state == WorkflowState.WAITING_FOR_MANUAL_ACTION

    # WAITING_FOR_MANUAL_ACTION -> RESUMED
    sm.transition_to(WorkflowState.RESUMED, WorkflowStep.AUTOMATION_RESUME)
    assert sm.current_state == WorkflowState.RESUMED

    # RESUMED -> SUBMITTED
    sm.transition_to(WorkflowState.SUBMITTED, WorkflowStep.AUTOMATION_SUBMIT)
    assert sm.current_state == WorkflowState.SUBMITTED
