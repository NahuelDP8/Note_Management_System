from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from app.models.category import Category


class CategoryRepository:

    def get_by_id(self, db: Session, category_id: int) -> Category | None:
        return (
            db.query(Category)
            .filter(Category.id == category_id)
            .first()
        )

    def get_visible_by_id(
        self,
        db: Session,
        category_id: int,
        user_id: int,
    ) -> Category | None:
        return (
            db.query(Category)
            .filter(
                Category.id == category_id,
                or_(
                    Category.user_id.is_(None),
                    Category.user_id == user_id,
                ),
            )
            .first()
        )

    def get_all_visible(self, db: Session, user_id: int) -> list[Category]:
        return (
            db.query(Category)
            .filter(
                or_(
                    Category.user_id.is_(None),
                    Category.user_id == user_id,
                )
            )
            .order_by(Category.name)
            .all()
        )

    def get_visible_by_name(
        self,
        db: Session,
        name: str,
        user_id: int,
    ) -> Category | None:
        normalized_name = name.casefold()
        return (
            db.query(Category)
            .filter(
                func.lower(Category.name) == normalized_name,
                or_(
                    Category.user_id.is_(None),
                    Category.user_id == user_id,
                ),
            )
            .first()
        )

    def get_global_by_name(self, db: Session, name: str) -> Category | None:
        return (
            db.query(Category)
            .filter(
                Category.user_id.is_(None),
                func.lower(Category.name) == name.casefold(),
            )
            .first()
        )

    def create(self, db: Session, name: str, user_id: int | None = None) -> Category:
        category = Category(name=name, user_id=user_id)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category
