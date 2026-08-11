from typing import Generator
from sqlalchemy.orm import Session
from app.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """FastAPI Dependency for database session lifecycle management."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
