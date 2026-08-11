from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from app.modules.workflow.enums import WorkflowState, WorkflowStep
from app.core.logging import logger


class WorkflowHistoryEntry(BaseModel):
    entry_id: str
    workflow_id: str
    step_name: str
    state: str
    event_type: Optional[str] = None
    detail: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class WorkflowHistory:
    """
    Tracks, records, and retrieves step executions, state transitions, user decisions,
    and event timelines for complete auditability.
    """

    def __init__(self):
        self._entries: Dict[str, List[WorkflowHistoryEntry]] = {}

    def record_step(
        self,
        workflow_id: str,
        step_name: str,
        state: str,
        detail: str,
        event_type: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None
    ) -> WorkflowHistoryEntry:
        """Records an execution step or event in workflow timeline."""
        if workflow_id not in self._entries:
            self._entries[workflow_id] = []

        entry = WorkflowHistoryEntry(
            entry_id=f"{workflow_id}_{len(self._entries[workflow_id]) + 1}",
            workflow_id=workflow_id,
            step_name=step_name,
            state=state,
            event_type=event_type,
            detail=detail,
            payload=payload or {}
        )
        self._entries[workflow_id].append(entry)
        logger.info(f"[WorkflowHistory] [{workflow_id}] {step_name} -> {state}: {detail}")
        return entry

    def get_history(self, workflow_id: str) -> List[WorkflowHistoryEntry]:
        """Retrieves timeline entries for a workflow."""
        return list(self._entries.get(workflow_id, []))

    def get_timeline_dict(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Returns JSON-serializable list of history entries."""
        entries = self.get_history(workflow_id)
        return [e.model_dump(mode="json") for e in entries]

    def clear(self, workflow_id: Optional[str] = None) -> None:
        if workflow_id:
            self._entries.pop(workflow_id, None)
        else:
            self._entries.clear()


# Global WorkflowHistory Singleton
global_workflow_history = WorkflowHistory()
