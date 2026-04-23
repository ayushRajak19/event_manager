"""
Application configuration and environment variables.
"""
import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Override values by setting environment variables, e.g.:
        export DATABASE_URL="postgresql://user:password@localhost/dbname"
        export SECRET_KEY="your-secret-key-here"
    """
    
    # Application metadata
    APP_NAME: str = "Technical Event Management System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./test.db"  # Default to SQLite for local development
    )
    DB_ECHO: bool = False  # Set to True to log all SQL queries
    
    # Security and JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS settings
    CORS_ORIGINS: list = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]
    
    # Password hashing
    PASSWORD_MIN_LENGTH: int = 8
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False


# Create global settings instance
settings = Settings()
