# /app/services/search/providers/database.py
from __future__ import annotations

"""Database search provider implementation.

This module provides a search provider that queries the database directly.
"""

from typing import Any, Dict, List, Optional, Type, Union, cast

from sqlalchemy import func, or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

from app.core.exceptions import DatabaseException, ErrorCode
from app.core.logging import get_logger
from app.models.product import Fitment, Product
from app.services.search.base import SearchProvider, SearchResult
from app.utils.db import paginate

logger = get_logger("app.services.search.providers.database")


class DatabaseSearchProvider(SearchProvider):
    """Search provider that queries the database directly."""

    def __init__(self, db: AsyncSession, model_class: Type[DeclarativeMeta]) -> None:
        """Initialize the database search provider.

        Args:
            db: Database session
            model_class: SQLAlchemy model class to search
        """
        self.db = db
        self.model_class = model_class
        self.searchable_fields: List[str] = []
        self.logger = logger

    async def initialize(self) -> None:
        """Initialize the database search provider."""
        # Determine searchable fields based on model type
        if self.model_class == Product:
            self.searchable_fields = ["name", "description", "sku", "part_number"]
        elif self.model_class == Fitment:
            self.searchable_fields = ["make", "model", "engine", "transmission"]
        else:
            # Default case - try to find common searchable fields
            for column_name in getattr(self.model_class, "__table__").columns.keys():
                if any(field in column_name.lower() for field in ["name", "title", "description", "id", "code"]):
                    self.searchable_fields.append(column_name)

        self.logger.debug(
            f"Initialized database search for {self.model_class.__name__} "
            f"with searchable fields: {', '.join(self.searchable_fields)}"
        )

    async def shutdown(self) -> None:
        """Shutdown the database search provider."""
        # Nothing to clean up
        pass

    async def search(
        self,
        search_term: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        page: int = 1,
        page_size: int = 20,
        **kwargs: Any
    ) -> SearchResult:
        """Search for entities in the database.

        Args:
            search_term: Text to search for
            filters: Filters to apply
            page: Page number (1-indexed)
            page_size: Number of items per page
            **kwargs: Additional search parameters

        Returns:
            Dict containing search results and pagination info

        Raises:
            DatabaseException: If the database search fails
        """
        try:
            # Start building the query
            query = select(self.model_class)

            # Apply text search if provided
            if search_term:
                search_conditions = []
                search_pattern = f"%{search_term.lower()}%"

                for field_name in self.searchable_fields:
                    if hasattr(self.model_class, field_name):
                        column = getattr(self.model_class, field_name)
                        # Only apply LIKE to string columns
                        if hasattr(column, "type") and hasattr(column.type, "python_type"):
                            if column.type.python_type == str:
                                search_conditions.append(func.lower(column).like(search_pattern))

                if search_conditions:
                    query = query.where(or_(*search_conditions))

            # Apply additional filters
            if filters:
                for key, value in filters.items():
                    if hasattr(self.model_class, key):
                        if isinstance(value, dict) and key == "attributes":
                            # Special handling for JSONB attributes
                            for attr_key, attr_value in value.items():
                                query = query.where(
                                    getattr(self.model_class, key).contains({attr_key: attr_value})
                                )
                        else:
                            query = query.where(getattr(self.model_class, key) == value)

            # Apply is_active filter if the model has that attribute and it wasn't explicitly filtered
            if hasattr(self.model_class, "is_active") and not (filters and "is_active" in filters):
                query = query.where(getattr(self.model_class, "is_active") == True)

            self.logger.debug(
                "Database search query built",
                search_term=search_term,
                filters=filters
            )

            # Execute paginated query
            result = await paginate(self.db, query, page, page_size)

            self.logger.info(
                "Database search successful",
                search_term=search_term,
                results_count=len(result.get("items", [])),
                total=result.get("total", 0)
            )

            return cast(SearchResult, result)

        except SQLAlchemyError as e:
            self.logger.error(
                "Database search query failed",
                search_term=search_term,
                error=str(e),
                exc_info=True
            )
            raise DatabaseException(
                message="Failed to search in database",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e
            ) from e
