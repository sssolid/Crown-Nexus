# app/core/config/__init__.py

from __future__ import annotations

"""
Configuration package for the application.

This module exports the main settings interfaces and common types used
throughout the application.
"""

# First, export base types that don't depend on settings
from app.core.config.base import Environment, LogLevel

# Then export the settings
from app.core.config.settings import Settings, get_settings, settings

# Export integration settings
from app.core.config.integrations.as400 import (
    AS400Settings,
    as400_settings,
    get_as400_connector_config,
)
from app.core.config.integrations.elasticsearch import (
    ElasticsearchSettings,
    elasticsearch_settings,
)

__all__ = [
    "Settings",
    "Environment",
    "LogLevel",
    "get_settings",
    "settings",
    "AS400Settings",
    "ElasticsearchSettings",
    "as400_settings",
    "elasticsearch_settings",
    "get_as400_connector_config",
]
