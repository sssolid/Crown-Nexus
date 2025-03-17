# /backend/app/utils/retry.py
from __future__ import annotations

import asyncio
import functools
import logging
import random
import time
from typing import Any, Callable, List, Optional, Type, TypeVar, Union, cast

from app.core.exceptions import (
    NetworkException,
    RateLimitException,
    ServiceUnavailableException,
    TimeoutException,
)
from app.core.logging import get_logger

F = TypeVar('F', bound=Callable[..., Any])
T = TypeVar('T')

logger = get_logger("app.utils.retry")

def retry(
    retries: int = 3,
    delay: float = 0.1,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    exceptions: Union[Type[Exception], List[Type[Exception]]] = Exception
) -> Callable[[F], F]:
    """Retry decorator for synchronous functions.
    
    This decorator retries a function when it raises specified exceptions,
    with exponential backoff and optional jitter.
    
    Args:
        retries: Maximum number of retries
        delay: Initial delay between retries in seconds
        backoff_factor: Backoff multiplier (how much to increase delay each retry)
        jitter: Whether to add random jitter to delay
        exceptions: Exception types to catch and retry
        
    Returns:
        Callable: Decorated function
    """
    # Ensure exceptions is a tuple
    if isinstance(exceptions, type) and issubclass(exceptions, Exception):
        exceptions = (exceptions,)
    elif isinstance(exceptions, list):
        exceptions = tuple(exceptions)
        
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            
            # Try multiple times
            for attempt in range(retries + 1):
                try:
                    # Execute function
                    return func(*args, **kwargs)
                except exceptions as e:
                    # Save exception for later
                    last_exception = e
                    
                    # Last attempt, re-raise exception
                    if attempt >= retries:
                        logger.warning(
                            f"Function {func.__name__} failed after {retries + 1} attempts",
                            exc_info=e
                        )
                        raise
                        
                    # Calculate retry delay with exponential backoff
                    retry_delay = delay * (backoff_factor ** attempt)
                    
                    # Add jitter if enabled
                    if jitter:
                        retry_delay = retry_delay * (0.5 + random.random())
                        
                    # Log retry attempt
                    logger.info(
                        f"Retrying {func.__name__} after error: {str(e)}, "
                        f"attempt {attempt + 1}/{retries + 1}, delay: {retry_delay:.2f}s"
                    )
                    
                    # Sleep before retrying
                    time.sleep(retry_delay)
                    
            # This should never happen, but just in case
            if last_exception:
                raise last_exception
                
            return None  # Unreachable, but makes mypy happy
            
        return cast(F, wrapper)
    return decorator

async def async_retry(
    retries: int = 3,
    delay: float = 0.1,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    exceptions: Union[Type[Exception], List[Type[Exception]]] = Exception
) -> Callable[[F], F]:
    """Retry decorator for asynchronous functions.
    
    This decorator retries an async function when it raises specified exceptions,
    with exponential backoff and optional jitter.
    
    Args:
        retries: Maximum number of retries
        delay: Initial delay between retries in seconds
        backoff_factor: Backoff multiplier (how much to increase delay each retry)
        jitter: Whether to add random jitter to delay
        exceptions: Exception types to catch and retry
        
    Returns:
        Callable: Decorated async function
    """
    # Ensure exceptions is a tuple
    if isinstance(exceptions, type) and issubclass(exceptions, Exception):
        exceptions = (exceptions,)
    elif isinstance(exceptions, list):
        exceptions = tuple(exceptions)
        
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            
            # Try multiple times
            for attempt in range(retries + 1):
                try:
                    # Execute function
                    return await func(*args, **kwargs)
                except exceptions as e:
                    # Save exception for later
                    last_exception = e
                    
                    # Last attempt, re-raise exception
                    if attempt >= retries:
                        logger.warning(
                            f"Function {func.__name__} failed after {retries + 1} attempts",
                            exc_info=e
                        )
                        raise
                        
                    # Calculate retry delay with exponential backoff
                    retry_delay = delay * (backoff_factor ** attempt)
                    
                    # Add jitter if enabled
                    if jitter:
                        retry_delay = retry_delay * (0.5 + random.random())
                        
                    # Log retry attempt
                    logger.info(
                        f"Retrying {func.__name__} after error: {str(e)}, "
                        f"attempt {attempt + 1}/{retries + 1}, delay: {retry_delay:.2f}s"
                    )
                    
                    # Sleep before retrying
                    await asyncio.sleep(retry_delay)
                    
            # This should never happen, but just in case
            if last_exception:
                raise last_exception
                
            return None  # Unreachable, but makes mypy happy
            
        return cast(F, wrapper)
    return decorator

