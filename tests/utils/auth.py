"""Auth test utilities for managing authentication tokens in tests."""

from collections.abc import Generator
from contextlib import contextmanager
from typing import Any


@contextmanager
def temporary_valid_tokens(
    auth_module: Any, tokens: set[str] | None
) -> Generator[None, None, None]:
    """
    Context manager that temporarily overrides VALID_API_KEYS.

    Args:
        auth_module: The module containing VALID_API_KEYS to override (e.g., app.core.auth)
        tokens: Set of tokens to use, or None to clear all tokens

    Yields:
        None

    Example:
        with temporary_valid_tokens(auth, {"test-token"}):
            # ... run tests with authentication enabled ...

        with temporary_valid_tokens(auth, None):
            # ... run tests with authentication disabled ...
    """
    original_tokens = auth_module.VALID_API_KEYS.copy()

    try:
        auth_module.VALID_API_KEYS.clear()
        if tokens is not None:
            auth_module.VALID_API_KEYS.update(tokens)
        yield
    finally:
        auth_module.VALID_API_KEYS.clear()
        auth_module.VALID_API_KEYS.update(original_tokens)


def create_auth_header(token: str) -> dict[str, str]:
    """
    Generate an Authorization header dictionary for Bearer token authentication.

    Args:
        token: The bearer token to include

    Returns:
        Dictionary with Authorization header in format {"Authorization": "Bearer <token>"}

    Example:
        headers = create_auth_header("my-token")
        response = client.get("/protected", headers=headers)
    """
    return {"Authorization": f"Bearer {token}"}
