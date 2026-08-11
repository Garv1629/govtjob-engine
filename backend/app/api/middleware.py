import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import logger


class LoggingAndTimingMiddleware(BaseHTTPMiddleware):
    """Middleware for measuring API latency and logging incoming HTTP requests."""

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()
        path = request.url.path
        method = request.method

        logger.info(f"Incoming Request: {method} {path}")

        try:
            response = await call_next(request)
            process_time = (time.time() - start_time) * 1000
            response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"
            logger.info(f"Completed Request: {method} {path} - Status {response.status_code} in {process_time:.2f}ms")
            return response
        except Exception as exc:
            process_time = (time.time() - start_time) * 1000
            logger.error(f"Unhandled Request Error: {method} {path} - {str(exc)} after {process_time:.2f}ms")
            raise exc
