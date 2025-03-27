# app/logging/context.py
from __future__ import annotations

"""
Logging context module.

This module provides context management for the logging system, including
request context, user tracking, and execution time logging.
"""

import datetime
from contextlib import contextmanager
from functools import wraps
from typing import Any, Callable, Optional, TypeVar, cast

import structlog
from structlog.stdlib import BoundLogger

# Import the request context from config to avoid circular imports
from app.logging.config import _request_context, get_logger

F = TypeVar("F", bound=Callable[..., Any])
T = TypeVar("T")


@contextmanager
def request_context(request_id: Optional[str] = None, user_id: Optional[str] = None):
    """
    Context manager for tracking request information.

    Args:
        request_id: Optional request ID (generated if not provided)
        user_id: Optional user ID

    Yields:
        The request ID being used
    """
    old_request_id = getattr(_request_context, "request_id", None)
    old_user_id = getattr(_request_context, "user_id", None)

    _request_context.request_id = request_id
    if user_id:
        _request_context.user_id = user_id

    try:
        yield request_id
    finally:
        if old_request_id:
            _request_context.request_id = old_request_id
        else:
            delattr(_request_context, "request_id")

        if user_id:
            if old_user_id:
                _request_context.user_id = old_user_id
            else:
                delattr(_request_context, "user_id")


def set_user_id(user_id: str) -> None:
    """
    Set the user ID for the current context.

    Args:
        user_id: The user ID to set
    """
    _request_context.user_id = user_id


def clear_user_id() -> None:
    """Clear the user ID from the current context."""
    if hasattr(_request_context, "user_id"):
        delattr(_request_context, "user_id")


def log_execution_time(logger: Optional[BoundLogger] = None, level: str = "info"):
    """
    Decorator to log function execution time.

    Args:
        logger: Optional logger to use (defaults to module logger)
        level: Log level to use

    Returns:
        Decorated function
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            log = logger or get_logger(func.__module__)
            log_method = getattr(log, level)

            start_time = datetime.datetime.now()
            log_method(f"{func.__name__} started")

            try:
                result = func(*args, **kwargs)
                execution_time = (datetime.datetime.now() - start_time).total_seconds()
                log_method(f"{func.__name__} completed", execution_time=execution_time)
                return result
            except Exception as e:
                execution_time = (datetime.datetime.now() - start_time).total_seconds()
                log.exception(
                    f"{func.__name__} failed",
                    error=str(e),
                    execution_time=execution_time,
                )
                raise

        return cast(F, wrapper)

    return decorator


def log_execution_time_async(logger: Optional[BoundLogger] = None, level: str = "info"):
    """
    Decorator to log async function execution time.

    Args:
        logger: Optional logger to use (defaults to module logger)
        level: Log level to use

    Returns:
        Decorated async function
    """

    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            log = logger or get_logger(func.__module__)
            log_method = getattr(log, level)

            start_time = datetime.datetime.now()
            log_method(f"{func.__name__} started")

            try:
                result = await func(*args, **kwargs)
                execution_time = (datetime.datetime.now() - start_time).total_seconds()
                log_method(f"{func.__name__} completed", execution_time=execution_time)
                return result
            except Exception as e:
                execution_time = (datetime.datetime.now() - start_time).total_seconds()
                log.exception(
                    f"{func.__name__} failed",
                    error=str(e),
                    execution_time=execution_time,
                )
                raise

        return cast(F, wrapper)

    return decorator
