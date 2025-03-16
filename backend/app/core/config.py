# backend/app/core/config.py

from __future__ import annotations

import os
import secrets
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

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
    """
    Application environment enumeration.
    
    Attributes:
        DEVELOPMENT: Development environment
        STAGING: Staging/testing environment
        PRODUCTION: Production environment
    """
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(str, Enum):
    """
    Log level enumeration.
    
    Attributes:
        DEBUG: Debug level logging
        INFO: Info level logging
        WARNING: Warning level logging
        ERROR: Error level logging
        CRITICAL: Critical level logging
    """
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class DatabaseSettings(BaseSettings):
    """
    Database connection settings.
    
    Attributes:
        POSTGRES_SERVER: PostgreSQL server hostname
        POSTGRES_USER: PostgreSQL username
        POSTGRES_PASSWORD: PostgreSQL password
        POSTGRES_DB: PostgreSQL database name
        POSTGRES_PORT: PostgreSQL server port
        SQLALCHEMY_DATABASE_URI: Constructed database URI
    """
    POSTGRES_SERVER: str = Field("localhost")
    POSTGRES_USER: str = Field("postgres")
    POSTGRES_PASSWORD: str = Field("postgres")
    POSTGRES_DB: str = Field("crown_nexus")
    POSTGRES_PORT: str = Field("5432")
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    
    @model_validator(mode="after")
    def assemble_db_connection(self) -> "DatabaseSettings":
        """
        Assemble database URI from components.
        
        Returns:
            Self with SQLALCHEMY_DATABASE_URI set
        """
        if self.SQLALCHEMY_DATABASE_URI:
            return self
        
        # Construct PostgreSQL URL
        self.SQLALCHEMY_DATABASE_URI = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=int(self.POSTGRES_PORT),
            path=f"{self.POSTGRES_DB}",
        )
        
        return self


class ElasticsearchSettings(BaseSettings):
    """
    Elasticsearch connection settings.
    
    Attributes:
        ELASTICSEARCH_HOST: Elasticsearch server hostname
        ELASTICSEARCH_PORT: Elasticsearch server port
        ELASTICSEARCH_USE_SSL: Whether to use SSL for connection
        ELASTICSEARCH_USERNAME: Elasticsearch username (optional)
        ELASTICSEARCH_PASSWORD: Elasticsearch password (optional)
    """
    ELASTICSEARCH_HOST: str = Field("localhost")
    ELASTICSEARCH_PORT: int = Field(9200)
    ELASTICSEARCH_USE_SSL: bool = Field(False)
    ELASTICSEARCH_USERNAME: Optional[str] = None
    ELASTICSEARCH_PASSWORD: Optional[SecretStr] = None
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    
    @property
    def uri(self) -> str:
        """
        Get Elasticsearch URI.
        
        Returns:
            Elasticsearch connection URI
        """
        protocol = "https" if self.ELASTICSEARCH_USE_SSL else "http"
        auth = ""
        if self.ELASTICSEARCH_USERNAME:
            password = self.ELASTICSEARCH_PASSWORD.get_secret_value() if self.ELASTICSEARCH_PASSWORD else ""
            auth = f"{self.ELASTICSEARCH_USERNAME}:{password}@"
        
        return f"{protocol}://{auth}{self.ELASTICSEARCH_HOST}:{self.ELASTICSEARCH_PORT}"


class RedisSettings(BaseSettings):
    """
    Redis connection settings.
    
    Attributes:
        REDIS_HOST: Redis server hostname
        REDIS_PORT: Redis server port
        REDIS_PASSWORD: Redis password (optional)
        REDIS_DB: Redis database number
    """
    REDIS_HOST: str = Field("localhost")
    REDIS_PORT: int = Field(6379)
    REDIS_PASSWORD: Optional[SecretStr] = None
    REDIS_DB: int = Field(0)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    
    @property
    def uri(self) -> str:
        """
        Get Redis URI.
        
        Returns:
            Redis connection URI
        """
        password_part = ""
        if self.REDIS_PASSWORD:
            password_part = f":{self.REDIS_PASSWORD.get_secret_value()}@"
        
        return f"redis://{password_part}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


