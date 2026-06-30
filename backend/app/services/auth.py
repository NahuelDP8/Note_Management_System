from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.config import settings
from app.repositories.user import get_by_email, create
from app.services.security import hash_password, verify_password
from app.services.jwt import create_access_token


def register_user(db: Session, email: str, password: str):
    if get_by_email(db, email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    if len(password) < settings.PASSWORD_MIN_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Password must be at least {settings.PASSWORD_MIN_LENGTH} characters long"
        )

    user = create(db, email, hash_password(password))
    token = create_access_token({"sub": str(user.id)})
    return user, token


def login_user(db: Session, email: str, password: str):
    user = get_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token({"sub": str(user.id)})
    return user, token
