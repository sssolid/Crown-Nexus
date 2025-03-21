# app/core/config/media.py

from __future__ import annotations

"""
Media handling configuration settings.

This module defines settings for media file storage, paths, and
CDN configuration.
"""

import os
from typing import Optional, Set

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.config.base import Environment


class MediaSettings(BaseSettings):
    """Media handling and storage settings."""

    # Media storage configuration
    MEDIA_ROOT: str = "media"
    MEDIA_URL: str = "/media/"
    MEDIA_STORAGE_TYPE: str = "local"  # Options: local, s3, azure, etc.
    MEDIA_CDN_URL: Optional[str] = None

    # Current environment (used for CDN decisions)
    ENVIRONMENT: Environment = Environment.DEVELOPMENT

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Allow extra fields in env file
    )

    @field_validator("MEDIA_ROOT")
    @classmethod
    def create_media_directories(cls, v: str) -> str:
        """Create media directories if they don't exist."""
        os.makedirs(v, exist_ok=True)
        for media_type in ["image", "document", "video", "other", "thumbnails"]:
            os.makedirs(os.path.join(v, media_type), exist_ok=True)
        return v

    @field_validator("MEDIA_STORAGE_TYPE")
    @classmethod
    def validate_storage_type(cls, v: str) -> str:
        """Validate media storage type."""
        valid_storage_types: Set[str] = {"local", "s3", "azure", "gcs"}
        if v not in valid_storage_types:
            raise ValueError(f"Invalid storage type: {v}. Must be one of {valid_storage_types}")
        return v

    @property
    def media_base_url(self) -> str:
        """Get media base URL."""
        if self.ENVIRONMENT == Environment.PRODUCTION and self.MEDIA_CDN_URL:
            return self.MEDIA_CDN_URL
        return self.MEDIA_URL
