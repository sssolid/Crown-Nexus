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
from app.core.config.integrations import (
    AS400Settings,
    ElasticsearchSettings,
    as400_settings,
    elasticsearch_settings,
    get_as400_connector_config,
)

# NOTE: The imports from integration modules are delayed to avoid circular imports
# The actual objects are still exported in __all__ for proper module API

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


# Delayed imports of integrations
def __getattr__(name: str) -> object:
    """
    Lazily import and return requested attributes.

    This PEP 562 function allows delayed imports of module attributes.
    """
    if name == "AS400Settings":
        from app.core.config.integrations.as400 import AS400Settings

        return AS400Settings
    elif name == "as400_settings":
        from app.core.config.integrations.as400 import as400_settings

        return as400_settings
    elif name == "get_as400_connector_config":
        from app.core.config.integrations.as400 import get_as400_connector_config

        return get_as400_connector_config
    elif name == "ElasticsearchSettings":
        from app.core.config.integrations.elasticsearch import ElasticsearchSettings

        return ElasticsearchSettings
    elif name == "elasticsearch_settings":
        from app.core.config.integrations.elasticsearch import elasticsearch_settings

        return elasticsearch_settings

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
