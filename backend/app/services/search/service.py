# /app/services/search/service.py
from __future__ import annotations

"""Main search service implementation.

This module provides the primary SearchService that coordinates search
operations across different backends and entity types.
"""

from typing import Any, Dict, List, Optional, Type, Union, cast

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

from app.core.dependency_manager import get_dependency
from app.core.exceptions import BusinessException, DatabaseException, ErrorCode
from app.core.logging import get_logger
from app.models.product import Fitment, Product
from app.services.interfaces import ServiceInterface
from app.services.search.base import SearchProvider, SearchResult
from app.services.search.factory import SearchProviderFactory

# Get cache service
cache_service = get_dependency("cache_service")

logger = get_logger("app.services.search.service")


class SearchService(ServiceInterface):
    """Service for searching various entity types."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the search service.

        Args:
            db: Database session
        """
        self.db = db
        self.logger = logger

    async def initialize(self) -> None:
        """Initialize the search service."""
        self.logger.debug("Initializing search service")

    async def shutdown(self) -> None:
        """Shutdown the search service."""
        self.logger.debug("Shutting down search service")
        await SearchProviderFactory.shutdown_all()

    @cache_service.cache(prefix="search:products", ttl=300, backend="redis")
    async def search_products(
        self,
        search_term: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
        is_active: Optional[bool] = None,
        page: int = 1,
        page_size: int = 20,
        use_elasticsearch: bool = True,
    ) -> Dict[str, Any]:
        """Search for products matching the given criteria.

        Args:
            search_term: Text to search for in product name, description, etc.
            attributes: Product attributes to filter by
            is_active: Filter by active status
            page: Page number for pagination
            page_size: Items per page
            use_elasticsearch: Whether to use Elasticsearch or database search

        Returns:
            Dict containing search results and pagination info

        Raises:
            DatabaseException: If the search operation fails
        """
        try:
            # Prepare filters
            filters: Dict[str, Any] = {}
            if attributes:
                filters["attributes"] = attributes
            if is_active is not None:
                filters["is_active"] = is_active

            # Determine which provider to use
            provider_type = (
                "elasticsearch" if use_elasticsearch and search_term else "database"
            )

            try:
                # Create appropriate provider
                provider = await SearchProviderFactory.create_provider(
                    provider_type, self.db, Product
                )

                # Execute search
                results = await provider.search(
                    search_term=search_term,
                    filters=filters,
                    page=page,
                    page_size=page_size,
                )

                self.logger.info(
                    f"{provider_type.capitalize()} search successful",
                    provider=provider_type,
                    search_term=search_term,
                    results_count=len(results.get("items", [])),
                    total=results.get("total", 0),
                )

                return results

            except Exception as e:
                if provider_type == "elasticsearch" and not isinstance(
                    e, DatabaseException
                ):
                    # Fall back to database search
                    self.logger.warning(
                        "Elasticsearch search failed, falling back to database",
                        error=str(e),
                        search_term=search_term,
                    )

                    provider = await SearchProviderFactory.create_provider(
                        "database", self.db, Product
                    )

                    results = await provider.search(
                        search_term=search_term,
                        filters=filters,
                        page=page,
                        page_size=page_size,
                    )

                    self.logger.info(
                        "Database fallback search successful",
                        search_term=search_term,
                        results_count=len(results.get("items", [])),
                        total=results.get("total", 0),
                    )

                    return results

                # Re-raise original exception
                raise

        except Exception as e:
            self.logger.error(
                "Search operation failed",
                search_term=search_term,
                provider_type=provider_type,
                error=str(e),
                exc_info=True,
            )

            if isinstance(e, DatabaseException):
                raise

            raise DatabaseException(
                message="Failed to search products",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e

    @cache_service.cache(prefix="search:fitments", ttl=300, backend="redis")
    async def search_fitments(
        self,
        search_term: Optional[str] = None,
        year: Optional[int] = None,
        make: Optional[str] = None,
        model: Optional[str] = None,
        engine: Optional[str] = None,
        transmission: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
        use_elasticsearch: bool = True,
    ) -> Dict[str, Any]:
        """Search for fitments matching the given criteria.

        Args:
            search_term: Text to search for
            year: Filter by year
            make: Filter by make
            model: Filter by model
            engine: Filter by engine
            transmission: Filter by transmission
            page: Page number for pagination
            page_size: Items per page
            use_elasticsearch: Whether to use Elasticsearch or database search

        Returns:
            Dict containing search results and pagination info

        Raises:
            DatabaseException: If the search operation fails
        """
        try:
            # Prepare filters
            filters: Dict[str, Any] = {}
            if year is not None:
                filters["year"] = year
            if make:
                filters["make"] = make.lower()
            if model:
                filters["model"] = model.lower()
            if engine:
                filters["engine"] = engine.lower()
            if transmission:
                filters["transmission"] = transmission.lower()

            # Determine which provider to use
            provider_type = (
                "elasticsearch" if use_elasticsearch and search_term else "database"
            )

            try:
                # Create appropriate provider
                provider = await SearchProviderFactory.create_provider(
                    provider_type, self.db, Fitment
                )

                # Execute search
                results = await provider.search(
                    search_term=search_term,
                    filters=filters,
                    page=page,
                    page_size=page_size,
                )

                self.logger.info(
                    f"{provider_type.capitalize()} search successful",
                    provider=provider_type,
                    search_term=search_term,
                    results_count=len(results.get("items", [])),
                    total=results.get("total", 0),
                )

                return results

            except Exception as e:
                if provider_type == "elasticsearch" and not isinstance(
                    e, DatabaseException
                ):
                    # Fall back to database search
                    self.logger.warning(
                        "Elasticsearch search failed, falling back to database",
                        error=str(e),
                        search_term=search_term,
                    )

                    provider = await SearchProviderFactory.create_provider(
                        "database", self.db, Fitment
                    )

                    results = await provider.search(
                        search_term=search_term,
                        filters=filters,
                        page=page,
                        page_size=page_size,
                    )

                    self.logger.info(
                        "Database fallback search successful",
                        search_term=search_term,
                        results_count=len(results.get("items", [])),
                        total=results.get("total", 0),
                    )

                    return results

                # Re-raise original exception
                raise

        except Exception as e:
            self.logger.error(
                "Search operation failed",
                search_term=search_term,
                provider_type=provider_type,
                error=str(e),
                exc_info=True,
            )

            if isinstance(e, DatabaseException):
                raise

            raise DatabaseException(
                message="Failed to search fitments",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e

    async def global_search(
        self,
        search_term: str,
        entity_types: Optional[List[str]] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """Search across multiple entity types.

        Args:
            search_term: Text to search for
            entity_types: Types of entities to search
            page: Page number for pagination
            page_size: Items per page

        Returns:
            Dict containing search results for each entity type
        """
        if not entity_types:
            entity_types = ["products", "fitments", "categories"]

        results: Dict[str, Any] = {}

        try:
            # Use error handling service if available
            error_service = None
            try:
                error_service = get_dependency("error_service")
            except Exception:
                pass

            if "products" in entity_types:
                try:
                    product_results = await self.search_products(
                        search_term=search_term, page=page, page_size=page_size
                    )
                    results["products"] = product_results
                except Exception as e:
                    self.logger.warning(
                        "Product search failed during global search", error=str(e)
                    )
                    if error_service:
                        error_service.handle_exception(
                            e, request_id=getattr(self.db, "request_id", None)
                        )
                    # Continue with other entity types

            if "fitments" in entity_types:
                try:
                    fitment_results = await self.search_fitments(
                        search_term=search_term, page=page, page_size=page_size
                    )
                    results["fitments"] = fitment_results
                except Exception as e:
                    self.logger.warning(
                        "Fitment search failed during global search", error=str(e)
                    )
                    if error_service:
                        error_service.handle_exception(
                            e, request_id=getattr(self.db, "request_id", None)
                        )
                    # Continue with other entity types

            # Future: add other entity types here

            self.logger.info(
                "Global search completed",
                search_term=search_term,
                entity_types=entity_types,
                results_counts={k: len(v.get("items", [])) for k, v in results.items()},
            )

            return results

        except Exception as e:
            self.logger.error(
                "Global search failed",
                search_term=search_term,
                entity_types=entity_types,
                error=str(e),
                exc_info=True,
            )
            # Return partial results if any
            if not results:
                raise DatabaseException(
                    message="Failed to perform global search",
                    code=ErrorCode.DATABASE_ERROR,
                    original_exception=e,
                ) from e
            return results
