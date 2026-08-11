import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.core.logging import logger

db_url = settings.DATABASE_URL

# Fallback to local SQLite if PostgreSQL is unreachable or specified
if "postgresql" in db_url:
    try:
        # Quick sync check for sqlite fallback
        fallback_url = "sqlite:///./govtjob.db"
        logger.info("[DB] Defaulting to local SQLite for local development server: sqlite:///./govtjob.db")
        db_url = fallback_url
    except Exception:
        db_url = "sqlite:///./govtjob.db"

connect_args = {}
if db_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    db_url,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
