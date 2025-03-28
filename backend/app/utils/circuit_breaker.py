# app/utils/circuit_breaker.py
"""
Circuit breaker implementation for preventing cascading failures.

This module implements the circuit breaker design pattern to prevent cascading failures
in distributed systems. It automatically detects failures and temporarily blocks operations
that are likely to fail, allowing the failing component to recover.

Features include:
- Configurable failure threshold, success threshold, and timeout
- Three states: CLOSED (normal), OPEN (blocking), and HALF-OPEN (testing)
- Support for both synchronous and asynchronous functions
- Registry of named circuit breakers for centralized management
- Fallback function support for graceful degradation

All functions include proper error handling, logging, and state management to ensure
system resilience and fail gracefully when downstream services are unavailable.
"""

from __future__ import annotations

import asyncio
import enum
import functools
import time
from dataclasses import dataclass, field
from threading import RLock
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Type,
    TypeVar,
    cast,
)

from app.core.exceptions import (
    ServiceException,
    ErrorCode,
)
from app.logging import get_logger

# Initialize structured logger
logger = get_logger("app.utils.circuit_breaker")

# Type variables
F = TypeVar("F", bound=Callable[..., Any])
T = TypeVar("T")


class CircuitState(enum.Enum):
    """Possible states of a circuit breaker."""

    CLOSED = "closed"  # Normal operation, requests are allowed
    OPEN = "open"  # Failed state, requests are blocked
    HALF_OPEN = "half_open"  # Testing state, limited requests to check recovery


@dataclass
class CircuitBreakerConfig:
    """Configuration options for circuit breaker behavior."""

    # Number of consecutive failures to open the circuit
    failure_threshold: int = 5

    # Number of consecutive successes to close the circuit
    success_threshold: int = 3

    # Time in seconds after which to try HALF_OPEN when OPEN
    timeout: float = 60.0

    # Types of exceptions that should trigger the circuit breaker
    exception_types: List[Type[Exception]] = field(default_factory=lambda: [Exception])

    # Optional fallback function to call when circuit is open
    fallback: Optional[Callable] = None


