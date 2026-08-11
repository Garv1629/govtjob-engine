import asyncio
from typing import Dict, Any, Callable, Awaitable, Optional, List
import heapq
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from app.core.logging import logger


class WorkflowTask(BaseModel):
    task_id: str
    workflow_id: str
    step_name: str
    priority: int = 10  # Lower number = higher priority
    payload: Dict[str, Any] = Field(default_factory=dict)
    retries: int = 0
    max_retries: int = 3
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def __lt__(self, other: "WorkflowTask") -> bool:
        return self.priority < other.priority


TaskHandler = Callable[[WorkflowTask], Awaitable[Any]]


class TaskQueue:
    """
    Priority-based Task Queue managing background execution of workflow steps,
    retry management, and concurrency control.
    """

    def __init__(self, concurrency: int = 5):
        self.concurrency = concurrency
        self._queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self._handlers: Dict[str, TaskHandler] = {}
        self._active_tasks: Dict[str, WorkflowTask] = {}
        self._workers: List[asyncio.Task] = []
        self._running: bool = False

    def register_handler(self, step_name: str, handler: TaskHandler) -> None:
        """Register worker task handler for a specific workflow step."""
        self._handlers[step_name] = handler
        logger.info(f"[TaskQueue] Registered handler for step '{step_name}'")

    async def enqueue(self, task: WorkflowTask) -> None:
        """Enqueue task into priority queue."""
        await self._queue.put((task.priority, task))
        logger.info(f"[TaskQueue] Enqueued task '{task.task_id}' for step '{task.step_name}' (Priority {task.priority})")

    async def start_workers(self) -> None:
        """Start background worker pool."""
        if self._running:
            return
        self._running = True
        for i in range(self.concurrency):
            worker_task = asyncio.create_task(self._worker_loop(i))
            self._workers.append(worker_task)
        logger.info(f"[TaskQueue] Started {self.concurrency} background task workers.")

    async def stop_workers(self) -> None:
        """Stop background worker pool gracefully."""
        self._running = False
        for w in self._workers:
            w.cancel()
        await asyncio.gather(*self._workers, return_exceptions=True)
        self._workers.clear()
        logger.info("[TaskQueue] Stopped task workers.")

    async def _worker_loop(self, worker_id: int) -> None:
        while self._running:
            try:
                priority, task = await self._queue.get()
                self._active_tasks[task.task_id] = task
                logger.debug(f"[TaskQueue Worker {worker_id}] Processing task {task.task_id} [{task.step_name}]")

                handler = self._handlers.get(task.step_name)
                if handler:
                    await handler(task)
                else:
                    logger.warning(f"[TaskQueue] No handler registered for step '{task.step_name}'")

                self._queue.task_done()
                self._active_tasks.pop(task.task_id, None)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"[TaskQueue Worker {worker_id}] Task execution error: {str(e)}")

    def get_pending_count(self) -> int:
        return self._queue.qsize()

    def get_active_count(self) -> int:
        return len(self._active_tasks)


# Global TaskQueue Singleton
global_task_queue = TaskQueue()
