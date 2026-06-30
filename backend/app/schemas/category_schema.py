# app/schemas/category_schema.py
from pydantic import BaseModel, Field, field_validator

class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        normalized = " ".join(value.strip().split())
        if not normalized:
            raise ValueError("Category name is required")
        return normalized

class CategoryOut(BaseModel):
    id: int
    name: str
    user_id: int | None = None

    class Config:
        from_attributes = True
