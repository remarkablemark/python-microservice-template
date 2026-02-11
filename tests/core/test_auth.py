"""Tests for authentication module."""

from collections.abc import Generator

import pytest
from fastapi import FastAPI, HTTPException, Request
from fastapi.testclient import TestClient

from tests.utils.auth import create_auth_header, temporary_valid_tokens


@pytest.fixture
def client_with_auth() -> Generator[TestClient, None, None]:
    """Test client with authentication enabled."""
    from app.api.routes.v1 import protected
    from app.core import auth

    with temporary_valid_tokens(auth, {"test-token-123", "another-token"}):
        # Create test app
        test_app = FastAPI()
        test_app.include_router(protected.router, prefix="/v1")

        yield TestClient(test_app)


@pytest.fixture
def client_without_auth() -> Generator[TestClient, None, None]:
    """Test client without authentication configured."""
    from app.core import auth

    with temporary_valid_tokens(auth, None):
        # Create test app without protected router (since auth is disabled)
        test_app = FastAPI()

        yield TestClient(test_app)


def test_protected_endpoint_with_valid_token(client_with_auth: TestClient) -> None:
    """Test protected endpoint with valid bearer token."""
    response = client_with_auth.get(
        "/v1/protected/", headers=create_auth_header("test-token-123")
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Access granted"
    assert data["authenticated"] == "true"


def test_protected_endpoint_with_second_valid_token(
    client_with_auth: TestClient,
) -> None:
    """Test protected endpoint with second valid bearer token."""
    response = client_with_auth.get(
        "/v1/protected/", headers=create_auth_header("another-token")
    )
    assert response.status_code == 200
    assert response.json()["authenticated"] == "true"


def test_protected_endpoint_without_token(client_with_auth: TestClient) -> None:
    """Test protected endpoint without bearer token."""
    response = client_with_auth.get("/v1/protected/")
    assert response.status_code == 401
    detail = response.json()["detail"]
    assert "bearer token" in detail.lower() or "authorization" in detail.lower()


def test_protected_endpoint_with_invalid_token(client_with_auth: TestClient) -> None:
    """Test protected endpoint with invalid bearer token."""
    response = client_with_auth.get(
        "/v1/protected/", headers=create_auth_header("invalid-token")
    )
    assert response.status_code == 403
    assert "Invalid bearer token" in response.json()["detail"]


def test_protected_endpoint_with_malformed_header(
    client_with_auth: TestClient,
) -> None:
    """Test protected endpoint with malformed authorization header."""
    response = client_with_auth.get(
        "/v1/protected/", headers={"Authorization": "InvalidFormat"}
    )
    assert response.status_code == 401


def test_protected_data_endpoint(client_with_auth: TestClient) -> None:
    """Test protected data endpoint."""
    response = client_with_auth.get(
        "/v1/protected/data", headers=create_auth_header("test-token-123")
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "This is protected data"
    assert data["data"] == ["item1", "item2", "item3"]
    assert "token_preview" in data
    assert data["token_preview"] == "test-tok..."


def test_protected_endpoint_not_available_without_auth_config(
    client_without_auth: TestClient,
) -> None:
    """Test that protected endpoints are not available when auth is not configured."""
    response = client_without_auth.get("/v1/protected/")
    assert response.status_code == 404


def test_auth_not_configured_error() -> None:
    """Test authentication error when tokens are not configured."""
    from app.core import auth

    with temporary_valid_tokens(auth, None):
        # Create a mock request (minimal scope dict for Request)
        scope = {
            "type": "http",
            "headers": [(b"authorization", b"Bearer test")],
            "method": "GET",
            "path": "/",
            "query_string": b"",
        }
        mock_request = Request(scope)

        with pytest.raises(HTTPException) as exc_info:
            auth.get_api_token(mock_request)  # type: ignore[reportArgumentType]

        assert exc_info.value.status_code == 500
        assert "not configured" in exc_info.value.detail


def test_is_auth_enabled() -> None:
    """Test is_auth_enabled function."""
    from app.core import auth

    # Test with tokens
    with temporary_valid_tokens(auth, {"test-token"}):
        assert auth.is_auth_enabled() is True

    # Test without tokens
    with temporary_valid_tokens(auth, None):
        assert auth.is_auth_enabled() is False
