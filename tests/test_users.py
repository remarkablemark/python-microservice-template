"""Tests for user endpoints."""

from collections.abc import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import Session


@pytest.fixture
def client_with_db(db_session: Session) -> Generator[TestClient, None, None]:
    """Test client with database enabled."""
    from app import database, users

    # Create a test app with users router included
    test_app = FastAPI()
    test_app.include_router(users.router)

    # Override get_session to use test session
    def get_test_session():
        yield db_session

    test_app.dependency_overrides[database.get_session] = get_test_session
    yield TestClient(test_app)
    test_app.dependency_overrides.clear()


def test_create_user(client_with_db: TestClient) -> None:
    """Test creating a new user."""
    response = client_with_db.post(
        "/users/",
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


def test_create_duplicate_user_email(client_with_db: TestClient) -> None:
    """Test creating a user with duplicate email."""
    # Create first user
    client_with_db.post(
        "/users/",
        json={
            "email": "duplicate@example.com",
            "username": "user1",
            "full_name": "User One",
        },
    )

    # Try to create user with same email
    response = client_with_db.post(
        "/users/",
        json={
            "email": "duplicate@example.com",
            "username": "user2",
            "full_name": "User Two",
        },
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_create_duplicate_user_username(client_with_db: TestClient) -> None:
    """Test creating a user with duplicate username."""
    # Create first user
    client_with_db.post(
        "/users/",
        json={
            "email": "user1@example.com",
            "username": "duplicateuser",
            "full_name": "User One",
        },
    )

    # Try to create user with same username
    response = client_with_db.post(
        "/users/",
        json={
            "email": "user2@example.com",
            "username": "duplicateuser",
            "full_name": "User Two",
        },
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_get_user(client_with_db: TestClient) -> None:
    """Test getting a user by ID."""
    # Create user
    create_response = client_with_db.post(
        "/users/",
        json={
            "email": "getuser@example.com",
            "username": "getuser",
            "full_name": "Get User",
        },
    )
    user_id = create_response.json()["id"]

    # Get user
    response = client_with_db.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == "getuser@example.com"


def test_get_nonexistent_user(client_with_db: TestClient) -> None:
    """Test getting a user that doesn't exist."""
    response = client_with_db.get("/users/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_list_users(client_with_db: TestClient) -> None:
    """Test listing all users."""
    # Create multiple users
    client_with_db.post(
        "/users/",
        json={"email": "user1@example.com", "username": "user1", "full_name": "User 1"},
    )
    client_with_db.post(
        "/users/",
        json={"email": "user2@example.com", "username": "user2", "full_name": "User 2"},
    )
    client_with_db.post(
        "/users/",
        json={"email": "user3@example.com", "username": "user3", "full_name": "User 3"},
    )

    # List users
    response = client_with_db.get("/users/")
    assert response.status_code == 200
    data: list[dict[str, object]] = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3


def test_list_users_with_pagination(client_with_db: TestClient) -> None:
    """Test listing users with pagination."""
    # Create multiple users
    for i in range(5):
        client_with_db.post(
            "/users/",
            json={
                "email": f"page{i}@example.com",
                "username": f"pageuser{i}",
                "full_name": f"Page User {i}",
            },
        )

    # Test skip and limit
    response = client_with_db.get("/users/?skip=2&limit=2")
    assert response.status_code == 200
    data: list[dict[str, object]] = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
