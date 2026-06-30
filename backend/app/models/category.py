from sqlalchemy import Column, ForeignKey, Index, Integer, String, func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
    )
    __table_args__ = (
        Index(
            "ix_categories_global_name_lower_unique",
            func.lower(name),
            unique=True,
            postgresql_where=user_id.is_(None),
        ),
        Index(
            "ix_categories_user_name_lower_unique",
            user_id,
            func.lower(name),
            unique=True,
            postgresql_where=user_id.is_not(None),
        ),
    )

    notes = relationship(
        "Note",
        secondary="note_categories",
        back_populates="categories"
    )
    user = relationship("User", back_populates="categories")
