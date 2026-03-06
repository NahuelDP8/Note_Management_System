from pydantic import BaseModel, Field
from app.schemas.category_schema import CategoryOut


class NoteCreate(BaseModel):
    title: str
    content: str | None = None
    category_ids: list[int] = Field(default_factory=list)


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    is_archived: bool | None = None
    category_ids: list[int] | None = None


class NoteOut(BaseModel):
    id: int
    title: str
    content: str | None
    is_archived: bool
    categories: list[CategoryOut] = Field(default_factory=list)

    class Config:
        from_attributes = True
