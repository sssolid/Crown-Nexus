# app/core/config/settings.py

from __future__ import annotations

"""
Combined application settings.

This module integrates all modular settings into a single application settings
class, providing a unified interface for configuration.
"""

from functools import lru_cache
from typing import Any, Dict

from pydantic import model_validator
from pydantic_settings import SettingsConfigDict

from app.core.config.base import BaseAppSettings
from app.core.config.celery import CelerySettings
from app.core.config.currency import CurrencySettings
from app.core.config.database import DatabaseSettings
from app.core.config.fitment import FitmentSettings
from app.core.config.media import MediaSettings
from app.core.config.security import SecuritySettings


class Settings(
    BaseAppSettings,
    DatabaseSettings,
    SecuritySettings,
    MediaSettings,
    FitmentSettings,
    CurrencySettings,
    CelerySettings,
):
    """
    Combined application settings.

    This class combines all modular settings into a single settings class
    for application-wide use, with any cross-module validations.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Allow extra fields in env file
    )

    @model_validator(mode="after")
    def setup_celery_urls(self) -> "Settings":
        """Set up Celery broker and result backend URLs if not provided."""
        # Default to Redis for Celery if not specified
        if not self.CELERY_BROKER_URL:
            self.CELERY_BROKER_URL = self.redis_uri

        if not self.CELERY_RESULT_BACKEND:
            self.CELERY_RESULT_BACKEND = self.redis_uri

        return self

    def model_dump(self, **kwargs: Any) -> Dict[str, Any]:
        """Get settings as a dictionary."""
        # We override this to handle any complex types or computed properties
        # that might cause issues with serialization
        settings_dict = super().model_dump(**kwargs)

        # Add any computed properties you want to include in the dictionary
        settings_dict["redis_uri"] = self.redis_uri
        settings_dict["media_base_url"] = self.media_base_url

        return settings_dict

    @property
    def as400(self) -> "AS400Settings":
        """
        Access AS400 settings.

        This allows accessing AS400 settings through the main settings object
        while keeping them modularly separated.

        Returns:
            AS400Settings: The AS400 settings object
        """
        from app.core.config.integrations.as400 import as400_settings

        return as400_settings

    @property
    def elasticsearch(self) -> "ElasticsearchSettings":
        """
        Access Elasticsearch settings.

        This allows accessing Elasticsearch settings through the main settings object
        while keeping them modularly separated.

        Returns:
            ElasticsearchSettings: The Elasticsearch settings object
        """
        from app.core.config.integrations.elasticsearch import elasticsearch_settings

        return elasticsearch_settings


@lru_cache
def get_settings() -> Settings:
    """Get application settings with caching."""
    return Settings()


# Initialize settings singleton
settings = get_settings()
