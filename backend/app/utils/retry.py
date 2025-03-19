# app/utils/retry.py
"""
Retry utilities for improving resilience of external service calls.

This module provides decorators and utilities for automatically retrying operations
that might fail due to transient issues, such as network timeouts, rate limiting,
or temporary service unavailability.

Features include:
- Configurable retry count, delay, and backoff
- Support for both synchronous and asynchronous functions
- Jitter to prevent thundering herd problems
- Exception filtering to retry only on specific errors
- Timeout handling for operations

All functions include proper error handling, logging, and configurable options to
ensure external service calls are resilient while maintaining responsiveness.
"""

from __future__ import annotations

import asyncio
import functools
import random
import time
from typing import (
    Any,
    Callable,
    List,
    Optional,
    Protocol,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)

from app.core.exceptions import (
    NetworkException,
    RateLimitException,
    ServiceException,
    ErrorCode,
)
from app.core.logging import get_logger

# Initialize structured logger
logger = get_logger("app.utils.retry")

# Type variables
F = TypeVar("F", bound=Callable[..., Any])
T = TypeVar("T")


class RetryableError(Protocol):
    """Protocol defining retryable error behaviors."""

    def is_retryable(self) -> bool:
        """Determine if exception should trigger retry."""
        ...


@overload
def retry(
    retries: int = ...,
    delay: float = ...,
    backoff_factor: float = ...,
    jitter: bool = ...,
    exceptions: Union[Type[Exception], List[Type[Exception]]] = ...,
) -> Callable[[F], F]: ...


@overload
def retry(func: F) -> F: ...


