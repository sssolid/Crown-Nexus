# app/core/config/base.py

from __future__ import annotations

"""
Base application configuration settings.

This module defines fundamental settings for the application including
environment, logging configuration, and basic application information.
"""

from enum import Enum
from pathlib import Path
from typing import Any, List, Optional, Union

from pydantic import field_validator
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


class BaseAppSettings(BaseSettings):
    """Base application settings and configuration."""

    # Basic info
    PROJECT_NAME: str = "Crown Nexus"
    DESCRIPTION: str = "B2B platform for automotive aftermarket industry"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent

    # Locale settings
    DEFAULT_LOCALE: str = "en"
    AVAILABLE_LOCALES: Union[List[str], str] = ["en", "es", "fr", "de"]

    # Logging settings
    LOG_LEVEL: LogLevel = LogLevel.INFO
    LOG_FORMAT: str = "text"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Allow extra fields in env file
        json_schema_extra={
            # Disable JSON parsing for these fields
            "AVAILABLE_LOCALES": {"env_mode": "str"},
        },
    )

    @field_validator("AVAILABLE_LOCALES", mode="before")
    @classmethod
    def parse_str_to_list(cls, v: Any) -> List[str]:
        """Parse string to list."""
        if isinstance(v, str):
            if not v:
                return []
            if "," in v:
                return [item.strip() for item in v.split(",")]
            return [v.strip()]
        return v
