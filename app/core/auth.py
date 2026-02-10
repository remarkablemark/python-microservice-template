"""Bearer token authentication.

Provides bearer token-based authentication via Authorization header.
"""

import os
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# Bearer token security scheme
bearer_scheme = HTTPBearer(auto_error=False)

# Load API tokens from environment
# Supports multiple tokens separated by commas
API_TOKENS_STR = os.getenv("API_TOKENS", "")
VALID_API_TOKENS = {
    token.strip() for token in API_TOKENS_STR.split(",") if token.strip()
}


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
    if not VALID_API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Bearer token authentication is not configured",
        )

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if credentials.credentials not in VALID_API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid bearer token",
        )

    return credentials.credentials


# Type alias for dependency injection
BearerToken = Annotated[str, Depends(get_api_token)]


def is_auth_enabled() -> bool:
    """Check if bearer token authentication is enabled.

    Returns:
        True if tokens are configured, False otherwise.
    """
    return bool(VALID_API_TOKENS)
