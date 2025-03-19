# /app/services/search/base.py
from __future__ import annotations

"""Base interfaces and types for the search system.

This module defines common types, protocols, and interfaces
used throughout the search service components.
"""

from typing import Any, Dict, List, Optional, Protocol, TypeVar, Union

from sqlalchemy.ext.asyncio import AsyncSession

# Type variables
T = TypeVar("T")  # Entity type


class SearchProvider(Protocol):
    """Protocol for search providers."""

    async def search(
        self,
        search_term: Optional[str],
        filters: Dict[str, Any],
        page: int,
        page_size: int,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Search for entities matching the criteria.

        Args:
            search_term: Text to search for
            filters: Filters to apply
            page: Page number (1-indexed)
            page_size: Number of items per page
            **kwargs: Additional search parameters

        Returns:
            Dict containing search results and pagination info
        """
        ...

    async def initialize(self) -> None:
        """Initialize the search provider."""
        ...

    async def shutdown(self) -> None:
        """Shutdown the search provider."""
        ...


class SearchResult(Dict[str, Any]):
    """Type for search results."""

    pass
