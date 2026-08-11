from typing import Any
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base declarative class for all SQLAlchemy models."""
    id: Any
