"""
config.py — Centralized configuration file for Hotel Management System
Author: Shivam Gupta
"""

from pydantic_settings import BaseSettings
from urllib.parse import quote_plus
from pathlib import Path


class Settings(BaseSettings):
    """
    Configuration manager using Pydantic for validation and .env support.
    """

    # =============================
    # Database Configuration
    # =============================
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""  # ⚠️ Set in .env or use environment variable
    DB_NAME: str = "hotel_management_system"

    # =============================
    # Flask App Settings
    # =============================
    API_TITLE: str = "Hotel Management System API"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # =============================
    # Paths and Files
    # =============================
    BASE_DIR: Path = Path(__file__).resolve().parent
    SQL_FILES_DIR: Path = BASE_DIR / "database"

    # =============================
    # Database URL Property
    # =============================
    @property
    def DATABASE_URL(self) -> str:
        """
        Builds a safe SQLAlchemy-compatible MySQL connection string.
        Handles special characters in passwords using urllib.parse.quote_plus().
        """
        encoded_password = quote_plus(self.DB_PASSWORD or "")
        return (
            f"mysql+pymysql://{self.DB_USER}:{encoded_password}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# =============================
# Instantiate Global Settings
# =============================
settings = Settings()

# Optional: Debug log (only if DEBUG is True)
if settings.DEBUG:
    print(f"✅ Loaded configuration for database: {settings.DB_NAME}")
    print(f"🔗 Connection URL: {settings.DATABASE_URL}")
