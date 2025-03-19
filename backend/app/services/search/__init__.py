# /app/services/search/__init__.py
from __future__ import annotations

"""Search service package for application-wide search functionality.

This package provides services for searching across various entity types
and different backends, including database and Elasticsearch.
"""

from app.services.search.service import SearchService


# Factory function for dependency injection
def get_search_service(db):
    """Factory function to get SearchService

    Args:
        db: Database session

    Returns:
        SearchService instance
    """
    return SearchService(db)


__all__ = ["get_search_service", "SearchService"]
