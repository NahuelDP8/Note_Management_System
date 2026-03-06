from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import Query

from app.db.deps import get_db
from app.services.dependencies import get_current_user
from app.services.notes_service import NotesService
from app.schemas.note_schema import NoteCreate, NoteOut, NoteUpdate
from app.models.user import User

router = APIRouter(prefix="/notes", tags=["notes"])
service = NotesService()


# List notes (optionally filtered by archived and/or category)
@router.get("", response_model=list[NoteOut])
def list_notes(
    archived: bool = False,
    category_ids: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NotesService()
    if category_ids:
        ids = [int(x) for x in category_ids.split(",")]
        return service.list_notes_by_categories(
            db,
            user_id=current_user.id,
            category_ids=ids,
            archived=archived,
        )

    return service.list_notes(
        db,
        user_id=current_user.id,
        archived=archived,
    )


# Create note
@router.post("", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(
    data: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.create_note(
        db=db,
        data=data,
        user_id=current_user.id,
    )


# Archive note
@router.patch("/{note_id}/archive", response_model=NoteOut)
def archive_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.archive_note(
        db=db,
        note_id=note_id,
        user_id=current_user.id,
    )


# Unarchive note
@router.patch("/{note_id}/unarchive", response_model=NoteOut)
def unarchive_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.unarchive_note(
        db=db,
        note_id=note_id,
        user_id=current_user.id,
    )


# Update note
@router.put("/{note_id}", response_model=NoteOut)
def update_note(
    note_id: int,
    data: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.update_note(
        db=db,
        note_id=note_id,
        data=data,
        user_id=current_user.id,
    )


# Delete note
@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service.delete_note(
        db=db,
        note_id=note_id,
        user_id=current_user.id,
    )


