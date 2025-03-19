"""
Configuration for the fitment module.

This module provides configuration settings and utilities.
"""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class FitmentSettings(BaseSettings):
    """Settings for the fitment module."""

    model_config = SettingsConfigDict(
        env_prefix="FITMENT_", case_sensitive=False, extra="ignore"
    )

    # Database paths
    vcdb_path: str = Field(..., description="Path to the VCDB database file")
    pcdb_path: str = Field(..., description="Path to the PCDB database file")

    # Database connection
    db_url: Optional[str] = Field(None, description="SQLAlchemy URL for the database")

    # Model mappings
    model_mappings_path: Optional[str] = Field(
        None, description="Path to the model mappings Excel file"
    )

    # Logging
    log_level: str = Field("INFO", description="Logging level")

    # Performance
    cache_size: int = Field(100, description="Maximum size for LRU caches")

    @validator("vcdb_path", "pcdb_path")
    def validate_file_path(self, v: str) -> str:
        """Validate that a file path exists."""
        if not os.path.isfile(v):
            raise ValueError(f"File not found: {v}")
        return v

    @validator("model_mappings_path")
    def validate_optional_file_path(self, v: Optional[str]) -> Optional[str]:
        """Validate that an optional file path exists if provided."""
        if v is not None and not os.path.isfile(v):
            raise ValueError(f"File not found: {v}")
        return v


@lru_cache(maxsize=1)
def get_settings() -> FitmentSettings:
    """
    Get the fitment settings.

    Returns:
        FitmentSettings instance
    """
    return FitmentSettings()
