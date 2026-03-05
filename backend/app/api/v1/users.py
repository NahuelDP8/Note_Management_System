from fastapi import APIRouter, Depends
from app.services.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def me(current_user = Depends(get_current_user)):
    return current_user
