import asyncio
import inspect
from typing import Dict, List, Callable, Awaitable, Union, Any, Type, Optional
from collections import deque
from app.modules.workflow.events import WorkflowEvent
from app.core.logging import logger

EventHandler = Callable[[WorkflowEvent], Union[None, Awaitable[None]]]


class EventBus:
    """
    Asynchronous event bus supporting strongly-typed event dispatching, wildcard listeners,
    and event log auditing.
    """

    def __init__(self, max_history: int = 1000):
        self._handlers: Dict[str, List[EventHandler]] = {}
        self._event_history: deque = deque(maxlen=max_history)
        self._lock = asyncio.Lock()

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        """Subscribe a handler to a specific event type or wildcard '*'."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        if handler not in self._handlers[event_type]:
            self._handlers[event_type].append(handler)
            logger.debug(f"[EventBus] Registered handler '{handler.__name__}' for event type '{event_type}'")

    def unsubscribe(self, event_type: str, handler: EventHandler) -> bool:
        """Unsubscribe a handler from an event type."""
        if event_type in self._handlers and handler in self._handlers[event_type]:
            self._handlers[event_type].remove(handler)
            return True
        return False

    async def publish(self, event: WorkflowEvent) -> List[Any]:
        """
        Publishes an event to all subscribed listeners (type match and wildcard '*').
        Executes handlers concurrently and captures results/exceptions.
        """
        async with self._lock:
            self._event_history.append(event)

        logger.info(f"[EventBus] Published Event: {event.event_type} (Workflow ID: {event.workflow_id})")

        listeners = list(self._handlers.get(event.event_type, []))
        wildcard_listeners = list(self._handlers.get("*", []))
        all_listeners = listeners + [l for l in wildcard_listeners if l not in listeners]

        if not all_listeners:
            logger.debug(f"[EventBus] No registered listeners for event '{event.event_type}'")
            return []

        tasks = []
        for handler in all_listeners:
            tasks.append(self._execute_handler(handler, event))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        for idx, res in enumerate(results):
            if isinstance(res, Exception):
                logger.error(
                    f"[EventBus] Error executing handler '{all_listeners[idx].__name__}' for event '{event.event_type}': {str(res)}"
                )
        return results

    async def _execute_handler(self, handler: EventHandler, event: WorkflowEvent) -> Any:
        try:
            if inspect.iscoroutinefunction(handler):
                return await handler(event)
            else:
                return handler(event)
        except Exception as e:
            logger.error(f"[EventBus] Exception in listener {handler.__name__}: {str(e)}")
            raise e

    def get_event_history(self, workflow_id: Optional[str] = None) -> List[WorkflowEvent]:
        events = list(self._event_history)
        if workflow_id:
            return [e for e in events if e.workflow_id == workflow_id]
        return events

    def clear(self) -> None:
        self._handlers.clear()
        self._event_history.clear()


# Global EventBus Singleton
global_event_bus = EventBus()
