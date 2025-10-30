from __future__ import annotations

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

# Note: For demo purposes we default to a local SQLite file.
# Use environment variable NOTES_DB_URL to override (e.g., for testing).
DEFAULT_SQLITE_URL = "sqlite:///./notes.db"
DATABASE_URL = os.getenv("NOTES_DB_URL", DEFAULT_SQLITE_URL)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM models."""
    pass


# For SQLite, check_same_thread should be False for multithreaded FastAPI
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# PUBLIC_INTERFACE
def get_db() -> Generator[Session, None, None]:
    """Dependency that provides a SQLAlchemy Session to route handlers."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# PUBLIC_INTERFACE
def init_db() -> None:
    """Initialize database by creating all tables."""
    # Import models to ensure they are registered with Base before create_all
    from . import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
