# backend/app/core/config.py

from __future__ import annotations

import os
import secrets
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import List, Optional, Union

from pydantic import (
    AnyHttpUrl,
    DirectoryPath,
    Field,
    PostgresDsn,
    SecretStr,
    field_validator,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    """Application environment enumeration."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(str, Enum):
    """Log level enumeration."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Settings(BaseSettings):
    """Application settings."""
    # Basic info
    PROJECT_NAME: str = Field("Crown Nexus")
    DESCRIPTION: str = Field("B2B platform for automotive aftermarket industry")
    VERSION: str = Field("0.1.0")
    API_V1_STR: str = Field("/api/v1")
    ENVIRONMENT: Environment = Field(Environment.DEVELOPMENT)
    BASE_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent.parent)

    # Database settings
    POSTGRES_SERVER: str = Field("localhost")
    POSTGRES_USER: str = Field("postgres")
    POSTGRES_PASSWORD: str = Field("postgres")
    POSTGRES_DB: str = Field("crown_nexus")
    POSTGRES_PORT: str = Field("5432")
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    # Security settings
    SECRET_KEY: str = Field("your-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60 * 24 * 8)  # 8 days
    ALGORITHM: str = Field("HS256")
    ALLOWED_HOSTS: List[str] = Field(
        default=["localhost", "127.0.0.1"], description="List of allowed hostnames"
    )
    TRUSTED_PROXIES: List[str] = Field(
        default=["127.0.0.1", "::1"], description="List of trusted proxy IP addresses"
    )
    CORS_ALWAYS_ALLOW: bool = Field(
        default=False, description="Whether to always allow CORS requests"
    )
    CSRF_COOKIE_SECURE: bool = Field(
        default=True, description="Whether to only send CSRF cookie over HTTPS"
    )
    CSRF_TOKEN_EXPIRY: int = Field(
        default=86400,
        description="Expiration time for CSRF tokens in seconds (24 hours)",
    )
    RATE_LIMIT_ENABLED: bool = Field(
        default=True, description="Whether rate limiting is enabled"
    )
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = Field(
        default=60, description="Default requests allowed per minute"
    )
    RATE_LIMIT_BURST_MULTIPLIER: float = Field(
        default=1.5, description="Multiplier for burst capacity"
    )
    RATE_LIMIT_STORAGE: str = Field(
        default="redis",
        description="Storage backend for rate limiting ('redis' or 'memory')",
    )
    CONTENT_SECURITY_POLICY: str = Field(
        default="default-src 'self'; img-src 'self' data:; script-src 'self'; style-src 'self'; connect-src 'self'",
        description="Content Security Policy header value",
    )
    PERMISSIONS_POLICY: str = Field(
        default="camera=(), microphone=(), geolocation=(), payment=()",
        description="Permissions Policy header value",
    )
    AUDIT_LOGGING_ENABLED: bool = Field(
        default=True, description="Whether audit logging is enabled"
    )
    AUDIT_LOG_TO_DB: bool = Field(
        default=True, description="Whether to log audit events to database"
    )
    AUDIT_LOG_TO_FILE: bool = Field(
        default=False, description="Whether to log audit events to file"
    )
    AUDIT_LOG_FILE: str = Field(
        default="logs/audit.log", description="File path for audit log"
    )

    # CORS settings
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = Field(default_factory=list)

    # Media settings
    MEDIA_ROOT: DirectoryPath = Field("media")
    MEDIA_URL: str = Field("/media/")
    MEDIA_STORAGE_TYPE: str = Field("local")
    MEDIA_CDN_URL: Optional[str] = None

    # Locale settings
    DEFAULT_LOCALE: str = Field("en")
    AVAILABLE_LOCALES: List[str] = Field(["en", "es", "fr", "de"])

    # Logging settings
    LOG_LEVEL: LogLevel = Field(LogLevel.INFO)
    LOG_FORMAT: str = Field("text")

    # Redis settings
    REDIS_HOST: str = Field("localhost")
    REDIS_PORT: int = Field(6379)
    REDIS_PASSWORD: Optional[SecretStr] = None
    REDIS_DB: int = Field(0)

    # Elasticsearch settings
    ELASTICSEARCH_HOST: str = Field("localhost")
    ELASTICSEARCH_PORT: int = Field(9200)
    ELASTICSEARCH_USE_SSL: bool = Field(False)
    ELASTICSEARCH_USERNAME: Optional[str] = None
    ELASTICSEARCH_PASSWORD: Optional[SecretStr] = None

    # Chat settings
    CHAT_ENCRYPTION_SALT: str = Field(default_factory=lambda: secrets.token_hex(16))
    CHAT_MESSAGE_LIMIT: int = Field(50)
    CHAT_RATE_LIMIT_PER_MINUTE: int = Field(60)
    CHAT_WEBSOCKET_KEEPALIVE: int = Field(30)
    CHAT_MAX_MESSAGE_LENGTH: int = Field(5000)

    # Fitment settings
    VCDB_PATH: str = Field("data/vcdb.accdb")
    PCDB_PATH: str = Field("data/pcdb.accdb")
    MODEL_MAPPINGS_PATH: Optional[str] = None
    FITMENT_DB_URL: Optional[str] = None
    FITMENT_LOG_LEVEL: str = Field("INFO")
    FITMENT_CACHE_SIZE: int = Field(100)

    # Celery settings
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None

    # Currency settings
    EXCHANGE_RATE_API_KEY: str = Field("")
    EXCHANGE_RATE_UPDATE_FREQUENCY: int = Field(24)
    STORE_INVERSE_RATES: bool = Field(True)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @model_validator(mode="after")
    def assemble_db_connection(self) -> Settings:
        """Build the database URI if not provided directly."""
        if not self.SQLALCHEMY_DATABASE_URI:
            self.SQLALCHEMY_DATABASE_URI = PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_SERVER,
                port=int(self.POSTGRES_PORT),
                path=f"{self.POSTGRES_DB}",
            )
        return self

    @property
    def redis_uri(self) -> str:
        """Get Redis connection URI."""
        password_part = ""
        if self.REDIS_PASSWORD:
            password_part = f":{self.REDIS_PASSWORD.get_secret_value()}@"

        return f"redis://{password_part}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    @property
    def elasticsearch_uri(self) -> str:
        """Get Elasticsearch connection URI."""
        protocol = "https" if self.ELASTICSEARCH_USE_SSL else "http"
        auth = ""
        if self.ELASTICSEARCH_USERNAME:
            password = (
                self.ELASTICSEARCH_PASSWORD.get_secret_value()
                if self.ELASTICSEARCH_PASSWORD
                else ""
            )
            auth = f"{self.ELASTICSEARCH_USERNAME}:{password}@"

        return f"{protocol}://{auth}{self.ELASTICSEARCH_HOST}:{self.ELASTICSEARCH_PORT}"

    @property
    def media_base_url(self) -> str:
        """Get media base URL."""
        if self.ENVIRONMENT == Environment.PRODUCTION and self.MEDIA_CDN_URL:
            return self.MEDIA_CDN_URL
        return self.MEDIA_URL

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @field_validator("MEDIA_ROOT", mode="before")
    @classmethod
    def create_media_directories(cls, v: str) -> str:
        """Create media directories if they don't exist."""
        os.makedirs(v, exist_ok=True)
        for media_type in ["image", "document", "video", "other", "thumbnails"]:
            os.makedirs(os.path.join(v, media_type), exist_ok=True)
        return v

    @model_validator(mode="after")
    def validate_fitment_paths(self) -> Settings:
        """Validate fitment file paths in production."""
        # Only validate paths in production
        if self.ENVIRONMENT == Environment.PRODUCTION:
            if not os.path.exists(self.VCDB_PATH):
                raise ValueError(f"VCDB_PATH does not exist: {self.VCDB_PATH}")

            if not os.path.exists(self.PCDB_PATH):
                raise ValueError(f"PCDB_PATH does not exist: {self.PCDB_PATH}")

            if self.MODEL_MAPPINGS_PATH and not os.path.exists(self.MODEL_MAPPINGS_PATH):
                raise ValueError(f"MODEL_MAPPINGS_PATH does not exist: {self.MODEL_MAPPINGS_PATH}")

        return self


@lru_cache
def get_settings() -> Settings:
    """Get application settings with caching."""
    return Settings()


# Initialize settings singleton
settings = get_settings()
