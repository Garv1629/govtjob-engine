import logging
import sys
import json
from datetime import datetime, timezone
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
from app.core.config import settings

# Create logs directory
LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"
AUDIT_LOG_FILE = LOG_DIR / "audit.log"


class StructuredJsonFormatter(logging.Formatter):
    """Formats log entries as structured JSON objects for OpenTelemetry & ELK ingestion."""

    def format(self, record: logging.LogRecord) -> str:
        log_object = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "line": record.lineno,
            "message": record.getMessage(),
            "environment": settings.APP_ENV,
        }

        # Include custom contextual attributes if present
        for key in ["request_id", "user_id", "workflow_id", "source_code", "duration_ms", "status_code"]:
            if hasattr(record, key):
                log_object[key] = getattr(record, key)

        if record.exc_info:
            log_object["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_object)


def setup_logging() -> logging.Logger:
    """Configures structured JSON logging for console and daily rotating file output."""
    logger = logging.getLogger("govtjob")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    logger.handlers.clear()

    json_formatter = StructuredJsonFormatter()

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(json_formatter)
    logger.addHandler(console_handler)

    # Daily Rotating App Log File
    file_handler = TimedRotatingFileHandler(
        filename=LOG_FILE,
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8"
    )
    file_handler.setFormatter(json_formatter)
    logger.addHandler(file_handler)

    return logger


logger = setup_logging()


class AuditLogger:
    """Specialized audit logger for recording critical user actions, security decisions, and system state changes."""

    def __init__(self):
        self.audit_logger = logging.getLogger("govtjob.audit")
        self.audit_logger.setLevel(logging.INFO)

        audit_handler = TimedRotatingFileHandler(
            filename=AUDIT_LOG_FILE,
            when="midnight",
            interval=1,
            backupCount=90,
            encoding="utf-8"
        )
        audit_handler.setFormatter(StructuredJsonFormatter())
        self.audit_logger.addHandler(audit_handler)

    def log_event(self, event_type: str, actor_id: str, action: str, resource_id: str, status: str, details: dict = None):
        extra = {
            "request_id": getattr(self, "request_id", "system"),
            "user_id": actor_id,
            "workflow_id": resource_id if "wf" in resource_id else None,
        }
        msg = f"[AUDIT] {event_type} | Actor: {actor_id} | Action: {action} | Resource: {resource_id} | Status: {status} | Details: {details or {}}"
        self.audit_logger.info(msg, extra=extra)


audit_logger = AuditLogger()
