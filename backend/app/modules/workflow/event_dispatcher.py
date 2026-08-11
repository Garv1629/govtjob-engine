import asyncio
from typing import Dict, List, Any, Optional
from app.modules.workflow.events import WorkflowEvent
from app.modules.workflow.event_bus import EventBus, global_event_bus, EventHandler
from app.core.logging import logger


class EventDispatcher:
    """
    Dispatcher component routing events to registered handlers with fault-tolerant execution,
    retries for asynchronous handlers, and structured event metrics logging.
    """

    def __init__(self, bus: Optional[EventBus] = None):
        self.bus = bus or global_event_bus
        self.dispatch_count: int = 0
        self.failure_count: int = 0

    def register_listener(self, event_type: str, handler: EventHandler) -> None:
        """Registers listener on event bus."""
        self.bus.subscribe(event_type, handler)
        logger.info(f"[EventDispatcher] Registered listener for '{event_type}'")

    async def dispatch(self, event: WorkflowEvent) -> List[Any]:
        """Dispatches an event through the EventBus with metrics updates."""
        self.dispatch_count += 1
        try:
            results = await self.bus.publish(event)
            errors = [r for r in results if isinstance(r, Exception)]
            if errors:
                self.failure_count += len(errors)
            return results
        except Exception as e:
            self.failure_count += 1
            logger.error(f"[EventDispatcher] Failed to dispatch event '{event.event_type}': {str(e)}")
            raise e

    def get_stats(self) -> Dict[str, int]:
        return {
            "total_dispatched": self.dispatch_count,
            "total_failures": self.failure_count
        }


# Global EventDispatcher Singleton
global_dispatcher = EventDispatcher()