def retry(
    func: Optional[F] = None,
    *,
    retries: int = 3,
    delay: float = 0.1,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    exceptions: Union[Type[Exception], List[Type[Exception]]] = Exception,
) -> Union[Callable[[F], F], F]:
    """Decorator to retry synchronous functions with exponential backoff.

    Args:
        func: Function to decorate (for direct use)
        retries: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff_factor: Multiplier for delay after each retry
        jitter: Whether to add randomness to delay timing
        exceptions: Exception type(s) to catch and retry on

    Returns:
        Callable: Decorated function that will retry on failure

    Examples:
        # As decorator with default settings
        @retry
        def fetch_data():
            ...

        # As decorator with custom settings
        @retry(retries=5, delay=0.5, exceptions=[ConnectionError, TimeoutError])
        def fetch_data():
            ...
    """
    # Convert single exception to tuple
    if isinstance(exceptions, type) and issubclass(exceptions, Exception):
        exceptions = (exceptions,)
    elif isinstance(exceptions, list):
        exceptions = tuple(exceptions)

    def decorator(fn: F) -> F:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None

            for attempt in range(retries + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    # Check if maximum retries reached
                    if attempt >= retries:
                        logger.warning(
                            f"Function {fn.__name__} failed after {retries + 1} attempts",
                            exc_info=e,
                        )
                        raise

                    # Check if exception has is_retryable method and it returns False
                    if hasattr(e, "is_retryable") and not e.is_retryable():
                        logger.info(
                            f"Not retrying {fn.__name__} for non-retryable error: {str(e)}"
                        )
                        raise

                    # Calculate retry delay with exponential backoff
                    retry_delay = delay * (backoff_factor**attempt)

                    # Add jitter to prevent thundering herd
                    if jitter:
                        retry_delay = retry_delay * (0.5 + random.random())

                    logger.info(
                        f"Retrying {fn.__name__} after error: {str(e)}, "
                        f"attempt {attempt + 1}/{retries + 1}, delay: {retry_delay:.2f}s"
                    )

                    # Wait before next attempt
                    time.sleep(retry_delay)

            # This should not be reached, but just in case
            if last_exception:
                raise last_exception

            return None  # Unreachable

        return cast(F, wrapper)

    # Handle direct decoration
    if func is not None:
        return decorator(func)

    return decorator


async def async_retry(
    func: Optional[F] = None,
    *,
    retries: int = 3,
    delay: float = 0.1,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    exceptions: Union[Type[Exception], List[Type[Exception]]] = Exception,
) -> Union[Callable[[F], F], F]:
    """Decorator to retry asynchronous functions with exponential backoff.

    Args:
        func: Function to decorate (for direct use)
        retries: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff_factor: Multiplier for delay after each retry
        jitter: Whether to add randomness to delay timing
        exceptions: Exception type(s) to catch and retry on

    Returns:
        Callable: Decorated async function that will retry on failure

    Examples:
        # As decorator with default settings
        @async_retry
        async def fetch_data():
            ...

        # As decorator with custom settings
        @async_retry(retries=5, delay=0.5, exceptions=[ConnectionError, TimeoutError])
        async def fetch_data():
            ...
    """
    # Convert single exception to tuple
    if isinstance(exceptions, type) and issubclass(exceptions, Exception):
        exceptions = (exceptions,)
    elif isinstance(exceptions, list):
        exceptions = tuple(exceptions)

    def decorator(fn: F) -> F:
        @functools.wraps(fn)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None

            for attempt in range(retries + 1):
                try:
                    return await fn(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    # Check if maximum retries reached
                    if attempt >= retries:
                        logger.warning(
                            f"Function {fn.__name__} failed after {retries + 1} attempts",
                            exc_info=e,
                        )
                        raise

                    # Check if exception has is_retryable method and it returns False
                    if hasattr(e, "is_retryable") and not e.is_retryable():
                        logger.info(
                            f"Not retrying {fn.__name__} for non-retryable error: {str(e)}"
                        )
                        raise

                    # Calculate retry delay with exponential backoff
                    retry_delay = delay * (backoff_factor**attempt)

                    # Add jitter to prevent thundering herd
                    if jitter:
                        retry_delay = retry_delay * (0.5 + random.random())

                    logger.info(
                        f"Retrying {fn.__name__} after error: {str(e)}, "
                        f"attempt {attempt + 1}/{retries + 1}, delay: {retry_delay:.2f}s"
                    )

                    # Wait before next attempt
                    await asyncio.sleep(retry_delay)

            # This should not be reached, but just in case
            if last_exception:
                raise last_exception

            return None  # Unreachable

        return cast(F, wrapper)

    # Handle direct decoration
    if func is not None:
        return decorator(func)

    return decorator


def retry_on_network_errors(
    retries: int = 3,
    delay: float = 0.5,
    backoff_factor: float = 2.0,
    jitter: bool = True,
) -> Callable[[F], F]:
    """Decorator to retry functions specifically on network-related errors.

    This is a convenience wrapper around retry() with pre-configured exception types
    for common network errors.

    Args:
        retries: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff_factor: Multiplier for delay after each retry
        jitter: Whether to add randomness to delay timing

    Returns:
        Callable: Decorator function
    """
    return retry(
        retries=retries,
        delay=delay,
        backoff_factor=backoff_factor,
        jitter=jitter,
        exceptions=[
            NetworkException,
            ServiceException,
            ConnectionError,
            TimeoutError,
        ],
    )


def async_retry_on_network_errors(
    retries: int = 3,
    delay: float = 0.5,
    backoff_factor: float = 2.0,
    jitter: bool = True,
) -> Callable[[F], F]:
    """Decorator to retry async functions specifically on network-related errors.

    This is a convenience wrapper around async_retry() with pre-configured exception types
    for common network errors.

    Args:
        retries: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff_factor: Multiplier for delay after each retry
        jitter: Whether to add randomness to delay timing

    Returns:
        Callable: Decorator function
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            retry_decorator = await async_retry(
                retries=retries,
                delay=delay,
                backoff_factor=backoff_factor,
                jitter=jitter,
                exceptions=[
                    NetworkException,
                    ServiceException,
                    ConnectionError,
                    TimeoutError,
                    asyncio.TimeoutError,
                ],
            )
            return await retry_decorator(func)(*args, **kwargs)
        return wrapper
    return decorator


def retry_with_timeout(
    retries: int = 3,
    delay: float = 0.5,
    timeout: float = 5.0,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    exceptions: Union[Type[Exception], List[Type[Exception]]] = Exception,
) -> Callable[[F], F]:
    """Decorator to retry functions with timeout.

    Combines timeout functionality with retry logic.

    Args:
        retries: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        timeout: Maximum execution time in seconds
        backoff_factor: Multiplier for delay after each retry
        jitter: Whether to add randomness to delay timing
        exceptions: Exception type(s) to catch and retry on

    Returns:
        Callable: Decorator function
    """

    def decorator(func: F) -> F:
        # Create retry decorator
        retry_wrapper = retry(
            retries=retries,
            delay=delay,
            backoff_factor=backoff_factor,
            jitter=jitter,
            exceptions=[*exceptions, TimeoutError],
        )

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            def timeout_wrapper() -> Any:
                """Execute function with timeout using signal."""
                import signal

                def timeout_handler(signum: int, frame: Any) -> None:
                    """Handle timeout signal."""
                    raise NetworkException(
                        message=f"Function {func.__name__} timed out after {timeout} seconds"
                    )

                # Set timeout handler
                old_handler = signal.signal(signal.SIGALRM, timeout_handler)
                signal.setitimer(signal.ITIMER_REAL, timeout)

                try:
                    return func(*args, **kwargs)
                finally:
                    # Reset timer and handler
                    signal.setitimer(signal.ITIMER_REAL, 0)
                    signal.signal(signal.SIGALRM, old_handler)

            # Apply both timeout and retry
            return retry_wrapper(timeout_wrapper)()

        return cast(F, wrapper)

    return decorator


async def async_retry_with_timeout(
    retries: int = 3,
    delay: float = 0.5,
    timeout: float = 5.0,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    exceptions: Union[Type[Exception], List[Type[Exception]]] = Exception,
) -> Callable[[F], F]:
    """Decorator to retry async functions with timeout.

    Combines timeout functionality with retry logic for async functions.

    Args:
        retries: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        timeout: Maximum execution time in seconds
        backoff_factor: Multiplier for delay after each retry
        jitter: Whether to add randomness to delay timing
        exceptions: Exception type(s) to catch and retry on

    Returns:
        Callable: Decorator function
    """

    async def decorator(func: F) -> F:
        # Create retry decorator
        retry_wrapper = await async_retry(
            retries=retries,
            delay=delay,
            backoff_factor=backoff_factor,
            jitter=jitter,
            exceptions=[*exceptions, asyncio.TimeoutError],
        )

        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            async def timeout_wrapper() -> Any:
                """Execute async function with timeout."""
                try:
                    return await asyncio.wait_for(
                        func(*args, **kwargs), timeout=timeout
                    )
                except asyncio.TimeoutError:
                    raise NetworkException(
                        message=f"Function {func.__name__} timed out after {timeout} seconds"
                    )

            # Apply both timeout and retry
            return await retry_wrapper(timeout_wrapper)()

        return cast(F, wrapper)

    return decorator
