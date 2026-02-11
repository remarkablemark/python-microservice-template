"""Protected endpoints example.

Demonstrates bearer token authentication usage.
"""

from fastapi import APIRouter, Depends

from app.core.auth import BearerToken, get_api_token

router = APIRouter(
    prefix="/protected", tags=["protected"], dependencies=[Depends(get_api_token)]
)


@router.get("/")
def read_protected() -> dict[str, str]:
    """Protected endpoint requiring valid bearer token.

    Requires Authorization header: Bearer <token>
    """
    return {"message": "Access granted", "authenticated": "true"}


@router.get("/data")
def read_protected_data(token: BearerToken) -> dict[str, str | list[str]]:
    """Protected endpoint returning sensitive data.

    Requires Authorization header: Bearer <token>
    """
    return {
        "message": "This is protected data",
        "data": ["item1", "item2", "item3"],
        "token_preview": token[:8] + "...",  # Show partial token for debugging
    }
