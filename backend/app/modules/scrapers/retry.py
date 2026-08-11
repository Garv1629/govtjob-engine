import asyncio
from typing import Callable, Any, TypeVar
from app.core.logging import logger

T = TypeVar("T")


async def execute_with_retry(
    func: Callable[[], Any],
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    source_code: str = "SYSTEM"
) -> T:
    """
    Executes an asynchronous function with exponential backoff retry logic.
    """
    delay = initial_delay
    last_exception = None

    for attempt in range(1, max_retries + 1):
        try:
            return await func()
        except Exception as e:
            last_exception = e
            logger.warning(
                f"[{source_code}] Retry Attempt {attempt}/{max_retries} failed with error: {str(e)}. Retrying in {delay:.2f}s..."
            )
            if attempt < max_retries:
                await asyncio.sleep(delay)
                delay *= backoff_factor

    logger.error(f"[{source_code}] All {max_retries} retry attempts exhausted.")
    raise last_exception
