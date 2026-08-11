from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.workflow.orchestrator import WorkflowOrchestrator
from app.modules.workflow.schemas import (
    WorkflowTriggerInput,
    UserDecisionInput,
    ManualActionResumeInput,
    WorkflowResponse,
    WorkflowHistoryOutput
)
from app.modules.workflow.registry import global_workflow_registry
from app.modules.workflow.history import global_workflow_history
from app.modules.workflow.metrics import global_workflow_metrics
from app.db.repositories import WorkflowInstanceRepository
from app.core.logging import logger

router = APIRouter(prefix="/workflow", tags=["Master AI Orchestration Engine"])


@router.post("/trigger", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def trigger_job_workflow(
    input_data: WorkflowTriggerInput,
    db: Session = Depends(get_db)
):
    """
    Triggers the Master AI Orchestration Engine for a newly discovered government job notification.
    Runs steps 1-9 (Discovery -> Duplicate Check -> PDF Download -> AI Extraction -> JSON Validation -> Eligibility -> Summary -> Alert -> Wait User Decision).
    """
    logger.info(f"API trigger job workflow received for '{input_data.job_title}'")
    orchestrator = WorkflowOrchestrator(db=db)
    result = await orchestrator.start_job_workflow(
        job_data=input_data.model_dump(),
        user_id=input_data.user_id
    )
    return result


@router.post("/{workflow_id}/decision", response_model=Dict[str, Any])
async def submit_user_decision(
    workflow_id: str,
    input_data: UserDecisionInput,
    db: Session = Depends(get_db)
):
    """
    Submits candidate decision (IGNORE, REMIND, APPLY) for an interactive alert.
    If APPLY, triggers browser automation (Login -> Form Fill -> Documents -> Pause for Manual Payment/OTP).
    """
    logger.info(f"API user decision '{input_data.decision}' for workflow '{workflow_id}'")
    orchestrator = WorkflowOrchestrator(db=db)
    result = await orchestrator.process_user_decision(
        workflow_id=workflow_id,
        decision=input_data.decision,
        payload=input_data.model_dump(exclude_unset=True)
    )
    return result


@router.post("/{workflow_id}/resume", response_model=Dict[str, Any])
async def resume_manual_action(
    workflow_id: str,
    input_data: ManualActionResumeInput,
    db: Session = Depends(get_db)
):
    """
    Resumes a paused browser automation workflow after user completes payment / OTP manual confirmation.
    """
    logger.info(f"API resume manual action for workflow '{workflow_id}'")
    orchestrator = WorkflowOrchestrator(db=db)
    result = await orchestrator.resume_manual_action(
        workflow_id=workflow_id,
        confirmation_payload=input_data.confirmation_payload
    )
    return result


@router.get("/metrics", response_model=Dict[str, Any])
async def get_orchestrator_metrics(db: Session = Depends(get_db)):
    """
    Retrieves real-time observability telemetry metrics for the Master AI Orchestration Engine.
    """
    instance_repo = WorkflowInstanceRepository(db)
    active_instances = instance_repo.get_active_workflows()
    state_counts = {}
    for inst in active_instances:
        state_counts[inst.current_state] = state_counts.get(inst.current_state, 0) + 1

    summary = global_workflow_metrics.get_summary(active_state_counts=state_counts)
    return summary.model_dump(mode="json")


@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow_status(workflow_id: str, db: Session = Depends(get_db)):
    """
    Retrieves detailed current state, step, and context for a workflow.
    """
    instance_repo = WorkflowInstanceRepository(db)
    instance = instance_repo.get_by_id(workflow_id)
    if not instance:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found.")

    return WorkflowResponse(
        workflow_id=instance.id,
        job_id=instance.job_id,
        user_id=instance.user_id,
        application_id=instance.application_id,
        current_state=instance.current_state,
        current_step=instance.current_step,
        user_decision=instance.user_decision,
        is_completed=instance.current_state == "COMPLETED",
        is_failed=instance.current_state == "FAILED",
        last_error=instance.last_error,
        created_at=instance.created_at,
        updated_at=instance.updated_at,
        context_data=instance.context_data or {}
    )


@router.get("/{workflow_id}/history", response_model=WorkflowHistoryOutput)
async def get_workflow_history_timeline(workflow_id: str):
    """
    Retrieves complete timeline execution history and state transition logs for auditability.
    """
    timeline = global_workflow_history.get_timeline_dict(workflow_id)
    reg = global_workflow_registry.get_instance(workflow_id)
    current_state = reg.state_machine.current_state.value if reg else "UNKNOWN"
    return WorkflowHistoryOutput(
        workflow_id=workflow_id,
        current_state=current_state,
        timeline=timeline
    )


@router.post("/{workflow_id}/recover", response_model=Dict[str, Any])
async def recover_workflow(workflow_id: str, db: Session = Depends(get_db)):
    """
    Recovers a failed or stranded workflow from its last valid checkpoint snapshot.
    """
    orchestrator = WorkflowOrchestrator(db=db)
    result = await orchestrator.recover_workflow(workflow_id)
    return result