class LocaleSettings(BaseSettings):
    """
    Internationalization and localization settings.
    
    Attributes:
        DEFAULT_LOCALE: Default locale
        AVAILABLE_LOCALES: List of available locales
    """
    DEFAULT_LOCALE: str = Field("en")
    AVAILABLE_LOCALES: List[str] = Field(["en", "es", "fr", "de"])
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


class ChatSettings(BaseSettings):
    """
    Chat system settings.
    
    Attributes:
        CHAT_ENCRYPTION_SALT: Salt for chat message encryption
        CHAT_MESSAGE_LIMIT: Default message limit for fetching history
        CHAT_RATE_LIMIT_PER_MINUTE: Maximum messages per minute per user
        CHAT_WEBSOCKET_KEEPALIVE: Keepalive interval in seconds
        CHAT_MAX_MESSAGE_LENGTH: Maximum message length in characters
    """
    CHAT_ENCRYPTION_SALT: str = Field(default_factory=lambda: secrets.token_hex(16))
    CHAT_MESSAGE_LIMIT: int = Field(50)
    CHAT_RATE_LIMIT_PER_MINUTE: int = Field(60)
    CHAT_WEBSOCKET_KEEPALIVE: int = Field(30)
    CHAT_MAX_MESSAGE_LENGTH: int = Field(5000)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


class FitmentSettings(BaseSettings):
    """
    Fitment system settings.
    
    Attributes:
        VCDB_PATH: Path to VCDB Access database
        PCDB_PATH: Path to PCDB Access database
        MODEL_MAPPINGS_PATH: Path to model mappings file (optional)
        FITMENT_DB_URL: Database URL for fitment data (optional)
        FITMENT_LOG_LEVEL: Log level for fitment system
        FITMENT_CACHE_SIZE: Size of fitment cache
    """
    VCDB_PATH: str = Field("data/vcdb.accdb")
    PCDB_PATH: str = Field("data/pcdb.accdb")
    MODEL_MAPPINGS_PATH: Optional[str] = None
    FITMENT_DB_URL: Optional[str] = None
    FITMENT_LOG_LEVEL: str = Field("INFO")
    FITMENT_CACHE_SIZE: int = Field(100)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    
    @model_validator(mode="after")
    def validate_file_paths(self) -> "FitmentSettings":
        """
        Validate that required file paths exist.
        
        Returns:
            Self with validated paths
            
        Raises:
            ValueError: If required paths don't exist
        """
        # Only validate paths in production
        if os.getenv("ENVIRONMENT") == Environment.PRODUCTION.value:
            if not os.path.exists(self.VCDB_PATH):
                raise ValueError(f"VCDB_PATH does not exist: {self.VCDB_PATH}")
            
            if not os.path.exists(self.PCDB_PATH):
                raise ValueError(f"PCDB_PATH does not exist: {self.PCDB_PATH}")
            
            if self.MODEL_MAPPINGS_PATH and not os.path.exists(self.MODEL_MAPPINGS_PATH):
                raise ValueError(f"MODEL_MAPPINGS_PATH does not exist: {self.MODEL_MAPPINGS_PATH}")
                
        return self


class CurrencySettings(BaseSettings):
    """
    Currency and exchange rate settings.
    
    Attributes:
        EXCHANGE_RATE_API_KEY: API key for exchange rate service
        EXCHANGE_RATE_UPDATE_FREQUENCY: Update frequency in hours
        STORE_INVERSE_RATES: Whether to store inverse rates
    """
    EXCHANGE_RATE_API_KEY: str = Field("")
    EXCHANGE_RATE_UPDATE_FREQUENCY: int = Field(24)
    STORE_INVERSE_RATES: bool = Field(True)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


