from sqlalchemy.orm import Session
from app.models.note import Note


class NotesRepository:
    def get_by_id_and_user(
        self,
        db: Session,
        note_id: int,
        user_id: int
    ):
        return (
            db.query(Note)
            .filter(
                Note.id == note_id,
                Note.user_id == user_id
            )
            .first()
        )

    def get_all_by_user(
        self,
        db: Session,
        user_id: int,
        archived: bool = False
    ):
        return (
            db.query(Note)
            .filter(
                Note.user_id == user_id,
                Note.is_archived == archived
            )
            .order_by(Note.id.desc())
            .all()
        )

    def get_by_id(self, db: Session, note_id: int):
        return (
            db.query(Note)
            .filter(Note.id == note_id)
            .first()
        )

    def create(
        self,
        db: Session,
        *,
        title: str,
        content: str | None,
        user_id: int
    ):
        note = Note(
            title=title,
            content=content,
            user_id=user_id,
            is_archived=False
        )
        db.add(note)
        db.commit()
        db.refresh(note)
        return note

    def save(self, db: Session, note: Note):
        db.commit()
        db.refresh(note)
        return note

    def delete(self, db: Session, note: Note):
        db.delete(note)
        db.commit()
