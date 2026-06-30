from pydantic import BaseModel, EmailStr, field_validator

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()

    @field_validator("password")
    @classmethod
    def strip_password(cls, value: str) -> str:
        return value.strip()

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
