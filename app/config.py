# app/config.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Self


# Define a Pydantic settings class to handle environment variables
class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_name: str
    db_hostname: str

    @property
    def database_url(self: Self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_hostname}/{self.db_name}"

    class Config:
        env_file = ".env"  # Load environment variables from .env file


# Cache the settings to avoid reloading on every access
@lru_cache()
def get_settings() -> Settings:
    return Settings()


# Use settings to configure the database
settings = get_settings()
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