class CORSSettings(BaseSettings):
    """
    CORS settings.
    
    Attributes:
        BACKEND_CORS_ORIGINS: List of allowed origins for CORS
    """
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = Field(default_factory=list)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """
        Parse CORS origins from string or list.
        
        Args:
            v: CORS origins as string or list
            
        Returns:
            List of CORS origin strings
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


class SecuritySettings(BaseSettings):
    """
    Security settings.
    
    Attributes:
        SECRET_KEY: Secret key for token signing
        ACCESS_TOKEN_EXPIRE_MINUTES: JWT token expiration time in minutes
        ALGORITHM: JWT signing algorithm
    """
    SECRET_KEY: str = Field("your-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60 * 24 * 8)  # 8 days
    ALGORITHM: str = Field("HS256")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


class MediaSettings(BaseSettings):
    """
    Media handling settings.
    
    Attributes:
        MEDIA_ROOT: Root directory for media files
        MEDIA_URL: URL prefix for media files
        MEDIA_STORAGE_TYPE: Storage type (local, s3, etc.)
        MEDIA_CDN_URL: CDN URL for media files (optional)
    """
    MEDIA_ROOT: DirectoryPath = Field("media")
    MEDIA_URL: str = Field("/media/")
    MEDIA_STORAGE_TYPE: str = Field("local")
    MEDIA_CDN_URL: Optional[str] = None
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    
    @field_validator("MEDIA_ROOT", mode="before")
    @classmethod
    def create_media_directories(cls, v: str) -> str:
        """
        Create media directories if they don't exist.
        
        Args:
            v: Media root path
            
        Returns:
            Media root path
        """
        os.makedirs(v, exist_ok=True)
        for media_type in ["image", "document", "video", "other", "thumbnails"]:
            os.makedirs(os.path.join(v, media_type), exist_ok=True)
        return v
    
    @property
    def media_base_url(self) -> str:
        """
        Get the base URL for media files.
        
        Returns:
            Base URL for media files (CDN URL in production, local path otherwise)
        """
        if os.getenv("ENVIRONMENT") == Environment.PRODUCTION.value and self.MEDIA_CDN_URL:
            return self.MEDIA_CDN_URL
        return self.MEDIA_URL


class CelerySettings(BaseSettings):
    """
    Celery worker settings.
    
    Attributes:
        CELERY_BROKER_URL: URL for Celery broker
        CELERY_RESULT_BACKEND: URL for Celery result backend
    """
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


class LoggingSettings(BaseSettings):
    """
    Logging configuration settings.
    
    Attributes:
        LOG_LEVEL: Default log level
        LOG_FORMAT: Log format (json or text)
    """
    LOG_LEVEL: LogLevel = Field(LogLevel.INFO)
    LOG_FORMAT: str = Field("text")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


class Settings(BaseSettings):
    """
    Main application settings combining all subsystems.
    
    Attributes:
        PROJECT_NAME: Name of the project
        DESCRIPTION: Project description
        VERSION: Application version
        ENVIRONMENT: Current environment
        API_V1_STR: API v1 prefix
        BASE_DIR: Base directory for the application
        
        # Subsystem settings included as properties
    """
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
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    
    # Elasticsearch settings
    ELASTICSEARCH_HOST: str = Field("localhost")
    ELASTICSEARCH_PORT: int = Field(9200)
    
    # Redis settings
    REDIS_HOST: str = Field("localhost")
    REDIS_PORT: int = Field(6379)
    
    # Security settings
    SECRET_KEY: str = Field("your-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60 * 24 * 8)
    
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
    
    # Chat settings
    CHAT_ENCRYPTION_SALT: str = Field("")
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
    
    # Currency settings
    EXCHANGE_RATE_API_KEY: str = Field("")
    EXCHANGE_RATE_UPDATE_FREQUENCY: int = Field(24)
    STORE_INVERSE_RATES: bool = Field(True)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """
        Parse CORS origins from string or list.
        
        Args:
            v: CORS origins as string or list
            
        Returns:
            List of CORS origin strings
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    @field_validator("MEDIA_ROOT", mode="before")
    @classmethod
    def create_media_directories(cls, v: str) -> str:
        """
        Create media directories if they don't exist.
        
        Args:
            v: Media root path
            
        Returns:
            Media root path
        """
        os.makedirs(v, exist_ok=True)
        for media_type in ["image", "document", "video", "other", "thumbnails"]:
            os.makedirs(os.path.join(v, media_type), exist_ok=True)
        return v
    
    @model_validator(mode="after")
    def assemble_db_connection(self) -> "Settings":
        """
        Assemble database URI from components.
        
        Returns:
            Self with SQLALCHEMY_DATABASE_URI set
        """
        if not self.SQLALCHEMY_DATABASE_URI:
            self.SQLALCHEMY_DATABASE_URI = PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_SERVER,
                path=f"{self.POSTGRES_DB}",
            )
        
        return self
    
    @property
    def media_base_url(self) -> str:
        """
        Get the base URL for media files.
        
        Returns:
            Base URL for media files (CDN URL in production, local path otherwise)
        """
        if self.ENVIRONMENT == Environment.PRODUCTION and self.MEDIA_CDN_URL:
            return self.MEDIA_CDN_URL
        return self.MEDIA_URL
    
    # Structured access to configuration subsystems
    @property
    def db(self) -> DatabaseSettings:
        """Get database settings."""
        return DatabaseSettings(
            POSTGRES_SERVER=self.POSTGRES_SERVER,
            POSTGRES_USER=self.POSTGRES_USER,
            POSTGRES_PASSWORD=self.POSTGRES_PASSWORD,
            POSTGRES_DB=self.POSTGRES_DB,
            SQLALCHEMY_DATABASE_URI=self.SQLALCHEMY_DATABASE_URI,
        )
    
    @property
    def elasticsearch(self) -> ElasticsearchSettings:
        """Get Elasticsearch settings."""
        return ElasticsearchSettings(
            ELASTICSEARCH_HOST=self.ELASTICSEARCH_HOST,
            ELASTICSEARCH_PORT=self.ELASTICSEARCH_PORT,
        )
    
    @property
    def redis(self) -> RedisSettings:
        """Get Redis settings."""
        return RedisSettings(
            REDIS_HOST=self.REDIS_HOST,
            REDIS_PORT=self.REDIS_PORT,
        )
    
    @property
    def security(self) -> SecuritySettings:
        """Get security settings."""
        return SecuritySettings(
            SECRET_KEY=self.SECRET_KEY,
            ACCESS_TOKEN_EXPIRE_MINUTES=self.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
    
    @property
    def media(self) -> MediaSettings:
        """Get media settings."""
        return MediaSettings(
            MEDIA_ROOT=self.MEDIA_ROOT,
            MEDIA_URL=self.MEDIA_URL,
            MEDIA_STORAGE_TYPE=self.MEDIA_STORAGE_TYPE,
            MEDIA_CDN_URL=self.MEDIA_CDN_URL,
        )
    
    @property
    def locale(self) -> LocaleSettings:
        """Get locale settings."""
        return LocaleSettings(
            DEFAULT_LOCALE=self.DEFAULT_LOCALE,
            AVAILABLE_LOCALES=self.AVAILABLE_LOCALES,
        )
    
    @property
    def chat(self) -> ChatSettings:
        """Get chat settings."""
        return ChatSettings(
            CHAT_ENCRYPTION_SALT=self.CHAT_ENCRYPTION_SALT,
            CHAT_MESSAGE_LIMIT=self.CHAT_MESSAGE_LIMIT,
            CHAT_RATE_LIMIT_PER_MINUTE=self.CHAT_RATE_LIMIT_PER_MINUTE,
            CHAT_WEBSOCKET_KEEPALIVE=self.CHAT_WEBSOCKET_KEEPALIVE,
            CHAT_MAX_MESSAGE_LENGTH=self.CHAT_MAX_MESSAGE_LENGTH,
        )
    
    @property
    def fitment(self) -> FitmentSettings:
        """Get fitment settings."""
        return FitmentSettings(
            VCDB_PATH=self.VCDB_PATH,
            PCDB_PATH=self.PCDB_PATH,
            MODEL_MAPPINGS_PATH=self.MODEL_MAPPINGS_PATH,
            FITMENT_DB_URL=self.FITMENT_DB_URL,
            FITMENT_LOG_LEVEL=self.FITMENT_LOG_LEVEL,
            FITMENT_CACHE_SIZE=self.FITMENT_CACHE_SIZE,
        )
    
    @property
    def currency(self) -> CurrencySettings:
        """Get currency settings."""
        return CurrencySettings(
            EXCHANGE_RATE_API_KEY=self.EXCHANGE_RATE_API_KEY,
            EXCHANGE_RATE_UPDATE_FREQUENCY=self.EXCHANGE_RATE_UPDATE_FREQUENCY,
            STORE_INVERSE_RATES=self.STORE_INVERSE_RATES,
        )


@lru_cache
def get_settings() -> Settings:
    """
    Get application settings with caching.
    
    This function is cached to avoid loading settings multiple times.
    
    Returns:
        Application settings
    """
    return Settings()


# Initialize settings singleton
settings = get_settings()