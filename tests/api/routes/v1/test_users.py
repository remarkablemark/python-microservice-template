"""Tests for user endpoints."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from tests.utils.app_factory import create_test_app_with_database


def create_test_user(
    client: TestClient,
    email: str,
    username: str,
    full_name: str,
    is_active: bool = True,
) -> dict[str, object]:
    """Helper function to create a test user.

    Args:
        client: TestClient instance
        email: User email address
        username: Username
        full_name: Full name
        is_active: Whether user is active (default: True)

    Returns:
        JSON response data from user creation
    """
    response = client.post(
        "/v1/users/",
        json={
            "email": email,
            "username": username,
            "full_name": full_name,
            "is_active": is_active,
        },
    )
    return response.json()


@pytest.fixture
def client_with_db(db_session: Session) -> Generator[TestClient, None, None]:
    """Test client with database enabled."""
    from app.api.routes.v1 import users

    # Create test app with database and users router
    test_app = create_test_app_with_database(
        db_session, include_routers=[(users.router, {"prefix": "/v1"})]
    )

    yield TestClient(test_app)
    test_app.dependency_overrides.clear()


def test_create_user(client_with_db: TestClient) -> None:
    """Test creating a new user."""
    response = client_with_db.post(
        "/v1/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "is_active": True,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert data["full_name"] == "Test User"
    assert data["is_active"] is True
    assert "id" in data


@pytest.mark.parametrize(
    ("first_email", "first_username", "second_email", "second_username"),
    [
        # Duplicate email
        ("duplicate@example.com", "user1", "duplicate@example.com", "user2"),
        # Duplicate username
        ("user1@example.com", "duplicateuser", "user2@example.com", "duplicateuser"),
    ],
    ids=["duplicate_email", "duplicate_username"],
)
def test_create_duplicate_user(
    client_with_db: TestClient,
    first_email: str,
    first_username: str,
    second_email: str,
    second_username: str,
) -> None:
    """Test creating a user with duplicate email or username."""
    # Create first user
    create_test_user(client_with_db, first_email, first_username, "User One")

    # Try to create user with duplicate field
    response = client_with_db.post(
        "/v1/users/",
        json={
            "email": second_email,
            "username": second_username,
            "full_name": "User Two",
        },
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_get_user(client_with_db: TestClient) -> None:
    """Test getting a user by ID."""
    # Create user
    user_data = create_test_user(
        client_with_db, "getuser@example.com", "getuser", "Get User"
    )
    user_id = user_data["id"]

    # Get user
    response = client_with_db.get(f"/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == "getuser@example.com"


def test_get_nonexistent_user(client_with_db: TestClient) -> None:
    """Test getting a user that doesn't exist."""
    response = client_with_db.get("/v1/users/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_list_users(client_with_db: TestClient) -> None:
    """Test listing all users."""
    # Create multiple users
    for i in range(1, 4):
        create_test_user(
            client_with_db, f"user{i}@example.com", f"user{i}", f"User {i}"
        )

    # List users
    response = client_with_db.get("/v1/users/")
    assert response.status_code == 200
    data: list[dict[str, object]] = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3


def test_list_users_with_pagination(client_with_db: TestClient) -> None:
    """Test listing users with pagination."""
    # Create multiple users
    for i in range(5):
        create_test_user(
            client_with_db, f"page{i}@example.com", f"pageuser{i}", f"Page User {i}"
        )

    # Test skip and limit
    response = client_with_db.get("/v1/users/?skip=2&limit=2")
    assert response.status_code == 200
    data: list[dict[str, object]] = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