def retry_on_network_errors(
    retries: int = 3,
    delay: float = 0.5,
    backoff_factor: float = 2.0,
    jitter: bool = True
) -> Callable[[F], F]:
    """Retry decorator for functions that may encounter network errors.
    
    This decorator is specialized for network-related errors and uses
    appropriate exception types.
    
    Args:
        retries: Maximum number of retries
        delay: Initial delay between retries in seconds
        backoff_factor: Backoff multiplier (how much to increase delay each retry)
        jitter: Whether to add random jitter to delay
        
    Returns:
        Callable: Decorated function
    """
    return retry(
        retries=retries,
        delay=delay,
        backoff_factor=backoff_factor,
        jitter=jitter,
        exceptions=[
            NetworkException,
            TimeoutException,
            ServiceUnavailableException,
            ConnectionError,
            TimeoutError,
        ]
    )

async def async_retry_on_network_errors(
    retries: int = 3,
    delay: float = 0.5,
    backoff_factor: float = 2.0,
    jitter: bool = True
) -> Callable[[F], F]:
    """Async retry decorator for functions that may encounter network errors.
    
    This decorator is specialized for network-related errors in async functions
    and uses appropriate exception types.
    
    Args:
        retries: Maximum number of retries
        delay: Initial delay between retries in seconds
        backoff_factor: Backoff multiplier (how much to increase delay each retry)
        jitter: Whether to add random jitter to delay
        
    Returns:
        Callable: Decorated async function
    """
    return await async_retry(
        retries=retries,
        delay=delay,
        backoff_factor=backoff_factor,
        jitter=jitter,
        exceptions=[
            NetworkException,
            TimeoutException,
            ServiceUnavailableException,
            ConnectionError,
            TimeoutError,
        ]
    )

def retry_with_timeout(
    retries: int = 3,
    delay: float = 0.5,
    timeout: float = 5.0,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    exceptions: Union[Type[Exception], List[Type[Exception]]] = Exception
) -> Callable[[F], F]:
    """Retry decorator with timeout for synchronous functions.
    
    This decorator combines retry logic with a timeout for each attempt.
    
    Args:
        retries: Maximum number of retries
        delay: Initial delay between retries in seconds
        timeout: Timeout for each attempt in seconds
        backoff_factor: Backoff multiplier (how much to increase delay each retry)
        jitter: Whether to add random jitter to delay
        exceptions: Exception types to catch and retry
        
    Returns:
        Callable: Decorated function
    """
    def decorator(func: F) -> F:
        # Use the retry decorator for the retry logic
        retry_wrapper = retry(
            retries=retries,
            delay=delay,
            backoff_factor=backoff_factor,
            jitter=jitter,
            exceptions=[*exceptions, TimeoutError]
        )
        
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # This will be called by the retry decorator
            def timeout_wrapper() -> Any:
                # Import here to avoid circular imports
                import signal
                
                # Define timeout handler
                def timeout_handler(signum: int, frame: Any) -> None:
                    raise TimeoutError(f"Function {func.__name__} timed out after {timeout} seconds")
                
                # Set timeout
                old_handler = signal.signal(signal.SIGALRM, timeout_handler)
                signal.setitimer(signal.ITIMER_REAL, timeout)
                
                try:
                    # Call function
                    return func(*args, **kwargs)
                finally:
                    # Reset timeout
                    signal.setitimer(signal.ITIMER_REAL, 0)
                    signal.signal(signal.SIGALRM, old_handler)
            
            # Call the retry wrapper with our timeout wrapper
            return retry_wrapper(timeout_wrapper)()
            
        return cast(F, wrapper)
    return decorator

async def async_retry_with_timeout(
    retries: int = 3,
    delay: float = 0.5,
    timeout: float = 5.0,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    exceptions: Union[Type[Exception], List[Type[Exception]]] = Exception
) -> Callable[[F], F]:
    """Retry decorator with timeout for asynchronous functions.
    
    This decorator combines retry logic with a timeout for each attempt.
    
    Args:
        retries: Maximum number of retries
        delay: Initial delay between retries in seconds
        timeout: Timeout for each attempt in seconds
        backoff_factor: Backoff multiplier (how much to increase delay each retry)
        jitter: Whether to add random jitter to delay
        exceptions: Exception types to catch and retry
        
    Returns:
        Callable: Decorated async function
    """
    def decorator(func: F) -> F:
        # Use the async_retry decorator for the retry logic
        retry_wrapper = await async_retry(
            retries=retries,
            delay=delay,
            backoff_factor=backoff_factor,
            jitter=jitter,
            exceptions=[*exceptions, asyncio.TimeoutError]
        )
        
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # This will be called by the retry decorator
            async def timeout_wrapper() -> Any:
                try:
                    # Call function with timeout
                    return await asyncio.wait_for(func(*args, **kwargs), timeout=timeout)
                except asyncio.TimeoutError:
                    # Convert asyncio timeout to our timeout exception
                    raise TimeoutException(
                        f"Function {func.__name__} timed out after {timeout} seconds"
                    )
            
            # Call the retry wrapper with our timeout wrapper
            return await retry_wrapper(timeout_wrapper)()
            
        return cast(F, wrapper)
    return decorator
