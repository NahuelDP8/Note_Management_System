from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./notes.db"
    SECRET_KEY: str = "you_Were_hired_:D"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 20

    class Config:
        env_file = ".env"

settings = Settings()
