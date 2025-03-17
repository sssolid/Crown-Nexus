from __future__ import annotations
import asyncio
import functools
import logging
import random
import time
from typing import Any, Callable, List, Optional, Type, TypeVar, Union, cast
from app.core.exceptions import NetworkException, RateLimitException, ServiceUnavailableException, TimeoutException
from app.core.logging import get_logger
F = TypeVar('F', bound=Callable[..., Any])
T = TypeVar('T')
logger = get_logger('app.utils.retry')
def retry(retries: int=3, delay: float=0.1, backoff_factor: float=2.0, jitter: bool=True, exceptions: Union[Type[Exception], List[Type[Exception]]]=Exception) -> Callable[[F], F]:
    if isinstance(exceptions, type) and issubclass(exceptions, Exception):
        exceptions = (exceptions,)
    elif isinstance(exceptions, list):
        exceptions = tuple(exceptions)
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt >= retries:
                        logger.warning(f'Function {func.__name__} failed after {retries + 1} attempts', exc_info=e)
                        raise
                    retry_delay = delay * backoff_factor ** attempt
                    if jitter:
                        retry_delay = retry_delay * (0.5 + random.random())
                    logger.info(f'Retrying {func.__name__} after error: {str(e)}, attempt {attempt + 1}/{retries + 1}, delay: {retry_delay:.2f}s')
                    time.sleep(retry_delay)
            if last_exception:
                raise last_exception
            return None
        return cast(F, wrapper)
    return decorator
async def async_retry(retries: int=3, delay: float=0.1, backoff_factor: float=2.0, jitter: bool=True, exceptions: Union[Type[Exception], List[Type[Exception]]]=Exception) -> Callable[[F], F]:
    if isinstance(exceptions, type) and issubclass(exceptions, Exception):
        exceptions = (exceptions,)
    elif isinstance(exceptions, list):
        exceptions = tuple(exceptions)
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt >= retries:
                        logger.warning(f'Function {func.__name__} failed after {retries + 1} attempts', exc_info=e)
                        raise
                    retry_delay = delay * backoff_factor ** attempt
                    if jitter:
                        retry_delay = retry_delay * (0.5 + random.random())
                    logger.info(f'Retrying {func.__name__} after error: {str(e)}, attempt {attempt + 1}/{retries + 1}, delay: {retry_delay:.2f}s')
                    await asyncio.sleep(retry_delay)
            if last_exception:
                raise last_exception
            return None
        return cast(F, wrapper)
    return decorator
def retry_on_network_errors(retries: int=3, delay: float=0.5, backoff_factor: float=2.0, jitter: bool=True) -> Callable[[F], F]:
    return retry(retries=retries, delay=delay, backoff_factor=backoff_factor, jitter=jitter, exceptions=[NetworkException, TimeoutException, ServiceUnavailableException, ConnectionError, TimeoutError])
async def async_retry_on_network_errors(retries: int=3, delay: float=0.5, backoff_factor: float=2.0, jitter: bool=True) -> Callable[[F], F]:
    return await async_retry(retries=retries, delay=delay, backoff_factor=backoff_factor, jitter=jitter, exceptions=[NetworkException, TimeoutException, ServiceUnavailableException, ConnectionError, TimeoutError])
def retry_with_timeout(retries: int=3, delay: float=0.5, timeout: float=5.0, backoff_factor: float=2.0, jitter: bool=True, exceptions: Union[Type[Exception], List[Type[Exception]]]=Exception) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        retry_wrapper = retry(retries=retries, delay=delay, backoff_factor=backoff_factor, jitter=jitter, exceptions=[*exceptions, TimeoutError])
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            def timeout_wrapper() -> Any:
                import signal
                def timeout_handler(signum: int, frame: Any) -> None:
                    raise TimeoutError(f'Function {func.__name__} timed out after {timeout} seconds')
                old_handler = signal.signal(signal.SIGALRM, timeout_handler)
                signal.setitimer(signal.ITIMER_REAL, timeout)
                try:
                    return func(*args, **kwargs)
                finally:
                    signal.setitimer(signal.ITIMER_REAL, 0)
                    signal.signal(signal.SIGALRM, old_handler)
            return retry_wrapper(timeout_wrapper)()
        return cast(F, wrapper)
    return decorator
async def async_retry_with_timeout(retries: int=3, delay: float=0.5, timeout: float=5.0, backoff_factor: float=2.0, jitter: bool=True, exceptions: Union[Type[Exception], List[Type[Exception]]]=Exception) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        retry_wrapper = await async_retry(retries=retries, delay=delay, backoff_factor=backoff_factor, jitter=jitter, exceptions=[*exceptions, asyncio.TimeoutError])
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            async def timeout_wrapper() -> Any:
                try:
                    return await asyncio.wait_for(func(*args, **kwargs), timeout=timeout)
                except asyncio.TimeoutError:
                    raise TimeoutException(f'Function {func.__name__} timed out after {timeout} seconds')
            return await retry_wrapper(timeout_wrapper)()
        return cast(F, wrapper)
    return decorator