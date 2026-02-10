"""Tests for HTTP exception factories."""

from fastapi import status

from app.core.exceptions import (
    bad_request_exception,
    forbidden_exception,
    internal_server_exception,
    not_found_exception,
    unauthorized_exception,
)


def test_not_found_exception() -> None:
    """Test not_found_exception creates 404 error."""
    exc = not_found_exception("User", 123)

    assert exc.status_code == status.HTTP_404_NOT_FOUND
    assert "User 123 not found" in exc.detail


def test_not_found_exception_string_id() -> None:
    """Test not_found_exception with string identifier."""
    exc = not_found_exception("Resource", "abc-123")

    assert exc.status_code == status.HTTP_404_NOT_FOUND
    assert "Resource abc-123 not found" in exc.detail


def test_bad_request_exception() -> None:
    """Test bad_request_exception creates 400 error."""
    exc = bad_request_exception("Invalid input")

    assert exc.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.detail == "Invalid input"


def test_unauthorized_exception_default() -> None:
    """Test unauthorized_exception creates 401 error with default message."""
    exc = unauthorized_exception()

    assert exc.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Missing or invalid bearer token" in exc.detail
    assert exc.headers == {"WWW-Authenticate": "Bearer"}


def test_unauthorized_exception_custom_message() -> None:
    """Test unauthorized_exception with custom message."""
    exc = unauthorized_exception("Custom auth error")

    assert exc.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.detail == "Custom auth error"
    assert exc.headers == {"WWW-Authenticate": "Bearer"}


def test_forbidden_exception_default() -> None:
    """Test forbidden_exception creates 403 error with default message."""
    exc = forbidden_exception()

    assert exc.status_code == status.HTTP_403_FORBIDDEN
    assert "Invalid bearer token" in exc.detail


def test_forbidden_exception_custom_message() -> None:
    """Test forbidden_exception with custom message."""
    exc = forbidden_exception("Access denied")

    assert exc.status_code == status.HTTP_403_FORBIDDEN
    assert exc.detail == "Access denied"


def test_internal_server_exception() -> None:
    """Test internal_server_exception creates 500 error."""
    exc = internal_server_exception("Database not configured")

    assert exc.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert exc.detail == "Database not configured"
