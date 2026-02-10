"""User endpoints (example).

This module demonstrates optional database usage.
These endpoints only work when DATABASE_URL is configured.
"""

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.db_utils import get_by_id_or_404
from app.core.exceptions import bad_request_exception
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=User, status_code=201)
def create_user(user: User, session: Session = Depends(get_session)) -> User:
    """Create a new user.

    Raises:
        HTTPException: If user with email or username already exists.
    """
    # Check if user already exists
    statement = select(User).where(
        (User.email == user.email) | (User.username == user.username)
    )
    existing = session.exec(statement).first()
    if existing:
        raise bad_request_exception("User with this email or username already exists")

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)) -> User:
    """Get user by ID.

    Raises:
        HTTPException: If user not found.
    """
    return get_by_id_or_404(session, User, user_id, "User")


@router.get("/", response_model=list[User])
def list_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
) -> list[User]:
    """List all users with pagination."""
    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()
    return list(users)
