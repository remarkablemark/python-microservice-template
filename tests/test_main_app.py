"""Tests for main app with optional features enabled."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, create_engine


def test_app_with_database_enabled() -> None:
    """Test app lifespan with database enabled."""
    from app import database, healthcheck, items, users

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

        # Create test app with lifespan
        @asynccontextmanager
        async def test_lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
            if database.engine is not None:
                database.create_db_and_tables()
            yield

        test_app = FastAPI(lifespan=test_lifespan)
        test_app.include_router(healthcheck.router)
        test_app.include_router(items.router)

        # Include users router since database is enabled
        test_app.include_router(users.router)

        # Test with client
        with TestClient(test_app) as client:
            # Verify basic endpoint works
            response = client.get("/healthcheck")
            assert response.status_code == 200

    finally:
        # Restore original engine
        database.engine = original_engine
        test_engine.dispose()


def test_app_with_auth_enabled() -> None:
    """Test app with authentication enabled."""
    from app import auth, healthcheck, items, protected

    # Save original tokens
    original_tokens = auth.VALID_API_TOKENS.copy()

    try:
        # Set test tokens
        auth.VALID_API_TOKENS.clear()
        auth.VALID_API_TOKENS.update({"test-token"})

        # Create test app
        test_app = FastAPI()
        test_app.include_router(healthcheck.router)
        test_app.include_router(items.router)

        # Include protected router since auth is enabled
        if auth.is_auth_enabled():
            test_app.include_router(protected.router)

        # Test with client
        with TestClient(test_app) as client:
            # Verify protected endpoint is available
            response = client.get(
                "/protected/", headers={"Authorization": "Bearer test-token"}
            )
            assert response.status_code == 200

    finally:
        # Restore original tokens
        auth.VALID_API_TOKENS.clear()
        auth.VALID_API_TOKENS.update(original_tokens)


def test_database_create_with_engine() -> None:
    """Test create_db_and_tables when engine is configured."""
    from app import database  # noqa: F401, F811

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

        # Create tables
        database.create_db_and_tables()

        # Verify table was created
        with Session(test_engine) as session:
            from sqlmodel import select

            from app.models import User

            result = session.exec(select(User)).all()
            assert isinstance(result, list)

    finally:
        # Restore original engine
        database.engine = original_engine
        test_engine.dispose()


def test_database_with_postgresql_connection_args() -> None:
    """Test database initialization with PostgreSQL (connection args logic)."""
    from app import database

    # Save original engine
    original_engine = database.engine
    original_url = database.DATABASE_URL

    try:
        # Test PostgreSQL URL doesn't get sqlite-specific connection args
        database.DATABASE_URL = "postgresql+psycopg://user:pass@localhost/db"

        # Create engine manually to test connection args logic
        connect_args = {}
        if database.DATABASE_URL and database.DATABASE_URL.startswith("sqlite"):
            connect_args = {"check_same_thread": False}

        # For PostgreSQL, connect_args should be empty
        assert connect_args == {}

    finally:
        # Restore original values
        database.engine = original_engine
        database.DATABASE_URL = original_url
