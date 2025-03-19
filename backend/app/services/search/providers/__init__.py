# /app/services/search/providers/__init__.py
from __future__ import annotations

"""Search provider implementations.

This package provides different implementations of the SearchProvider protocol
for searching entities through various backends.
"""

from app.services.search.providers.database import DatabaseSearchProvider
from app.services.search.providers.elasticsearch import ElasticsearchSearchProvider

__all__ = ["DatabaseSearchProvider", "ElasticsearchSearchProvider"]
