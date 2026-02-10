"""Tests for database utilities."""

import pytest
from fastapi import HTTPException
from sqlmodel import Session

from app.core.db_utils import exists_by_field, get_by_id_or_404
from app.models.user import User


def test_get_by_id_or_404_found(db_session: Session) -> None:
    """Test get_by_id_or_404 returns record when found."""
    # Create a user
    user = User(
        email="test@example.com",
        username="testuser",
        full_name="Test User",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Get the user
    assert user.id is not None
    found_user = get_by_id_or_404(db_session, User, user.id, "User")
    assert found_user.id == user.id
    assert found_user.email == "test@example.com"


def test_get_by_id_or_404_not_found(db_session: Session) -> None:
    """Test get_by_id_or_404 raises 404 when not found."""
    with pytest.raises(HTTPException) as exc_info:
        get_by_id_or_404(db_session, User, 99999, "User")

    assert exc_info.value.status_code == 404
    assert "User 99999 not found" in exc_info.value.detail


def test_get_by_id_or_404_default_resource_name(db_session: Session) -> None:
    """Test get_by_id_or_404 uses model name when resource_name not provided."""
    with pytest.raises(HTTPException) as exc_info:
        get_by_id_or_404(db_session, User, 99999)

    assert exc_info.value.status_code == 404
    assert "User 99999 not found" in exc_info.value.detail


def test_exists_by_field_true(db_session: Session) -> None:
    """Test exists_by_field returns True when record exists."""
    # Create a user
    user = User(
        email="exists@example.com",
        username="existsuser",
        full_name="Exists User",
    )
    db_session.add(user)
    db_session.commit()

    # Check if user exists by email
    assert exists_by_field(db_session, User, "email", "exists@example.com") is True
    assert exists_by_field(db_session, User, "username", "existsuser") is True


def test_exists_by_field_false(db_session: Session) -> None:
    """Test exists_by_field returns False when record does not exist."""
    assert (
        exists_by_field(db_session, User, "email", "nonexistent@example.com") is False
    )
    assert exists_by_field(db_session, User, "username", "nonexistent") is False
