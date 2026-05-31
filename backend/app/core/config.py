from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "Mohd Azam Portfolio API"
    DEBUG: bool = True
    FRONTEND_URL: str = "http://localhost:3000"

    DATABASE_URL: str = "sqlite:///./portfolio.db"

    SECRET_KEY: str = "change-this-secret-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    ADMIN_EMAIL: str = "aa3981863@gmail.com"
    ADMIN_PASSWORD: str = "ChangeMe@123"
    ADMIN_NAME: str = "Mohd Azam"

    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    CONTACT_RECEIVER: str = "aa3981863@gmail.com"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
