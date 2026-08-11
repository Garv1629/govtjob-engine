import time
import uuid
from typing import Dict, Tuple
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.core.logging import logger, audit_logger


class RateLimiter:
    """In-memory IP rate limiter enforcing request thresholds per minute."""

    def __init__(self, requests_per_minute: int = 120):
        self.requests_per_minute = requests_per_minute
        self.clients: Dict[str, Tuple[int, float]] = {}  # ip -> (count, window_start_time)

    def is_rate_limited(self, client_ip: str) -> bool:
        now = time.time()
        if client_ip not in self.clients:
            self.clients[client_ip] = (1, now)
            return False

        count, window_start = self.clients[client_ip]
        if now - window_start > 60.0:
            # Reset window
            self.clients[client_ip] = (1, now)
            return False

        if count >= self.requests_per_minute:
            return True

        self.clients[client_ip] = (count + 1, window_start)
        return False


rate_limiter = RateLimiter(requests_per_minute=settings.RATE_LIMIT_PER_MINUTE)


class SecurityAndLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware enforcing security headers, IP rate limiting, and structured request logging."""

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()
        request_id = str(uuid.uuid4())
        client_ip = request.client.host if request.client else "127.0.0.1"

        # Rate Limiting Check
        if settings.RATE_LIMIT_PER_MINUTE > 0 and rate_limiter.is_rate_limited(client_ip):
            logger.warning(
                f"Rate limit exceeded for IP {client_ip} on path {request.url.path}",
                extra={"request_id": request_id, "user_id": client_ip, "status_code": 429}
            )
            audit_logger.log_event("RATE_LIMIT", client_ip, "API_CALL", request.url.path, "REJECTED", {"reason": "Quota Exceeded"})
            return Response(
                content='{"error": "Too Many Requests", "message": "Rate limit exceeded. Please wait a minute."}',
                status_code=429,
                media_type="application/json"
            )

        # Process Request
        response: Response = await call_next(request)
        duration_ms = round((time.time() - start_time) * 1000, 2)

        # Inject Security Headers
        if settings.SECURITY_HEADERS_ENABLED:
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
            response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none';"
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
            response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        # Log Request Telemetry
        logger.info(
            f"HTTP {request.method} {request.url.path} -> {response.status_code} ({duration_ms}ms)",
            extra={
                "request_id": request_id,
                "user_id": client_ip,
                "duration_ms": duration_ms,
                "status_code": response.status_code
            }
        )

        return response
