from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path


class Settings(BaseSettings):
    APP_PORT: int
    DEV_MODE: bool
    JWT_SECRET_KEY: str
    JWT_EXPIRATION: int = 86400000  # Default 24 hours in milliseconds
    ALLOWED_ROLES: str
    ALLOWED_PERMISSIONS: str
    MONGO_HOST: str = "localhost"
    MONGO_PORT: int
    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGODB_DATABASE: str
    POSTGRE_HOST: str = "localhost"
    POSTGRE_PORT: int
    POSTGRE_USER: str
    POSTGRE_PASSWORD: str
    POSTGRE_DATABASE: str
    OPENAI_API_KEY: str
    OPENAI_DEFAULT_MODEL: str
    OPENAI_MAX_TOKENS: int
    OPENAI_TEMPERATURE: float


    model_config = {"env_file": ".env"}

    @property
    def mongo_db_url(self) -> str:
        """Constructs and returns the MongoDB connection URL"""
        return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGODB_DATABASE}?authSource=admin"

    @property
    def postgre_db_url(self) -> str:
        """Constructs and returns the MongoDB connection URL"""
        return f"postgresql+asyncpg://{self.POSTGRE_USER}:{self.POSTGRE_PASSWORD}@{self.POSTGRE_HOST}:{self.POSTGRE_PORT}/{self.POSTGRE_DATABASE}"

# Global singleton instance
settings = Settings()

# Ensure the environment variable is set for libraries that need it
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
os.environ["OPENAI_DEFAULT_MODEL"] = settings.OPENAI_DEFAULT_MODEL

if __name__ == "__main__":
    print(f"mongo url={settings.mongo_db_url}")
    print(f"postgre url={settings.postgre_db_url}")
