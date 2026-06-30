import re

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    CORS_ORIGINS: str = "http://localhost:5173"
    PASSWORD_MIN_LENGTH: int = 8

    @field_validator("DATABASE_URL")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        if value.startswith("postgres://"):
            return value.replace("postgres://", "postgresql+psycopg://", 1)
        if value.startswith("postgresql://"):
            return value.replace("postgresql://", "postgresql+psycopg://", 1)
        return value

    @field_validator("CORS_ORIGINS")
    @classmethod
    def validate_cors_origins(cls, value: str) -> str:
        for origin in [item.strip() for item in value.split(",") if item.strip()]:
            is_local_http = origin.startswith("http://localhost") or origin.startswith(
                "http://127.0.0.1"
            )
            if not is_local_http and not origin.startswith("https://"):
                raise ValueError("CORS origins must use HTTPS outside local development.")
        return value

    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip() and "*" not in origin
        ]

    @property
    def cors_origin_regex(self) -> str | None:
        wildcard_origins = [
            origin.strip()
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip() and "*" in origin
        ]
        if not wildcard_origins:
            return None

        patterns = [
            re.escape(origin).replace(r"\*", r"[^/]+")
            for origin in wildcard_origins
        ]
        return r"^(" + "|".join(patterns) + r")$"

    class Config:
        env_file = ".env"

settings = Settings()
