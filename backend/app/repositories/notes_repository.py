from sqlalchemy.orm import Session

from app.models.note import Note
from app.models.category import Category


class NotesRepository:

    def get_by_id_and_user(
        self,
        db: Session,
        note_id: int,
        user_id: int,
    ) -> Note | None:
        return (
            db.query(Note)
            .filter(
                Note.id == note_id,
                Note.user_id == user_id,
            )
            .first()
        )

    def get_all_by_user(
        self,
        db: Session,
        user_id: int,
        archived: bool = False,
    ) -> list[Note]:
        return (
            db.query(Note)
            .filter(
                Note.user_id == user_id,
                Note.is_archived == archived,
            )
            .order_by(Note.id.desc())
            .all()
        )

    def get_by_categories(
        self,
        db: Session,
        user_id: int,
        category_ids: list[int],
        archived: bool = False,
    ):
        return (
            db.query(Note)
            .join(Note.categories)
            .filter(
                Note.user_id == user_id,
                Note.is_archived == archived,
                Category.id.in_(category_ids),
            )
            .distinct()
            .all()
        )


    def create(
        self,
        db: Session,
        title: str,
        content: str,
        user_id: int,
        categories: list[Category] | None = None,
    ):
        note = Note(
            title=title,
            content=content,
            user_id=user_id,
        )

        if categories:
            note.categories = categories

        db.add(note)
        db.commit()
        db.refresh(note)

        return note


    def update(
        self,
        db: Session,
        *,
        note: Note,
        title: str | None = None,
        content: str | None = None,
        is_archived: bool | None = None,
        categories: list[Category] | None = None,
    ) -> Note:

        if title is not None:
            note.title = title

        if content is not None:
            note.content = content

        if is_archived is not None:
            note.is_archived = is_archived

        if categories is not None:
            note.categories.clear()
            note.categories.extend(categories)

        db.commit()
        db.refresh(note)
        return note

    def delete(self, db: Session, note: Note) -> None:
        db.delete(note)
        db.commit()
