# app/utils/db_metrics.py
from __future__ import annotations

import functools
import inspect
import time
from typing import Any, Callable, Dict, List, Optional, TypeVar, cast

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependency_manager import get_dependency
from app.core.logging import get_logger
from app.services.metrics_service import MetricsService

logger = get_logger("app.utils.db_metrics")
F = TypeVar("F", bound=Callable[..., Any])


def track_db_query(
    operation: str,
    entity: Optional[str] = None,
) -> Callable[[F], F]:
    """Decorator for tracking database query metrics.

    Args:
        operation: Database operation (e.g., SELECT, INSERT)
        entity: Optional entity being queried

    Returns:
        Decorator function
    """
    def decorator(func: F) -> F:
        is_async = inspect.iscoroutinefunction(func)

        if is_async:
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                # Get metrics service
                metrics_service: Optional[MetricsService] = None
                try:
                    metrics_service = get_dependency("metrics_service")
                except Exception as e:
                    logger.debug(f"Could not get metrics service: {str(e)}")

                # Determine entity from args or kwargs if not provided
                entity_name = entity
                if not entity_name:
                    for arg in args:
                        if hasattr(arg, "__tablename__"):
                            entity_name = getattr(arg, "__tablename__")
                            break

                    if not entity_name:
                        for _, val in kwargs.items():
                            if hasattr(val, "__tablename__"):
                                entity_name = getattr(val, "__tablename__")
                                break

                entity_name = entity_name or "unknown"

                # Start timing
                start_time = time.monotonic()
                error = None

                try:
                    # Execute the function
                    return await func(*args, **kwargs)
                except Exception as e:
                    # Capture error
                    error = type(e).__name__
                    raise
                finally:
                    # Calculate duration
                    duration = time.monotonic() - start_time

                    # Track metrics if service is available
                    if metrics_service:
                        metrics_service.track_db_query(
                            operation=operation,
                            entity=entity_name,
                            duration=duration,
                            error=error
                        )

            return cast(F, async_wrapper)
        else:
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                # Get metrics service
                metrics_service: Optional[MetricsService] = None
                try:
                    metrics_service = get_dependency("metrics_service")
                except Exception as e:
                    logger.debug(f"Could not get metrics service: {str(e)}")

                # Determine entity from args or kwargs if not provided
                entity_name = entity
                if not entity_name:
                    for arg in args:
                        if hasattr(arg, "__tablename__"):
                            entity_name = getattr(arg, "__tablename__")
                            break

                    if not entity_name:
                        for _, val in kwargs.items():
                            if hasattr(val, "__tablename__"):
                                entity_name = getattr(val, "__tablename__")
                                break

                entity_name = entity_name or "unknown"

                # Start timing
                start_time = time.monotonic()
                error = None

                try:
                    # Execute the function
                    return func(*args, **kwargs)
                except Exception as e:
                    # Capture error
                    error = type(e).__name__
                    raise
                finally:
                    # Calculate duration
                    duration = time.monotonic() - start_time

                    # Track metrics if service is available
                    if metrics_service:
                        metrics_service.track_db_query(
                            operation=operation,
                            entity=entity_name,
                            duration=duration,
                            error=error
                        )

            return cast(F, sync_wrapper)

    return decorator


def track_db_transaction() -> Callable[[F], F]:
    """Decorator for tracking database transaction metrics.

    Returns:
        Decorator function
    """
    return track_db_query(operation="TRANSACTION", entity="transaction")


def track_db_select(entity: Optional[str] = None) -> Callable[[F], F]:
    """Decorator for tracking database SELECT query metrics.

    Args:
        entity: Optional entity being queried

    Returns:
        Decorator function
    """
    return track_db_query(operation="SELECT", entity=entity)


def track_db_insert(entity: Optional[str] = None) -> Callable[[F], F]:
    """Decorator for tracking database INSERT query metrics.

    Args:
        entity: Optional entity being inserted

    Returns:
        Decorator function
    """
    return track_db_query(operation="INSERT", entity=entity)


def track_db_update(entity: Optional[str] = None) -> Callable[[F], F]:
    """Decorator for tracking database UPDATE query metrics.

    Args:
        entity: Optional entity being updated

    Returns:
        Decorator function
    """
    return track_db_query(operation="UPDATE", entity=entity)


def track_db_delete(entity: Optional[str] = None) -> Callable[[F], F]:
    """Decorator for tracking database DELETE query metrics.

    Args:
        entity: Optional entity being deleted

    Returns:
        Decorator function
    """
    return track_db_query(operation="DELETE", entity=entity)
