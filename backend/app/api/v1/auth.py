from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.user import UserCreate, UserOut
from app.schemas.token import Token
from app.services.auth import register_user, login_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut)
def register(data: UserCreate, db: Session = Depends(get_db)):
    user, _ = register_user(db, data.email, data.password)
    return user

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    _, token = login_user(
        db,
        form_data.username,  #email
        form_data.password
    )
    return {
        "access_token": token,
        "token_type": "bearer"
    }