from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.schemas.category_schema import CategoryCreate


class CategoriesService:
    def __init__(self):
        self.repo = CategoryRepository()

    def list_categories(self, db: Session, user_id: int) -> list[Category]:
        categories = self.repo.get_all_visible(db, user_id)
        unique_categories: dict[str, Category] = {}

        for category in categories:
            key = category.name.casefold()
            if key not in unique_categories or category.user_id is None:
                unique_categories[key] = category

        return sorted(
            unique_categories.values(),
            key=lambda category: category.name.casefold(),
        )

    def create_category(
        self,
        db: Session,
        data: CategoryCreate,
        user_id: int,
    ) -> Category:
        existing = self.repo.get_visible_by_name(db, data.name, user_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category name already exists",
            )

        try:
            return self.repo.create(db, name=data.name, user_id=user_id)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category name already exists",
            )
