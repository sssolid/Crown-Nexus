# backend/app/core/config.py
"""
Application configuration module.

This module defines the application settings using Pydantic's BaseSettings
for environment variable validation and loading. It provides a centralized
configuration system with type validation and default values.

Environment variables can override these settings by using the same name
as the class attributes. The module uses dotenv for local development
to read values from a .env file.

Examples:
    To access configuration values:

    ```python
    from app.core.config import settings

    db_name = settings.POSTGRES_DB
    ```
"""

from __future__ import annotations

import os
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, DirectoryPath, PostgresDsn, validator
from pydantic_settings import BaseSettings


class Environment(str, Enum):
    """Environment enumeration."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """
    Application settings.

    Attributes:
        PROJECT_NAME: Name of the project
        DESCRIPTION: Project description
        VERSION: API version
        API_V1_STR: API v1 prefix
        SECRET_KEY: Secret key for JWT tokens
        ACCESS_TOKEN_EXPIRE_MINUTES: Expiration time for access tokens in minutes
        BACKEND_CORS_ORIGINS: List of origins that should be allowed by CORS
        POSTGRES_SERVER: PostgreSQL server hostname
        POSTGRES_USER: PostgreSQL username
        POSTGRES_PASSWORD: PostgreSQL password
        POSTGRES_DB: PostgreSQL database name
        SQLALCHEMY_DATABASE_URI: SQLAlchemy database URI
        ELASTICSEARCH_HOST: Elasticsearch host
        ELASTICSEARCH_PORT: Elasticsearch port
        REDIS_HOST: Redis host
        REDIS_PORT: Redis port
        MEDIA_ROOT: Root directory for media files
        MEDIA_URL: Base URL for media files
        MEDIA_STORAGE_TYPE: Type of media storage to use
        ENVIRONMENT: Current environment (development, staging, production)
    """
    PROJECT_NAME: str = "Crown Nexus"
    DESCRIPTION: str = "B2B platform for automotive aftermarket industry"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    # Environment
    ENVIRONMENT: Environment = Environment.DEVELOPMENT

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """
        Parse CORS origins from string or list.

        Args:
            v: CORS origins as string or list

        Returns:
            Union[List[str], str]: Parsed CORS origins

        Raises:
            ValueError: If the value cannot be parsed as a list of origins
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "crown_nexus"  # Database name without slash
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        """
        Assemble database URI from components.

        Args:
            v: Database URI if already provided
            values: Settings values

        Returns:
            Any: Assembled database URI
        """
        if isinstance(v, str):
            return v

        # Get required values, using empty string as fallback
        user = values.get("POSTGRES_USER", "")
        password = values.get("POSTGRES_PASSWORD", "")
        server = values.get("POSTGRES_SERVER", "")
        db = values.get("POSTGRES_DB", "")

        # Ensure all required components are present
        if not all([user, password, server, db]):
            return None

        # Build the connection string correctly
        return f"postgresql+asyncpg://{user}:{password}@{server}/{db}"

    # Elasticsearch
    ELASTICSEARCH_HOST: str = "localhost"
    ELASTICSEARCH_PORT: int = 9200

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    DEFAULT_LOCALE: str = "en"
    AVAILABLE_LOCALES: List[str] = ["en", "es", "fr", "de"]

    # Exchange Rate API settings
    EXCHANGE_RATE_API_KEY: str = ""
    EXCHANGE_RATE_UPDATE_FREQUENCY: int = 24  # Update frequency in hours
    STORE_INVERSE_RATES: bool = True  # Store inverse rates (e.g., EUR->USD and USD->EUR)


    # Fitment module settings
    VCDB_PATH: str = "data/vcdb.accdb"
    PCDB_PATH: str = "data/pcdb.accdb"
    MODEL_MAPPINGS_PATH: Optional[str] = None
    FITMENT_DB_URL: Optional[str] = None
    FITMENT_LOG_LEVEL: str = "INFO"
    FITMENT_CACHE_SIZE: int = 100

    # Media settings
    MEDIA_ROOT: DirectoryPath = "media"
    MEDIA_URL: str = "/media/"
    MEDIA_STORAGE_TYPE: str = "local"  # Options: "local", "s3", etc.
    MEDIA_CDN_URL: Optional[str] = None  # CDN URL for production

    @validator("MEDIA_ROOT", pre=True)
    def create_media_directories(cls, v: str) -> str:
        """
        Create media directories if they don't exist.

        Args:
            v: Media root path

        Returns:
            str: Media root path
        """
        # Create main media directory
        os.makedirs(v, exist_ok=True)

        # Create subdirectories for each media type
        for media_type in ["image", "document", "video", "other", "thumbnails"]:
            os.makedirs(os.path.join(v, media_type), exist_ok=True)

        return v

    @property
    def media_base_url(self) -> str:
        """
        Get the base URL for media files.

        This will use the CDN URL in production or the local media URL in development.

        Returns:
            str: Base URL for media files
        """
        if self.ENVIRONMENT == Environment.PRODUCTION and self.MEDIA_CDN_URL:
            return self.MEDIA_CDN_URL
        return self.MEDIA_URL

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
