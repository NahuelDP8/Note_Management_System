from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
from app.models.category import Category
from app.services.security import hash_password


DEMO_EMAIL = "user@example.com"
DEMO_PASSWORD = "string"

DEFAULT_CATEGORIES = [
    "Trabajo",
    "Personal",
    "Ideas",
    "Estudio",
]


def seed_default_categories(db: Session) -> None:
    for name in DEFAULT_CATEGORIES:
        exists = (
            db.query(Category)
            .filter(Category.user_id.is_(None))
            .filter(Category.name.ilike(name))
            .first()
        )
        if not exists:
            db.add(Category(name=name, user_id=None))

    db.commit()


def seed():
    db: Session = SessionLocal()

    try:
        # -----------------------
        # User
        # -----------------------
        user = db.query(User).filter(User.email == DEMO_EMAIL).first()
        if not user:
            print("👤 Creating demo user...")
            user = User(
                email=DEMO_EMAIL,
                hashed_password=hash_password(DEMO_PASSWORD)
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            print("ℹ️ Demo user already exists")

        # -----------------------
        # Categories
        # -----------------------
        seed_default_categories(db)
        print("🏷️ Categories seeded")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
