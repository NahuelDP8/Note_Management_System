from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.note import Note
from app.models.category import Category
from app.schemas.note_schema import NoteCreate, NoteUpdate
from app.repositories.notes_repository import NotesRepository
from app.repositories.category_repository import CategoryRepository


class NotesService:

    def __init__(self):
        self.repo = NotesRepository()
        self.category_repo = CategoryRepository()

    # Private methods

    def __get_note_or_404(
        self,
        db: Session,
        note_id: int,
        user_id: int,
    ) -> Note:
        note = self.repo.get_by_id_and_user(db, note_id, user_id)

        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found",
            )

        return note

    def __get_categories_or_404(
        self,
        db: Session,
        category_ids: list[int],
    ) -> list[Category]:

        categories = []

        for category_id in category_ids:
            category = self.category_repo.get_by_id(db, category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category {category_id} not found",
                )
            categories.append(category)

        return categories

    # Public methods
    def list_notes_by_categories(
        self,
        db: Session,
        user_id: int,
        category_ids: list[int],
        archived: bool = False,
    ):
        return self.repo.get_by_categories(
            db=db,
            user_id=user_id,
            category_ids=category_ids,
            archived=archived,
        )


    def list_notes(
        self,
        db: Session,
        user_id: int,
        archived: bool,
    ):
        return self.repo.get_all_by_user(db, user_id, archived)

    def create_note(
        self,
        db: Session,
        data: NoteCreate,
        user_id: int,
    ):
        categories = []

        if data.category_ids:
            categories = self.__get_categories_or_404(
                db,
                data.category_ids
            )

        return self.repo.create(
            db,
            title=data.title,
            content=data.content,
            user_id=user_id,
            categories=categories,
        )

    def update_note(
        self,
        db: Session,
        note_id: int,
        data: NoteUpdate,
        user_id: int,
    ):
        note = self.__get_note_or_404(db, note_id, user_id)

        categories = None
        if data.category_ids is not None:
            categories = self.__get_categories_or_404(db, data.category_ids)

        return self.repo.update(
            db,
            note=note,
            title=data.title,
            content=data.content,
            is_archived=data.is_archived,
            categories=categories,
        )

    def archive_note(
        self,
        db: Session,
        note_id: int,
        user_id: int,
    ):
        note = self.__get_note_or_404(db, note_id, user_id)

        return self.repo.update(
            db,
            note=note,
            is_archived=True,
        )

    def unarchive_note(
        self,
        db: Session,
        note_id: int,
        user_id: int,
    ):
        note = self.__get_note_or_404(db, note_id, user_id)

        return self.repo.update(
            db,
            note=note,
            is_archived=False,
        )

    def delete_note(
        self,
        db: Session,
        note_id: int,
        user_id: int,
    ):
        note = self.__get_note_or_404(db, note_id, user_id)
        self.repo.delete(db, note)

    def list_notes_by_category(
        self,
        db: Session,
        user_id: int,
        category_id: int,
        archived: bool = False,
    ):
        category = self.category_repo.get_by_id(db, category_id)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        return self.repo.get_by_category(
            db=db,
            user_id=user_id,
            category_id=category_id,
            archived=archived,
        )
