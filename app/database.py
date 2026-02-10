"""Optional database configuration.

Database is enabled when DATABASE_URL environment variable is set.
"""

import os
from collections.abc import Generator

from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine

# Optional: Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Database is optional - only initialize if DATABASE_URL is set
engine: Engine | None = None
if DATABASE_URL:
    # Create engine with appropriate settings
    connect_args = {}
    if DATABASE_URL.startswith("sqlite"):
        # SQLite-specific settings
        connect_args = {"check_same_thread": False}

    engine = create_engine(
        DATABASE_URL,
        echo=os.getenv("DATABASE_ECHO", "").lower() == "true",
        connect_args=connect_args,
    )


def create_db_and_tables() -> None:
    """Create database tables if database is enabled."""
    if engine is not None:
        SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Dependency to get database session.

    Yields:
        Database session if database is enabled, None otherwise.

    Raises:
        RuntimeError: If database is not configured.
    """
    if engine is None:
        raise RuntimeError(
            "Database not configured. Set DATABASE_URL environment variable."
        )

    with Session(engine) as session:
        yield session
