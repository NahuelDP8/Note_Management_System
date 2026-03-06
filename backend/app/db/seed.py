from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
from app.models.category import Category
from app.services.security import hash_password


DEMO_EMAIL = "user@example.com"
DEMO_PASSWORD = "string"

DEFAULT_CATEGORIES = [
    "work",
    "personal",
    "study",
    "ideas",
    "sport",
    "recipes",
]


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
        for name in DEFAULT_CATEGORIES:
            exists = db.query(Category).filter(Category.name == name).first()
            if not exists:
                db.add(Category(name=name))

        db.commit()
        print("🏷️ Categories seeded")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