class CircuitBreaker:
    """Circuit breaker implementation to prevent cascading failures."""

    # Registry of all circuit breakers by name
    _breakers: Dict[str, CircuitBreaker] = {}

    # Thread-safe lock for registry access
    _lock = RLock()

    def __init__(
        self, name: str, config: Optional[CircuitBreakerConfig] = None
    ) -> None:
        """Initialize a new circuit breaker.

        Args:
            name: Unique name for this circuit breaker
            config: Configuration options, or None for defaults
        """
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = 0.0
        self.last_state_change_time = time.time()

        # Register this circuit breaker in the registry
        with self._lock:
            self._breakers[name] = self
            logger.info(
                f"Circuit breaker '{name}' initialized",
                state=self.state.value,
                failure_threshold=self.config.failure_threshold,
                success_threshold=self.config.success_threshold,
                timeout=self.config.timeout,
            )

    @classmethod
    def get(cls, name: str) -> CircuitBreaker:
        """Get an existing circuit breaker by name.

        Args:
            name: Name of the circuit breaker

        Returns:
            CircuitBreaker: The named circuit breaker

        Raises:
            ValueError: If no circuit breaker with that name exists
        """
        with cls._lock:
            if name not in cls._breakers:
                msg = f"Circuit breaker not found: {name}"
                logger.error(msg)
                raise ValueError(msg)
            return cls._breakers[name]

    @classmethod
    def get_or_create(
        cls, name: str, config: Optional[CircuitBreakerConfig] = None
    ) -> CircuitBreaker:
        """Get an existing circuit breaker or create a new one.

        Args:
            name: Name of the circuit breaker
            config: Configuration options for new breaker, or None for defaults

        Returns:
            CircuitBreaker: The named circuit breaker
        """
        with cls._lock:
            if name not in cls._breakers:
                logger.info(f"Creating new circuit breaker: {name}")
                return cls(name, config)

            logger.debug(f"Returning existing circuit breaker: {name}")
            return cls._breakers[name]

    @classmethod
    def reset_all(cls) -> None:
        """Reset all circuit breakers to CLOSED state."""
        with cls._lock:
            for name, breaker in cls._breakers.items():
                logger.info(f"Resetting circuit breaker: {name}")
                breaker.reset()

    @classmethod
    def get_all_states(cls) -> Dict[str, CircuitState]:
        """Get the current state of all circuit breakers.

        Returns:
            Dict[str, CircuitState]: Map of circuit breaker names to states
        """
        with cls._lock:
            return {name: breaker.state for name, breaker in cls._breakers.items()}

    def reset(self) -> None:
        """Reset this circuit breaker to CLOSED state."""
        with self._lock:
            old_state = self.state
            self.state = CircuitState.CLOSED
            self.failure_count = 0
            self.success_count = 0
            self.last_failure_time = 0.0
            self.last_state_change_time = time.time()
            logger.info(
                f"Circuit breaker '{self.name}' reset",
                old_state=old_state.value,
                new_state=self.state.value,
            )

    def check_state(self) -> None:
        """Check if circuit state should change based on time elapsed.

        If in OPEN state and timeout has elapsed, transitions to HALF_OPEN.
        """
        with self._lock:
            if self.state == CircuitState.OPEN:
                elapsed = time.time() - self.last_failure_time
                if elapsed >= self.config.timeout:
                    logger.info(
                        f"Circuit breaker '{self.name}' timeout elapsed ({elapsed:.2f}s)",
                        old_state=self.state.value,
                        timeout=self.config.timeout,
                    )
                    self._transition_to(CircuitState.HALF_OPEN)

    def _transition_to(self, new_state: CircuitState) -> None:
        """Transition to a new state with appropriate state reset.

        Args:
            new_state: The state to transition to
        """
        if self.state != new_state:
            logger.info(
                f"Circuit breaker '{self.name}' transitioning from {self.state.value} to {new_state.value}",
                old_state=self.state.value,
                new_state=new_state.value,
            )
            self.state = new_state
            self.last_state_change_time = time.time()

            # Reset appropriate counters based on new state
            if new_state == CircuitState.CLOSED:
                self.failure_count = 0
            elif new_state == CircuitState.OPEN:
                self.success_count = 0
            elif new_state == CircuitState.HALF_OPEN:
                self.failure_count = 0
                self.success_count = 0

    def _on_success(self) -> None:
        """Handle successful execution.

        Increment success counter and potentially transition state.
        """
        with self._lock:
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                logger.debug(
                    f"Circuit breaker '{self.name}' success in HALF_OPEN state",
                    success_count=self.success_count,
                    threshold=self.config.success_threshold,
                )

                # Check if success threshold reached to close circuit
                if self.success_count >= self.config.success_threshold:
                    self._transition_to(CircuitState.CLOSED)
            elif self.state == CircuitState.CLOSED:
                # Reset failure count on success when closed
                self.failure_count = 0

    def _on_failure(self, exception: Exception) -> None:
        """Handle execution failure.

        Update failure counter, timestamp, and potentially transition state.

        Args:
            exception: The exception that occurred
        """
        with self._lock:
            self.last_failure_time = time.time()

            # Check if exception type should trigger circuit breaker
            if not any(
                isinstance(exception, exc_type)
                for exc_type in self.config.exception_types
            ):
                logger.debug(
                    f"Circuit breaker '{self.name}' ignoring exception type: {type(exception).__name__}"
                )
                return

            if self.state == CircuitState.CLOSED:
                self.failure_count += 1
                logger.debug(
                    f"Circuit breaker '{self.name}' failure in CLOSED state",
                    failure_count=self.failure_count,
                    threshold=self.config.failure_threshold,
                )

                # Check if failure threshold reached to open circuit
                if self.failure_count >= self.config.failure_threshold:
                    self._transition_to(CircuitState.OPEN)
            elif self.state == CircuitState.HALF_OPEN:
                # Any failure in HALF_OPEN state opens the circuit again
                logger.info(
                    f"Circuit breaker '{self.name}' failure in HALF_OPEN state",
                    error=str(exception),
                )
                self._transition_to(CircuitState.OPEN)

    def __call__(self, func: F) -> F:
        """Decorate function with circuit breaker (synchronous version).

        Args:
            func: The function to wrap with circuit breaker

        Returns:
            F: Wrapped function
        """

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Check if state should change based on elapsed time
            self.check_state()

            # Fast fail if circuit is open
            if self.state == CircuitState.OPEN:
                logger.warning(f"Circuit breaker '{self.name}' is OPEN - fast failing")

                # Use fallback if configured
                if self.config.fallback:
                    return self.config.fallback(*args, **kwargs)

                # Otherwise raise service unavailable exception
                raise ServiceException(
                    message=f"Service is unavailable (circuit breaker '{self.name}' is OPEN)",
                )

            try:
                # Execute function
                result = func(*args, **kwargs)

                # Handle success
                self._on_success()
                return result
            except Exception as e:
                # Handle failure
                self._on_failure(e)
                raise

        return cast(F, wrapper)

    def async_call(self, func: F) -> F:
        """Decorate async function with circuit breaker.

        Args:
            func: The async function to wrap with circuit breaker

        Returns:
            F: Wrapped async function
        """

        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Check if state should change based on elapsed time
            self.check_state()

            # Fast fail if circuit is open
            if self.state == CircuitState.OPEN:
                logger.warning(f"Circuit breaker '{self.name}' is OPEN - fast failing")

                # Use fallback if configured
                if self.config.fallback:
                    if asyncio.iscoroutinefunction(self.config.fallback):
                        return await self.config.fallback(*args, **kwargs)
                    return self.config.fallback(*args, **kwargs)

                # Otherwise raise service unavailable exception
                raise ServiceException(
                    message=f"Service is unavailable (circuit breaker '{self.name}' is OPEN)",
                )

            try:
                # Execute async function
                result = await func(*args, **kwargs)

                # Handle success
                self._on_success()
                return result
            except Exception as e:
                # Handle failure
                self._on_failure(e)
                raise

        return cast(F, wrapper)


