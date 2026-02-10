"""Test app factory utilities for creating FastAPI test applications."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import APIRouter, FastAPI
from sqlmodel import Session


def create_test_app_with_database(
    db_session: Session,
    include_routers: list[tuple[APIRouter, dict[str, Any]]] | None = None,
) -> FastAPI:
    """
    Create a FastAPI test app with database session dependency override.

    Args:
        db_session: Database session to inject into the app
        include_routers: Optional list of (router, kwargs) tuples to include

    Returns:
        FastAPI app instance with database configured

    Example:
        app = create_test_app_with_database(
            session,
            include_routers=[(users_router, {"prefix": "/users", "tags": ["users"]})]
        )
    """
    from app.core.database import get_session

    app = FastAPI()

    # Override database session dependency
    def get_session_override() -> Session:
        return db_session

    app.dependency_overrides[get_session] = get_session_override

    # Include routers if provided
    if include_routers:
        for router, kwargs in include_routers:
            app.include_router(router, **kwargs)

    return app


def create_test_app_with_lifespan(
    lifespan_context: Any,
    include_routers: list[tuple[APIRouter, dict[str, Any]]] | None = None,
) -> FastAPI:
    """
    Create a FastAPI test app with custom lifespan context manager.

    Args:
        lifespan_context: Async context manager function for app lifespan
        include_routers: Optional list of (router, kwargs) tuples to include

    Returns:
        FastAPI app instance with custom lifespan

    Example:
        @asynccontextmanager
        async def test_lifespan(app: FastAPI):
            # startup logic
            yield
            # shutdown logic

        app = create_test_app_with_lifespan(test_lifespan)
    """
    app = FastAPI(lifespan=lifespan_context)

    # Include routers if provided
    if include_routers:
        for router, kwargs in include_routers:
            app.include_router(router, **kwargs)

    return app


@asynccontextmanager
async def empty_lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Empty lifespan context manager for testing.

    This is useful when you want to test app behavior without any startup/shutdown logic.

    Args:
        _app: FastAPI application instance (unused)

    Yields:
        None
    """
    yield
