from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.user import User
from app.schemas.category_schema import CategoryCreate, CategoryOut
from app.services.categories_service import CategoriesService
from app.services.dependencies import get_current_user

router = APIRouter(prefix="/categories", tags=["categories"])
service = CategoriesService()


@router.get("", response_model=list[CategoryOut])
def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.list_categories(db, current_user.id)


@router.post(
    "",
    response_model=CategoryOut,
    status_code=status.HTTP_201_CREATED
)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.create_category(db, data, current_user.id)
