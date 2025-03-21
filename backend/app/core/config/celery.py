# app/core/config/celery.py

from __future__ import annotations

"""
Celery task queue configuration settings.

This module defines settings for the Celery task queue including broker
and backend configurations.
"""

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class CelerySettings(BaseSettings):
    """Celery task queue settings."""

    # Celery configuration
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Allow extra fields in env file
    )
