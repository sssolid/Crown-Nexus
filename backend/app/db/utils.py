# app/db/utils.py
from __future__ import annotations

"""
Database utilities.

This module provides utilities for working with databases and transactions.
"""

import functools
import inspect
from typing import Any, Callable, TypeVar, cast

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger

logger = get_logger("app.db.utils")

T = TypeVar("T")
F = TypeVar("F", bound=Callable[..., Any])

def transaction(func: F) -> F:
    """
    Decorator for database transactions.

    This decorator handles transaction management for database operations,
    committing on success and rolling back on failure.

    It supports both synchronous and asynchronous functions.

    Args:
        func: Function to wrap with transaction management

    Returns:
        Wrapped function with transaction management
    """
    @functools.wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        # Find the database session in args or kwargs
        session = None
        for arg in args:
            if isinstance(arg, AsyncSession):
                session = arg
                break

        if session is None:
            for _, arg in kwargs.items():
                if isinstance(arg, AsyncSession):
                    session = arg
                    break

        if session is None:
            # If no session found, assume it's handled inside the function
            logger.debug(f"No session found for transaction in {func.__name__}, proceeding without transaction management")
            return await func(*args, **kwargs)

        try:
            # Execute the function
            result = await func(*args, **kwargs)

            # Commit the transaction
            await session.commit()
            return result
        except Exception as e:
            # Roll back the transaction on error
            logger.error(f"Transaction failed in {func.__name__}: {str(e)}")
            await session.rollback()
            raise

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        # For synchronous functions (not used in this app)
        raise NotImplementedError(
            "Synchronous transactions not supported in the async application. "
            f"Convert {func.__name__} to an async function."
        )

    # Determine if the decorated function is async
    if inspect.iscoroutinefunction(func):
        return cast(F, async_wrapper)
    else:
        return cast(F, sync_wrapper)
