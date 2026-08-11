from datetime import datetime, timezone
from typing import List, Dict, Any
from app.core.logging import logger


class AutomationAuditLogger:
    """Records granular event audit trails for every browser action."""

    def __init__(self):
        self.logs: List[Dict[str, Any]] = []

    def log_event(self, event_type: str, message: str, details: Dict[str, Any] = None):
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "message": message,
            "details": details or {}
        }
        self.logs.append(entry)
        logger.info(f"[AUTOMATION AUDIT] [{event_type}] {message}")

    def get_logs() -> List[Dict[str, Any]]:
        return self.logs
