from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.main import app


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function", autouse=False)
def db_session() -> Generator[Session, None, None]:
    """Create a test database session.

    Creates a new in-memory database for each test function.
    """
    from sqlalchemy.pool import StaticPool

    # Import models to ensure they're registered
    from app import models  # noqa: F401, F811  # type: ignore[reportUnusedImport]

    # Use in-memory SQLite with StaticPool to ensure single connection
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create all tables
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    # Clean up
    engine.dispose()
