# app/core/config/base.py

from __future__ import annotations

"""
Base application configuration settings.

This module defines fundamental settings for the application including
environment, logging configuration, and basic application information.
"""

from enum import Enum
from pathlib import Path
from typing import List, Optional

from pydantic import Field, field_validator
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
    PROJECT_NAME: str = Field("Crown Nexus")
    DESCRIPTION: str = Field("B2B platform for automotive aftermarket industry")
    VERSION: str = Field("0.1.0")
    API_V1_STR: str = Field("/api/v1")
    ENVIRONMENT: Environment = Field(Environment.DEVELOPMENT)
    BASE_DIR: Path = Field(
        default_factory=lambda: Path(__file__).resolve().parent.parent.parent.parent
    )

    # Locale settings
    DEFAULT_LOCALE: str = Field("en")
    AVAILABLE_LOCALES: List[str] = Field(["en", "es", "fr", "de"])

    # Logging settings
    LOG_LEVEL: LogLevel = Field(LogLevel.INFO)
    LOG_FORMAT: str = Field("text")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @field_validator("AVAILABLE_LOCALES")
    def validate_locales(cls, v: List[str]) -> List[str]:
        """Validate that all locales are correctly formatted."""
        for locale in v:
            if not locale.isalpha() or len(locale) != 2:
                raise ValueError(f"Invalid locale format: {locale}. Expected 2-letter code.")
        return v
