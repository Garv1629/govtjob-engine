import hashlib
from datetime import datetime, timezone


def generate_content_hash(organization: str, advt_number: str, title: str) -> str:
    """Generates unique content hash for job notification deduplication."""
    raw = f"{organization.strip().upper()}:{advt_number.strip().upper()}:{title.strip().upper()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def get_utc_now() -> datetime:
    """Returns current UTC timestamp with timezone awareness."""
    return datetime.now(timezone.utc)
