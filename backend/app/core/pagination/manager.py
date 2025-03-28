# app/core/pagination/manager.py
from __future__ import annotations

"""Core pagination functionality.

This module provides the main functions for paginating query results using
both offset-based and cursor-based pagination strategies.
"""

import time
from typing import Any, Callable, Optional, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select

from app.core.exceptions import ValidationException
from app.core.pagination.base import (
    CursorPaginationParams,
    OffsetPaginationParams,
    PaginationResult,
)
from app.core.pagination.exceptions import (
    InvalidCursorException,
    InvalidPaginationParamsException,
)
from app.core.pagination.factory import PaginationProviderFactory
from app.core.pagination.providers import (
    CursorPaginationProvider,
    OffsetPaginationProvider,
)
from app.logging import get_logger

logger = get_logger("app.core.pagination.manager")

# Try to import metrics service, but don't fail if not available
try:
    from app.core.dependency_manager import get_dependency
    from app.core.metrics.base import MetricName

    HAS_METRICS = True
except ImportError:
    HAS_METRICS = False

T = TypeVar("T")
R = TypeVar("R")

PaginationProviderFactory._providers = {
    "offset": OffsetPaginationProvider,
    "cursor": CursorPaginationProvider,
}


async def initialize() -> None:
    """Initialize the pagination system."""
    logger.info("Initializing pagination system")


async def shutdown() -> None:
    """Shutdown the pagination system and clean up resources."""
    logger.info("Shutting down pagination system")
    PaginationProviderFactory.clear_cache()


async def paginate_with_offset(
    db: AsyncSession,
    model_class: Type[DeclarativeMeta],
    query: Select,
    params: OffsetPaginationParams,
    transform_func: Optional[Callable[[Any], Any]] = None,
    response_model: Optional[Type[Any]] = None,
) -> PaginationResult[Any]:
    """
    Paginate query results using offset-based pagination.

    Args:
        db: Database session
        model_class: SQLAlchemy model class
        query: SQLAlchemy select query
        params: Offset pagination parameters
        transform_func: Optional function to transform each result item
        response_model: Optional Pydantic model to convert results

    Returns:
        PaginationResult with paginated items and metadata

    Raises:
        InvalidPaginationParamsException: If pagination parameters are invalid
        ValidationException: If other validation errors occur
    """
    metrics_service = None
    start_time = time.monotonic()
    error = None

    try:
        if HAS_METRICS:
            try:
                metrics_service = get_dependency("metrics_service")
            except Exception as e:
                logger.debug(f"Could not get metrics service: {str(e)}")

        logger.debug(
            f"Offset pagination requested for {model_class.__name__}",
            extra={"page": params.page, "page_size": params.page_size},
        )

        try:
            provider = PaginationProviderFactory.create_provider(
                "offset", db, model_class, response_model
            )
            transform = transform_func
            if transform is None and response_model is not None:
                transform = _create_default_transform_func(response_model)
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
                logger.warning(
                    f"Validation error in offset pagination for {model_class.__name__}",
                    exc_info=e,
                    extra={"params": params.model_dump()},
                )
                raise
            logger.error(
                f"Offset pagination failed: {str(e)}",
                exc_info=True,
                extra={"model": model_class.__name__, "params": params.model_dump()},
            )
            raise InvalidPaginationParamsException(
                message=f"Pagination failed: {str(e)}",
                params=params.model_dump(),
                original_exception=e,
            ) from e
    except Exception as e:
        error = type(e).__name__
        raise
    finally:
        if metrics_service and HAS_METRICS:
            duration = time.monotonic() - start_time
            try:
                model_name = model_class.__name__.lower()
                metrics_service.observe_histogram(
                    "pagination_duration_seconds",
                    duration,
                    {"type": "offset", "model": model_name, "error": str(error or "")},
                )
                metrics_service.increment_counter(
                    "pagination_operations_total",
                    1,
                    {"type": "offset", "model": model_name, "error": str(error or "")},
                )
            except Exception as metrics_err:
                logger.warning(
                    f"Failed to record pagination metrics: {str(metrics_err)}",
                    exc_info=metrics_err,
                )


async def paginate_with_cursor(
    db: AsyncSession,
    model_class: Type[DeclarativeMeta],
    query: Select,
    params: CursorPaginationParams,
    transform_func: Optional[Callable[[Any], Any]] = None,
    response_model: Optional[Type[Any]] = None,
) -> PaginationResult[Any]:
    """
    Paginate query results using cursor-based pagination.

    Args:
        db: Database session
        model_class: SQLAlchemy model class
        query: SQLAlchemy select query
        params: Cursor pagination parameters
        transform_func: Optional function to transform each result item
        response_model: Optional Pydantic model to convert results

    Returns:
        PaginationResult with paginated items and metadata

    Raises:
        InvalidCursorException: If the cursor is invalid
        InvalidPaginationParamsException: If pagination parameters are invalid
        ValidationException: If other validation errors occur
    """
    metrics_service = None
    start_time = time.monotonic()
    error = None

    try:
        if HAS_METRICS:
            try:
                metrics_service = get_dependency("metrics_service")
            except Exception as e:
                logger.debug(f"Could not get metrics service: {str(e)}")

        logger.debug(
            f"Cursor pagination requested for {model_class.__name__}",
            extra={"cursor": bool(params.cursor), "limit": params.limit},
        )

        try:
            provider = PaginationProviderFactory.create_provider(
                "cursor", db, model_class, response_model
            )
            transform = transform_func
            if transform is None and response_model is not None:
                transform = _create_default_transform_func(response_model)
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
        except ValueError as e:
            logger.warning(
                f"Invalid cursor for {model_class.__name__}",
                exc_info=e,
                extra={"cursor": params.cursor},
            )
            raise InvalidCursorException(
                message=f"Invalid cursor format: {str(e)}",
                cursor=params.cursor,
                original_exception=e,
            ) from e
        except Exception as e:
            if isinstance(e, ValidationException) or isinstance(
                e, InvalidCursorException
            ):
                raise
            logger.error(
                f"Cursor pagination failed: {str(e)}",
                exc_info=True,
                extra={"model": model_class.__name__, "params": params.model_dump()},
            )
            raise InvalidPaginationParamsException(
                message=f"Pagination failed: {str(e)}",
                params=params.model_dump(),
                original_exception=e,
            ) from e
    except Exception as e:
        error = type(e).__name__
        raise
    finally:
        if metrics_service and HAS_METRICS:
            duration = time.monotonic() - start_time
            try:
                model_name = model_class.__name__.lower()
                metrics_service.observe_histogram(
                    "pagination_duration_seconds",
                    duration,
                    {"type": "cursor", "model": model_name, "error": str(error or "")},
                )
                metrics_service.increment_counter(
                    "pagination_operations_total",
                    1,
                    {"type": "cursor", "model": model_name, "error": str(error or "")},
                )
            except Exception as metrics_err:
                logger.warning(
                    f"Failed to record pagination metrics: {str(metrics_err)}",
                    exc_info=metrics_err,
                )


def _create_default_transform_func(response_model: Type[Any]) -> Callable[[Any], Any]:
    """
    Create a default transform function for converting database models to response models.

    Args:
        response_model: Pydantic model class for the response

    Returns:
        A function that transforms database models to response models

    Raises:
        ValueError: If response_model is None
    """
    if response_model is None:
        raise ValueError("Response model is required for default transform function")

    def transform(item: Any) -> Any:
        if hasattr(response_model, "from_orm"):
            return response_model.from_orm(item)
        else:
            return response_model(**item.__dict__)

    return transform
