from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.note import Note
from app.schemas.note_schema import NoteCreate
from app.repositories.notes_repository import NotesRepository


class NotesService:
    def __init__(self):
        self.repo = NotesRepository()

    def __get_note_or_404(
        self,
        db: Session,
        note_id: int,
        user_id: int
    ) -> Note:
        note = self.repo.get_by_id_and_user(db, note_id, user_id)

        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        return note


    def list_notes(
        self,
        db: Session,
        user_id: int,
        archived: bool
    ):
        return self.repo.get_all_by_user(db, user_id, archived)

    def create_note(
        self,
        db: Session,
        data: NoteCreate,
        user_id: int
    ):
        return self.repo.create(
            db,
            title=data.title,
            content=data.content,
            user_id=user_id
        )

    def archive_note(
        self,
        db: Session,
        note_id: int,
        user_id: int
    ):
        note = self.__get_note_or_404(db, note_id, user_id)
        note.is_archived = True
        return self.repo.save(db, note)

    def unarchive_note(
        self,
        db: Session,
        note_id: int,
        user_id: int
    ):
        note = self.__get_note_or_404(db, note_id, user_id)
        note.is_archived = False
        return self.repo.save(db, note)


    def update_note(
        self, 
        db: Session, 
        note_id: int, 
        data, user_id: int
    ):
        note = self.__get_note_or_404(db, note_id, user_id)
        note.title = data.title
        note.content = data.content

        db.commit()
        db.refresh(note)

        return note

    def delete_note(
        self,
        db: Session,
        note_id: int,
        user_id: int
    ):
        note = self.__get_note_or_404(db, note_id, user_id)
        self.repo.delete(db, note)
