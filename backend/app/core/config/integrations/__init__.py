# app/core/config/integrations/__init__.py

from __future__ import annotations

"""
Integration settings package.

This module exports all integration-specific settings.
"""

from app.core.config.integrations.as400 import (
    AS400Settings,
    as400_settings,
    get_as400_connector_config,
)
from app.core.config.integrations.filemaker import (
    FilemakerSettings,
    filemaker_settings,
    get_filemaker_connector_config,
)
from app.core.config.integrations.elasticsearch import (
    ElasticsearchSettings,
    elasticsearch_settings,
)

__all__ = [
    "AS400Settings",
    "as400_settings",
    "get_as400_connector_config",
    "FilemakerSettings",
    "filemaker_settings",
    "get_filemaker_connector_config",
    "ElasticsearchSettings",
    "elasticsearch_settings",
]
