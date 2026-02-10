"""Database test utilities for managing test database engines and sessions."""

from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

from sqlmodel import Session, SQLModel, create_engine


def create_test_engine() -> Any:
    """
    Create a test SQLite engine with standard test configuration.

    Returns:
        Engine configured for in-memory SQLite database with:
        - connect_args for check_same_thread=False
        - poolclass=StaticPool for connection pooling
    """
    from sqlalchemy.pool import StaticPool

    return create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


@contextmanager
def temporary_test_engine(
    database_module: Any,
) -> Generator[Any, None, None]:
    """
    Context manager that temporarily overrides a database module's engine.

    Args:
        database_module: The module containing the engine to override (e.g., app.core.database)

    Yields:
        The temporary test engine

    Example:
        with temporary_test_engine(database) as engine:
            SQLModel.metadata.create_all(engine)
            # ... run tests ...
    """
    original_engine = database_module.engine
    test_engine = create_test_engine()

    try:
        database_module.engine = test_engine
        SQLModel.metadata.create_all(test_engine)
        yield test_engine
    finally:
        database_module.engine = original_engine
        if test_engine is not None:
            SQLModel.metadata.drop_all(test_engine)
            test_engine.dispose()


def get_test_session(engine: Any) -> Generator[Session, None, None]:
    """
    Create a test database session from an engine.

    Args:
        engine: SQLAlchemy engine to create session from

    Yields:
        SQLModel Session instance
    """
    with Session(engine) as session:
        yield session
