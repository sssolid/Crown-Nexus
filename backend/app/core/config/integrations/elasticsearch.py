# app/core/config/integrations/elasticsearch.py

from __future__ import annotations

"""
Elasticsearch integration configuration.

This module defines configuration settings for the Elasticsearch integration,
including connection parameters and security settings.
"""

from typing import Optional

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ElasticsearchSettings(BaseSettings):
    """Elasticsearch connection and configuration settings."""

    # Connection settings
    ELASTICSEARCH_HOST: str = "localhost"
    ELASTICSEARCH_PORT: int = 9200
    ELASTICSEARCH_USE_SSL: bool = False
    ELASTICSEARCH_USERNAME: Optional[str] = None
    ELASTICSEARCH_PASSWORD: Optional[SecretStr] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Allow extra fields in env file
    )

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

# Create the settings instance
elasticsearch_settings = ElasticsearchSettings()
