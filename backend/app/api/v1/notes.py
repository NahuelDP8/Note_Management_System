from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.services.dependencies import get_current_user
from app.services.notes_service import NotesService
from app.schemas.note_schema import NoteCreate, NoteOut
from app.models.user import User

router = APIRouter(prefix="/notes", tags=["notes"])
service = NotesService()

#List all unarchive notes of a specific user
@router.get("/", response_model=list[NoteOut])
def list_notes(
    archived: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return service.list_notes(
        db=db,
        user_id=current_user.id,
        archived=archived
    )

#Create Note of a specific user
@router.post("/", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(
    data: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return service.create_note(db, data, current_user.id)

#Archive Note of a specific user
@router.patch("/{note_id}/archive", response_model=NoteOut)
def archive_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return service.archive_note(db, note_id, current_user.id)

#Unarchive Note of a specific user
@router.patch("/{note_id}/unarchive", response_model=NoteOut)
def unarchive_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return service.unarchive_note(db, note_id, current_user.id)

# Update Note of a specific user
@router.put("/{note_id}", response_model=NoteOut)
def update_note(
    note_id: int,
    data: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return service.update_note(db, note_id, data, current_user.id)


#Delete Note of a specific user
@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service.delete_note(db, note_id, current_user.id)