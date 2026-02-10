"""User endpoints (example).

This module demonstrates optional database usage.
These endpoints only work when DATABASE_URL is configured.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import User

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
        raise HTTPException(
            status_code=400, detail="User with this email or username already exists"
        )

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
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=list[User])
def list_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
) -> list[User]:
    """List all users with pagination."""
    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()
    return list(users)
