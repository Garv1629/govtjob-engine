import asyncio
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.db.repositories import WorkflowInstanceRepository, WorkflowCheckpointRepository
from app.db.models.workflow_instance import WorkflowInstance, WorkflowCheckpoint
from app.modules.workflow.enums import WorkflowState, WorkflowStep
from app.core.config import settings
from app.core.logging import logger


class WorkflowRecovery:
    """
    Failure recovery engine managing automatic retries with exponential backoff,
    checkpoint persistence, crash recovery, and workflow resumption.
    """

    def __init__(self, db: Session):
        self.db = db
        self.instance_repo = WorkflowInstanceRepository(db)
        self.checkpoint_repo = WorkflowCheckpointRepository(db)
        self.max_retries = settings.WORKFLOW_MAX_RETRIES
        self.backoff_factor = settings.WORKFLOW_RETRY_BACKOFF_FACTOR

    def save_checkpoint(
        self,
        workflow_id: str,
        step_name: str,
        state: str,
        checkpoint_data: Dict[str, Any]
    ) -> WorkflowCheckpoint:
        """Saves a checkpoint snapshot to DB for fault recovery."""
        checkpoint = self.checkpoint_repo.create({
            "workflow_id": workflow_id,
            "step_name": step_name,
            "state": state,
            "checkpoint_data": checkpoint_data,
            "timestamp": datetime.now(timezone.utc)
        })

        # Update current step and state in workflow instance
        self.instance_repo.update(workflow_id, {
            "current_step": step_name,
            "current_state": state,
            "context_data": checkpoint_data
        })

        logger.info(f"[WorkflowRecovery] Created checkpoint for workflow '{workflow_id}' at step '{step_name}' ({state})")
        return checkpoint

    def get_last_checkpoint(self, workflow_id: str) -> Optional[WorkflowCheckpoint]:
        """Retrieves most recent valid checkpoint."""
        return self.checkpoint_repo.get_latest_checkpoint(workflow_id)

    async def calculate_retry_delay(self, retry_count: int) -> float:
        """Calculates backoff delay in seconds for retries."""
        return min(60.0, (self.backoff_factor ** retry_count) * 2.0)

    def handle_step_failure(
        self,
        workflow_id: str,
        error_msg: str,
        current_step: str
    ) -> Tuple[bool, int]:
        """
        Increments retry count in DB instance and determines if retry attempt is allowed.
        Returns tuple of (should_retry, new_retry_count).
        """
        instance = self.instance_repo.get_by_id(workflow_id)
        if not instance:
            return False, 0

        new_retry_count = instance.retry_count + 1
        should_retry = new_retry_count <= self.max_retries

        new_state = instance.current_state if should_retry else WorkflowState.FAILED.value

        self.instance_repo.update(workflow_id, {
            "retry_count": new_retry_count,
            "last_error": error_msg,
            "current_state": new_state
        })

        logger.warning(
            f"[WorkflowRecovery] Failure at step '{current_step}' for workflow '{workflow_id}'. Retry {new_retry_count}/{self.max_retries}. Should retry: {should_retry}. Error: {error_msg}"
        )
        return should_retry, new_retry_count

    def perform_crash_recovery(self) -> List[Dict[str, Any]]:
        """
        Scans DB on application startup for interrupted or stranded active workflows.
        Attempts recovery or resets stranded states.
        """
        incomplete = self.instance_repo.get_incomplete_workflows()
        recovered_list = []

        logger.info(f"[WorkflowRecovery] Performing crash recovery check. Found {len(incomplete)} incomplete workflows.")

        for instance in incomplete:
            latest_cp = self.get_last_checkpoint(instance.id)
            status_info = {
                "workflow_id": instance.id,
                "previous_state": instance.current_state,
                "recovered_step": latest_cp.step_name if latest_cp else instance.current_step,
                "has_checkpoint": latest_cp is not None
            }

            # If stranded in processing or automation_running, set to recoverable or failed for retry
            if instance.current_state in [WorkflowState.PROCESSING.value, WorkflowState.AUTOMATION_RUNNING.value]:
                if latest_cp:
                    self.instance_repo.update(instance.id, {
                        "current_state": latest_cp.state,
                        "current_step": latest_cp.step_name,
                        "context_data": latest_cp.checkpoint_data,
                        "last_error": "System rebooted during step execution; restored to last checkpoint."
                    })
                    status_info["status"] = "RESTORED_TO_CHECKPOINT"
                else:
                    self.instance_repo.update(instance.id, {
                        "current_state": WorkflowState.FAILED.value,
                        "last_error": "System rebooted during step execution with no checkpoint."
                    })
                    status_info["status"] = "MARKED_FAILED"
            else:
                status_info["status"] = "RETAINED_STATE"

            recovered_list.append(status_info)

        return recovered_list
