# app/core/config/fitment.py

from __future__ import annotations

"""
Fitment data configuration settings.

This module defines settings for automotive fitment data processing including
database paths, caching, and validation.
"""

import os
from typing import Optional

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.config.base import Environment


class FitmentSettings(BaseSettings):
    """Fitment database and processing settings."""

    # Paths to fitment data files
    VCDB_PATH: str = "data/vcdb.accdb"
    PCDB_PATH: str = "data/pcdb.accdb"
    MODEL_MAPPINGS_PATH: Optional[str] = None

    # Database and performance settings
    FITMENT_DB_URL: Optional[str] = None
    FITMENT_LOG_LEVEL: str = "INFO"
    FITMENT_CACHE_SIZE: int = 100

    # Environment (used for validation logic)
    ENVIRONMENT: Environment = Environment.DEVELOPMENT

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Allow extra fields in env file
    )

    @model_validator(mode="after")
    def validate_fitment_paths(self) -> "FitmentSettings":
        """Validate fitment file paths in production."""
        # Only validate paths in production
        if self.ENVIRONMENT == Environment.PRODUCTION:
            if not os.path.exists(self.VCDB_PATH):
                raise ValueError(f"VCDB_PATH does not exist: {self.VCDB_PATH}")

            if not os.path.exists(self.PCDB_PATH):
                raise ValueError(f"PCDB_PATH does not exist: {self.PCDB_PATH}")

            if self.MODEL_MAPPINGS_PATH and not os.path.exists(
                self.MODEL_MAPPINGS_PATH
            ):
                raise ValueError(
                    f"MODEL_MAPPINGS_PATH does not exist: {self.MODEL_MAPPINGS_PATH}"
                )

        return self
