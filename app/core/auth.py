"""Bearer token authentication.

Provides bearer token-based authentication via Authorization header.
"""

from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.env import get_env_list
from app.core.exceptions import (
    forbidden_exception,
    internal_server_exception,
    unauthorized_exception,
)

# Bearer token security scheme
bearer_scheme = HTTPBearer(auto_error=False)

# Load API tokens from environment
# Supports multiple tokens separated by commas
VALID_API_KEYS = set(get_env_list("API_KEYS"))


def get_api_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    """Validate bearer token from Authorization header.

    Args:
        credentials: Bearer token credentials from Authorization header.

    Returns:
        The validated token.

    Raises:
        HTTPException: If token is missing or invalid.
    """
    # If no tokens are configured, authentication is disabled
    if not VALID_API_KEYS:
        raise internal_server_exception("Bearer token authentication is not configured")

    if not credentials:
        raise unauthorized_exception("Missing bearer token")

    if credentials.credentials not in VALID_API_KEYS:
        raise forbidden_exception("Invalid bearer token")

    return credentials.credentials


# Type alias for dependency injection
BearerToken = Annotated[str, Depends(get_api_token)]


def is_auth_enabled() -> bool:
    """Check if bearer token authentication is enabled.

    Returns:
        True if tokens are configured, False otherwise.
    """
    return bool(VALID_API_KEYS)
