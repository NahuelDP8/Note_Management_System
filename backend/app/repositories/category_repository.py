from sqlalchemy.orm import Session
from app.models.category import Category


class CategoryRepository:

    def get_by_id(self, db: Session, category_id: int) -> Category | None:
        return (
            db.query(Category)
            .filter(Category.id == category_id)
            .first()
        )

    def get_all(self, db: Session) -> list[Category]:
        return (
            db.query(Category)
            .order_by(Category.name)
            .all()
        )

    def create(self, db: Session, name: str) -> Category:
        category = Category(name=name)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category
