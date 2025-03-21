# app/core/config/settings.py

from __future__ import annotations

"""
Combined application settings.

This module integrates all modular settings into a single application settings
class, providing a unified interface for configuration.
"""

from functools import lru_cache
from typing import Any, Dict, Optional

from pydantic import model_validator
from pydantic_settings import BaseSettings

from app.core.config.base import BaseAppSettings, Environment, LogLevel
from app.core.config.celery import CelerySettings
from app.core.config.currency import CurrencySettings
from app.core.config.database import DatabaseSettings
from app.core.config.fitment import FitmentSettings
from app.core.config.integrations.elasticsearch import ElasticsearchSettings
from app.core.config.media import MediaSettings
from app.core.config.security import SecuritySettings


class Settings(
    BaseAppSettings,
    DatabaseSettings,
    SecuritySettings,
    MediaSettings,
    ElasticsearchSettings,
    FitmentSettings,
    CurrencySettings,
    CelerySettings,
):
    """
    Combined application settings.

    This class combines all modular settings into a single settings class
    for application-wide use, with any cross-module validations.
    """

    @model_validator(mode="after")
    def setup_celery_urls(self) -> Settings:
        """Set up Celery broker and result backend URLs if not provided."""
        # Default to Redis for Celery if not specified
        if not self.CELERY_BROKER_URL:
            self.CELERY_BROKER_URL = self.redis_uri

        if not self.CELERY_RESULT_BACKEND:
            self.CELERY_RESULT_BACKEND = self.redis_uri

        return self

    def dict(self, **kwargs: Any) -> Dict[str, Any]:
        """Get settings as a dictionary."""
        # We override this to handle any complex types or computed properties
        # that might cause issues with serialization
        settings_dict = super().dict(**kwargs)

        # Add any computed properties you want to include in the dictionary
        settings_dict["redis_uri"] = self.redis_uri
        settings_dict["elasticsearch_uri"] = self.elasticsearch_uri
        settings_dict["media_base_url"] = self.media_base_url

        return settings_dict


@lru_cache
def get_settings() -> Settings:
    """Get application settings with caching."""
    return Settings()


# Initialize settings singleton
settings = get_settings()
