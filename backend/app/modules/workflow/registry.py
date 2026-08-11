from typing import Dict, Any, Optional, List
from app.modules.workflow.state_machine import StateMachine
from app.modules.workflow.enums import WorkflowState
from app.core.logging import logger


class RegisteredWorkflow:
    def __init__(self, workflow_id: str, job_id: Optional[str] = None, user_id: Optional[str] = None):
        self.workflow_id = workflow_id
        self.job_id = job_id
        self.user_id = user_id
        self.state_machine = StateMachine(initial_state=WorkflowState.DISCOVERED)
        self.context: Dict[str, Any] = {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "job_id": self.job_id,
            "user_id": self.user_id,
            "current_state": self.state_machine.current_state.value,
            "context_keys": list(self.context.keys())
        }


class WorkflowRegistry:
    """
    Central registry keeping track of active workflow instances, definitions, and execution contexts.
    """

    def __init__(self):
        self._instances: Dict[str, RegisteredWorkflow] = {}

    def register_instance(
        self,
        workflow_id: str,
        job_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> RegisteredWorkflow:
        """Registers a new active workflow instance in memory."""
        instance = RegisteredWorkflow(workflow_id=workflow_id, job_id=job_id, user_id=user_id)
        self._instances[workflow_id] = instance
        logger.info(f"[WorkflowRegistry] Registered active workflow '{workflow_id}'")
        return instance

    def get_instance(self, workflow_id: str) -> Optional[RegisteredWorkflow]:
        return self._instances.get(workflow_id)

    def unregister_instance(self, workflow_id: str) -> bool:
        if workflow_id in self._instances:
            del self._instances[workflow_id]
            logger.info(f"[WorkflowRegistry] Unregistered workflow '{workflow_id}'")
            return True
        return False

    def list_active_instances(self) -> List[Dict[str, Any]]:
        return [inst.to_dict() for inst in self._instances.values()]


# Global WorkflowRegistry Singleton
global_workflow_registry = WorkflowRegistry()
