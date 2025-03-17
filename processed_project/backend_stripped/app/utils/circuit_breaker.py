from __future__ import annotations
import asyncio
import enum
import functools
import logging
import time
from dataclasses import dataclass, field
from threading import RLock
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union, cast
from app.core.exceptions import ServiceUnavailableException
from app.core.logging import get_logger
F = TypeVar('F', bound=Callable[..., Any])
logger = get_logger('app.utils.circuit_breaker')
class CircuitState(enum.Enum):
    CLOSED = 'closed'
    OPEN = 'open'
    HALF_OPEN = 'half_open'
@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    success_threshold: int = 3
    timeout: float = 60.0
    exception_types: List[Type[Exception]] = field(default_factory=lambda: [Exception])
    fallback: Optional[Callable] = None
class CircuitBreaker:
    _breakers: Dict[str, CircuitBreaker] = {}
    _lock = RLock()
    def __init__(self, name: str, config: Optional[CircuitBreakerConfig]=None) -> None:
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = 0.0
        self.last_state_change_time = time.time()
        with self._lock:
            self._breakers[name] = self
    @classmethod
    def get(cls, name: str) -> CircuitBreaker:
        with cls._lock:
            if name not in cls._breakers:
                raise ValueError(f'Circuit breaker not found: {name}')
            return cls._breakers[name]
    @classmethod
    def get_or_create(cls, name: str, config: Optional[CircuitBreakerConfig]=None) -> CircuitBreaker:
        with cls._lock:
            if name not in cls._breakers:
                return cls(name, config)
            return cls._breakers[name]
    @classmethod
    def reset_all(cls) -> None:
        with cls._lock:
            for breaker in cls._breakers.values():
                breaker.reset()
    @classmethod
    def get_all_states(cls) -> Dict[str, CircuitState]:
        with cls._lock:
            return {name: breaker.state for name, breaker in cls._breakers.items()}
    def reset(self) -> None:
        with self._lock:
            self.state = CircuitState.CLOSED
            self.failure_count = 0
            self.success_count = 0
            self.last_failure_time = 0.0
            self.last_state_change_time = time.time()
    def check_state(self) -> None:
        with self._lock:
            if self.state == CircuitState.OPEN:
                elapsed = time.time() - self.last_failure_time
                if elapsed >= self.config.timeout:
                    self._transition_to(CircuitState.HALF_OPEN)
    def _transition_to(self, new_state: CircuitState) -> None:
        if self.state != new_state:
            logger.info(f"Circuit breaker '{self.name}' transitioning from {self.state.value} to {new_state.value}")
            self.state = new_state
            self.last_state_change_time = time.time()
            if new_state == CircuitState.CLOSED:
                self.failure_count = 0
            elif new_state == CircuitState.OPEN:
                self.success_count = 0
            elif new_state == CircuitState.HALF_OPEN:
                self.failure_count = 0
                self.success_count = 0
    def _on_success(self) -> None:
        with self._lock:
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.config.success_threshold:
                    self._transition_to(CircuitState.CLOSED)
            elif self.state == CircuitState.CLOSED:
                self.failure_count = 0
    def _on_failure(self, exception: Exception) -> None:
        with self._lock:
            self.last_failure_time = time.time()
            if not any((isinstance(exception, exc_type) for exc_type in self.config.exception_types)):
                return
            if self.state == CircuitState.CLOSED:
                self.failure_count += 1
                if self.failure_count >= self.config.failure_threshold:
                    self._transition_to(CircuitState.OPEN)
            elif self.state == CircuitState.HALF_OPEN:
                self._transition_to(CircuitState.OPEN)
    def __call__(self, func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            self.check_state()
            if self.state == CircuitState.OPEN:
                logger.warning(f"Circuit breaker '{self.name}' is OPEN - fast failing")
                if self.config.fallback:
                    return self.config.fallback(*args, **kwargs)
                raise ServiceUnavailableException(f"Service is unavailable (circuit breaker '{self.name}' is OPEN)")
            try:
                result = func(*args, **kwargs)
                self._on_success()
                return result
            except Exception as e:
                self._on_failure(e)
                raise
        return cast(F, wrapper)
    def async_call(self, func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            self.check_state()
            if self.state == CircuitState.OPEN:
                logger.warning(f"Circuit breaker '{self.name}' is OPEN - fast failing")
                if self.config.fallback:
                    if asyncio.iscoroutinefunction(self.config.fallback):
                        return await self.config.fallback(*args, **kwargs)
                    return self.config.fallback(*args, **kwargs)
                raise ServiceUnavailableException(f"Service is unavailable (circuit breaker '{self.name}' is OPEN)")
            try:
                result = await func(*args, **kwargs)
                self._on_success()
                return result
            except Exception as e:
                self._on_failure(e)
                raise
        return cast(F, wrapper)
def circuit_breaker(name: str, failure_threshold: int=5, success_threshold: int=3, timeout: float=60.0, exception_types: Optional[List[Type[Exception]]]=None, fallback: Optional[Callable]=None) -> Callable[[F], F]:
    if exception_types is None:
        exception_types = [Exception]
    config = CircuitBreakerConfig(failure_threshold=failure_threshold, success_threshold=success_threshold, timeout=timeout, exception_types=exception_types, fallback=fallback)
    breaker = CircuitBreaker.get_or_create(name, config)
    def decorator(func: F) -> F:
        if asyncio.iscoroutinefunction(func):
            return breaker.async_call(func)
        return breaker(func)
    return decorator