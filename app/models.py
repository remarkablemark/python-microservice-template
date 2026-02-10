"""Database models.

Example SQLModel models for the application.
"""

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """User model example."""

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    username: str = Field(index=True, unique=True)
    full_name: str | None = None
    is_active: bool = Field(default=True)
