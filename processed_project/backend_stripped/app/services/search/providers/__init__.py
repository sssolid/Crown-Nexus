from __future__ import annotations
'Search provider implementations.\n\nThis package provides different implementations of the SearchProvider protocol\nfor searching entities through various backends.\n'
from app.services.search.providers.database import DatabaseSearchProvider
from app.services.search.providers.elasticsearch import ElasticsearchSearchProvider
__all__ = ['DatabaseSearchProvider', 'ElasticsearchSearchProvider']