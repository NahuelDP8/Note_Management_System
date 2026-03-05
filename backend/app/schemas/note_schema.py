from pydantic import BaseModel

class NoteCreate(BaseModel):
    title: str
    content: str | None = None

class NoteUpdate(BaseModel):
    title: str
    content: str | None = None

class NoteOut(BaseModel):
    id: int
    title: str
    content: str | None
    is_archived: bool

    class Config:
        from_attributes = True
