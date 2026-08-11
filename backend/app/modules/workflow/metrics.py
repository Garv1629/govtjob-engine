from typing import Dict, Any, List, Optional
from collections import Counter
from datetime import datetime, timezone
import statistics
from pydantic import BaseModel, Field
from app.modules.workflow.enums import WorkflowState
from app.core.logging import logger


class MetricSnapshot(BaseModel):
    current_workflows_count: int = 0
    running_workflows_count: int = 0
    completed_workflows_count: int = 0
    failed_workflows_count: int = 0
    cancelled_workflows_count: int = 0
    total_retries_count: int = 0
    avg_processing_time_seconds: float = 0.0
    avg_automation_time_seconds: float = 0.0
    failure_reasons_breakdown: Dict[str, int] = Field(default_factory=dict)
    state_breakdown: Dict[str, int] = Field(default_factory=dict)


class WorkflowMetrics:
    """
    Telemetry and observability metrics tracker for the Master AI Orchestration Engine.
    """

    def __init__(self):
        self._processing_times: List[float] = []
        self._automation_times: List[float] = []
        self._total_retries: int = 0
        self._completed_count: int = 0
        self._failed_count: int = 0
        self._cancelled_count: int = 0
        self._failure_reasons: Counter = Counter()

    def record_processing_time(self, duration_seconds: float) -> None:
        """Record duration from job discovery to WAITING_FOR_USER."""
        if duration_seconds > 0:
            self._processing_times.append(duration_seconds)
            logger.debug(f"[WorkflowMetrics] Recorded processing time: {duration_seconds:.2f}s")

    def record_automation_time(self, duration_seconds: float) -> None:
        """Record duration of browser automation run."""
        if duration_seconds > 0:
            self._automation_times.append(duration_seconds)
            logger.debug(f"[WorkflowMetrics] Recorded automation time: {duration_seconds:.2f}s")

    def record_retry(self, step_name: str, count: int = 1) -> None:
        self._total_retries += count

    def record_completion(self, final_state: WorkflowState) -> None:
        if final_state == WorkflowState.COMPLETED:
            self._completed_count += 1
        elif final_state == WorkflowState.CANCELLED:
            self._cancelled_count += 1
        elif final_state == WorkflowState.FAILED:
            self._failed_count += 1

    def record_failure_reason(self, reason: str) -> None:
        if reason:
            self._failure_reasons[reason] += 1
            self._failed_count += 1

    def get_summary(self, active_state_counts: Optional[Dict[str, int]] = None) -> MetricSnapshot:
        active_counts = active_state_counts or {}

        running_states = [
            WorkflowState.PROCESSING.value,
            WorkflowState.ANALYZED.value,
            WorkflowState.WAITING_FOR_USER.value,
            WorkflowState.AUTOMATION_RUNNING.value,
            WorkflowState.WAITING_FOR_MANUAL_ACTION.value,
            WorkflowState.RESUMED.value
        ]

        running_count = sum(active_counts.get(s, 0) for s in running_states)
        total_active = sum(active_counts.values())

        avg_proc = round(statistics.mean(self._processing_times), 2) if self._processing_times else 0.0
        avg_auto = round(statistics.mean(self._automation_times), 2) if self._automation_times else 0.0

        return MetricSnapshot(
            current_workflows_count=total_active,
            running_workflows_count=running_count,
            completed_workflows_count=self._completed_count,
            failed_workflows_count=self._failed_count,
            cancelled_workflows_count=self._cancelled_count,
            total_retries_count=self._total_retries,
            avg_processing_time_seconds=avg_proc,
            avg_automation_time_seconds=avg_auto,
            failure_reasons_breakdown=dict(self._failure_reasons),
            state_breakdown=active_counts
        )


# Global WorkflowMetrics Singleton
global_workflow_metrics = WorkflowMetrics()
