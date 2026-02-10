"""Optional database configuration.

Database is enabled when DATABASE_URL environment variable is set.
"""

from collections.abc import Generator

from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine

from app.core.env import get_env_bool, get_env_str
from app.core.exceptions import internal_server_exception

# Optional: Get database URL from environment
DATABASE_URL = get_env_str("DATABASE_URL")

# Database is optional - only initialize if DATABASE_URL is set
engine: Engine | None = None
if DATABASE_URL:  # pragma: no cover
    # Create engine with appropriate settings
    connect_args = {}
    if DATABASE_URL.startswith("sqlite"):
        # SQLite-specific settings
        connect_args = {"check_same_thread": False}

    engine = create_engine(
        DATABASE_URL,
        echo=get_env_bool("DATABASE_ECHO"),
        connect_args=connect_args,
    )


def create_db_and_tables() -> None:
    """Create database tables if database is enabled."""
    if engine is not None:
        SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Dependency to get database session.

    Yields:
        Database session if database is enabled.

    Raises:
        HTTPException: If database is not configured.
    """
    if engine is None:
        raise internal_server_exception(
            "Database not configured. Set DATABASE_URL environment variable."
        )

    with Session(engine) as session:
        yield session
