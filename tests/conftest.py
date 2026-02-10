from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel

from app.main import app
from tests.utils.database import create_test_engine


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function", autouse=False)
def db_session() -> Generator[Session, None, None]:
    """Create a test database session.

    Creates a new in-memory database for each test function.
    """
    # Import models to ensure they're registered
    from app.models import user  # noqa: F401, F811  # type: ignore[reportUnusedImport]

    # Create test engine using utility
    engine = create_test_engine()

    # Create all tables
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    # Clean up
    engine.dispose()
