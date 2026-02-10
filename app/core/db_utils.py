"""Database query utilities for common patterns."""

from typing import Any, TypeVar

from sqlmodel import Session, SQLModel, select

from app.core.exceptions import not_found_exception

T = TypeVar("T", bound=SQLModel)


def get_by_id_or_404(
    session: Session,
    model: type[T],
    id: int,
    resource_name: str | None = None,
) -> T:
    """
    Get a database record by ID or raise 404 if not found.

    Args:
        session: Database session
        model: SQLModel class to query
        id: Primary key ID
        resource_name: Resource name for error message (defaults to model name)

    Returns:
        Model instance

    Raises:
        HTTPException: 404 if record not found

    Example:
        user = get_by_id_or_404(session, User, user_id, "User")
    """
    record = session.get(model, id)
    if record is None:
        name = resource_name or model.__name__
        raise not_found_exception(name, id)
    return record


def exists_by_field(
    session: Session,
    model: type[SQLModel],
    field_name: str,
    value: Any,
) -> bool:
    """
    Check if a record exists with a specific field value.

    Args:
        session: Database session
        model: SQLModel class to query
        field_name: Field name to check
        value: Value to search for

    Returns:
        True if record exists, False otherwise

    Example:
        email_exists = exists_by_field(session, User, "email", "test@example.com")
    """
    field = getattr(model, field_name)
    statement = select(model).where(field == value)
    result = session.exec(statement).first()
    return result is not None
