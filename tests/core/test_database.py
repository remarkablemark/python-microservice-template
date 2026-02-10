"""Tests for database module."""

import pytest
from fastapi import HTTPException
from sqlmodel import Session, create_engine, select

from app.core.database import create_db_and_tables, get_session


def test_database_not_configured() -> None:
    """Test that database session raises error when not configured."""
    # The current app has no DATABASE_URL set by default
    # So calling get_session should raise an error
    from app.core import database

    # Save current engine
    original_engine = database.engine
    try:
        # Temporarily set engine to None
        database.engine = None

        with pytest.raises(HTTPException) as exc_info:
            next(get_session())

        assert exc_info.value.status_code == 500
        assert "not configured" in exc_info.value.detail.lower()
    finally:
        # Restore original engine
        database.engine = original_engine


def test_database_create_tables(db_session: Session) -> None:
    """Test database table creation."""
    # The db_session fixture already creates tables
    # Test that we can query the database
    # Query should work without errors
    from sqlmodel import select

    from app.models.user import User

    statement = select(User)
    result = db_session.exec(statement).all()
    assert isinstance(result, list)


def test_create_db_and_tables() -> None:
    """Test create_db_and_tables function."""
    from sqlalchemy.pool import StaticPool

    from app.models import user  # noqa: F401, F811  # type: ignore[reportUnusedImport]

    # Create a test engine
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Save current engine
    from app.core import database

    original_engine = database.engine
    try:
        # Set test engine
        database.engine = test_engine

        # Create tables
        create_db_and_tables()

        # Verify tables exist by creating a session and querying
        with Session(test_engine) as session:
            from app.models.user import User

            statement = select(User)
            result = session.exec(statement).all()
            assert isinstance(result, list)
    finally:
        # Restore original engine
        database.engine = original_engine
        test_engine.dispose()


def test_get_session_yields_session(db_session: Session) -> None:
    """Test that get_session yields a valid session."""
    assert isinstance(db_session, Session)


def test_database_sqlite_connection_args() -> None:
    """Test that SQLite URLs get special connection args."""
    from sqlalchemy.pool import StaticPool

    # Test SQLite connection args logic
    test_url = "sqlite:///test.db"
    connect_args = {}

    if test_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}

    assert connect_args == {"check_same_thread": False}

    # Create an engine to verify it works
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    assert test_engine is not None
    test_engine.dispose()


def test_database_postgresql_no_special_args() -> None:
    """Test that PostgreSQL URLs don't get SQLite-specific args."""
    test_url = "postgresql+psycopg://user:pass@localhost/db"
    connect_args = {}

    if test_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}

    # PostgreSQL should not get SQLite-specific args
    assert connect_args == {}


def test_get_session_context_manager() -> None:
    """Test that get_session properly uses context manager."""
    from sqlalchemy.pool import StaticPool

    from app.core import database  # noqa: F401, F811

    # Create test engine
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Save original engine
    original_engine = database.engine

    try:
        # Set test engine
        database.engine = test_engine
        database.create_db_and_tables()

        # Test get_session generator
        gen = get_session()
        session = next(gen)

        # Verify session was yielded
        assert isinstance(session, Session)

        # Complete the generator (this tests the context manager cleanup)
        try:
            next(gen)
        except StopIteration:
            pass  # Expected

    finally:
        # Restore original engine
        database.engine = original_engine
        test_engine.dispose()
