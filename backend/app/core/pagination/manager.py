# /app/core/pagination/manager.py
from __future__ import annotations

"""Core pagination functionality.

This module provides the main functions for paginating query results using
both offset-based and cursor-based pagination strategies.
"""

from typing import (
    Any,
    Callable,
    Optional,
    Type,
    TypeVar,
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select

from app.core.exceptions import ValidationException
from app.core.logging import get_logger
from app.core.pagination.base import (
    CursorPaginationParams,
    OffsetPaginationParams,
    PaginationResult,
)
from app.core.pagination.factory import PaginationProviderFactory
from app.core.pagination.providers import (
    CursorPaginationProvider,
    OffsetPaginationProvider,
)

logger = get_logger("app.core.pagination.manager")

T = TypeVar("T")  # SQLAlchemy model type
R = TypeVar("R")  # Result type

# Register providers once at module load time
PaginationProviderFactory._providers = {
    "offset": OffsetPaginationProvider,
    "cursor": CursorPaginationProvider,
}


async def initialize() -> None:
    """Initialize the pagination system."""
    logger.info("Initializing pagination system")


async def shutdown() -> None:
    """Shutdown the pagination system."""
    logger.info("Shutting down pagination system")
    # Clear provider cache
    PaginationProviderFactory.clear_cache()


async def paginate_with_offset(
    db: AsyncSession,
    model_class: Type[DeclarativeMeta],
    query: Select,
    params: OffsetPaginationParams,
    transform_func: Optional[Callable[[Any], Any]] = None,
    response_model: Optional[Type[Any]] = None,
) -> PaginationResult[Any]:
    """Paginate query results using offset-based pagination.

    Args:
        db: Database session
        model_class: SQLAlchemy model class
        query: SQLAlchemy select query
        params: Pagination parameters
        transform_func: Optional function to transform each result item
        response_model: Optional Pydantic response model

    Returns:
        Paginated results

    Raises:
        ValidationException: If pagination parameters are invalid
    """
    try:
        # Create offset pagination provider
        provider = PaginationProviderFactory.create_provider(
            "offset", db, model_class, response_model
        )

        # Determine transform function
        transform = transform_func
        if transform is None and response_model is not None:
            transform = _create_default_transform_func(response_model)

        # Execute pagination
        result = await provider.paginate_with_offset(query, params, transform)

        logger.debug(
            f"Offset pagination for {model_class.__name__} completed",
            extra={
                "page": params.page,
                "page_size": params.page_size,
                "total": result.total,
                "items_count": len(result.items),
            },
        )

        return result

    except Exception as e:
        if isinstance(e, ValidationException):
            raise

        logger.error(
            f"Offset pagination failed: {str(e)}",
            exc_info=True,
            extra={
                "model": model_class.__name__,
                "params": params.model_dump(),
            },
        )

        raise ValidationException(
            message=f"Pagination failed: {str(e)}",
            details=[
                {"loc": ["pagination"], "msg": str(e), "type": "pagination_error"}
            ],
        )


async def paginate_with_cursor(
    db: AsyncSession,
    model_class: Type[DeclarativeMeta],
    query: Select,
    params: CursorPaginationParams,
    transform_func: Optional[Callable[[Any], Any]] = None,
    response_model: Optional[Type[Any]] = None,
) -> PaginationResult[Any]:
    """Paginate query results using cursor-based pagination.

    Args:
        db: Database session
        model_class: SQLAlchemy model class
        query: SQLAlchemy select query
        params: Pagination parameters
        transform_func: Optional function to transform each result item
        response_model: Optional Pydantic response model

    Returns:
        Paginated results

    Raises:
        ValidationException: If pagination parameters are invalid
    """
    try:
        # Create cursor pagination provider
        provider = PaginationProviderFactory.create_provider(
            "cursor", db, model_class, response_model
        )

        # Determine transform function
        transform = transform_func
        if transform is None and response_model is not None:
            transform = _create_default_transform_func(response_model)

        # Execute pagination
        result = await provider.paginate_with_cursor(query, params, transform)

        logger.debug(
            f"Cursor pagination for {model_class.__name__} completed",
            extra={
                "cursor": bool(params.cursor),
                "limit": params.limit,
                "total": result.total,
                "items_count": len(result.items),
                "has_next": result.has_next,
            },
        )

        return result

    except Exception as e:
        if isinstance(e, ValidationException):
            raise

        logger.error(
            f"Cursor pagination failed: {str(e)}",
            exc_info=True,
            extra={
                "model": model_class.__name__,
                "params": params.model_dump(),
            },
        )

        raise ValidationException(
            message=f"Pagination failed: {str(e)}",
            details=[
                {"loc": ["pagination"], "msg": str(e), "type": "pagination_error"}
            ],
        )


def _create_default_transform_func(response_model: Type[Any]) -> Callable[[Any], Any]:
    """Create a default transform function using the response model.

    Args:
        response_model: Pydantic response model

    Returns:
        Function to transform database models to response models
    """
    if response_model is None:
        raise ValueError("Response model is required for default transform function")

    def transform(item: Any) -> Any:
        # Check if the response model has a from_orm method
        if hasattr(response_model, "from_orm"):
            return response_model.from_orm(item)
        else:
            # Fallback for models without from_orm
            return response_model(**item.__dict__)

    return transform
