"""HTTP exception factories for consistent error responses."""

from fastapi import HTTPException, status


def not_found_exception(resource: str, identifier: str | int) -> HTTPException:
    """
    Create a 404 Not Found exception.

    Args:
        resource: Type of resource (e.g., "User", "Item")
        identifier: Resource identifier that was not found

    Returns:
        HTTPException with 404 status code

    Example:
        raise not_found_exception("User", user_id)
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource} {identifier} not found",
    )


def bad_request_exception(detail: str) -> HTTPException:
    """
    Create a 400 Bad Request exception.

    Args:
        detail: Error message describing the bad request

    Returns:
        HTTPException with 400 status code

    Example:
        raise bad_request_exception("Email already exists")
    """
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail,
    )


def unauthorized_exception(
    detail: str = "Missing or invalid bearer token",
) -> HTTPException:
    """
    Create a 401 Unauthorized exception.

    Args:
        detail: Error message (default: "Missing or invalid bearer token")

    Returns:
        HTTPException with 401 status code

    Example:
        raise unauthorized_exception("Authorization header required")
    """
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def forbidden_exception(detail: str = "Invalid bearer token") -> HTTPException:
    """
    Create a 403 Forbidden exception.

    Args:
        detail: Error message (default: "Invalid bearer token")

    Returns:
        HTTPException with 403 status code

    Example:
        raise forbidden_exception("Access denied")
    """
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail,
    )


def internal_server_exception(detail: str) -> HTTPException:
    """
    Create a 500 Internal Server Error exception.

    Args:
        detail: Error message describing the server error

    Returns:
        HTTPException with 500 status code

    Example:
        raise internal_server_exception("Database not configured")
    """
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=detail,
    )