def circuit_breaker(
    name: str,
    failure_threshold: int = 5,
    success_threshold: int = 3,
    timeout: float = 60.0,
    exception_types: Optional[List[Type[Exception]]] = None,
    fallback: Optional[Callable] = None,
) -> Callable[[F], F]:
    """Decorator factory for applying circuit breaker pattern.

    Args:
        name: Unique name for the circuit breaker
        failure_threshold: Number of failures before opening circuit
        success_threshold: Number of successes before closing circuit
        timeout: Seconds before trying again after circuit opens
        exception_types: List of exception types to count as failures
        fallback: Function to call when circuit is open

    Returns:
        Callable: Decorator function

    Examples:
        @circuit_breaker("payment_service", failure_threshold=3)
        def process_payment(order_id):
            ...

        @circuit_breaker("user_service", fallback=get_cached_user)
        async def get_user(user_id):
            ...
    """
    if exception_types is None:
        exception_types = [Exception]

    # Create config
    config = CircuitBreakerConfig(
        failure_threshold=failure_threshold,
        success_threshold=success_threshold,
        timeout=timeout,
        exception_types=exception_types,
        fallback=fallback,
    )

    # Get or create circuit breaker
    breaker = CircuitBreaker.get_or_create(name, config)

    def decorator(func: F) -> F:
        """Decorator that applies circuit breaker to function."""
        if asyncio.iscoroutinefunction(func):
            return breaker.async_call(func)
        return breaker(func)

    return decorator
