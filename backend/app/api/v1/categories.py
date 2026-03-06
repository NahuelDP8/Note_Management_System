from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.category import Category
from app.schemas.category_schema import CategoryCreate, CategoryOut

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryOut])
def list_categories(
    db: Session = Depends(get_db),
):
    return db.query(Category).order_by(Category.name).all()


@router.post(
    "",
    response_model=CategoryOut,
    status_code=status.HTTP_201_CREATED
)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
):
    category = Category(name=data.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category
