# /backend/app/utils/circuit_breaker.py
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

logger = get_logger("app.utils.circuit_breaker")

class CircuitState(enum.Enum):
    """Circuit breaker states.
    
    The circuit breaker can be in one of three states:
    - CLOSED: Normal operation, requests are allowed
    - OPEN: Circuit is broken, all requests fail immediately
    - HALF_OPEN: Allowing a limited number of test requests to check if the service is back
    """
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

@dataclass
class CircuitBreakerConfig:
    """Circuit breaker configuration.
    
    This class holds the configuration for a circuit breaker.
    
    Attributes:
        failure_threshold: Number of failures before opening the circuit
        success_threshold: Number of successes before closing the circuit
        timeout: Time in seconds to wait before transitioning from OPEN to HALF_OPEN
        exception_types: Types of exceptions that increment the failure counter
        fallback: Optional fallback function to call when the circuit is open
    """
    failure_threshold: int = 5
    success_threshold: int = 3
    timeout: float = 60.0
    exception_types: List[Type[Exception]] = field(default_factory=lambda: [Exception])
    fallback: Optional[Callable] = None

class CircuitBreaker:
    """Circuit breaker implementation.
    
    This class implements the circuit breaker pattern, which prevents
    an application from repeatedly trying to execute an operation that's
    likely to fail, allowing it to continue without waiting for the fault
    to be fixed or wasting resources while the fault is being fixed.
    
    Attributes:
        name: Unique name for this circuit breaker
        config: Circuit breaker configuration
        state: Current circuit state
        failure_count: Count of consecutive failures
        success_count: Count of consecutive successes
        last_failure_time: Time of last failure
        last_state_change_time: Time of last state change
    """
    
    # Class-level storage for circuit breakers
    _breakers: Dict[str, CircuitBreaker] = {}
    _lock = RLock()
    
    def __init__(
        self,
        name: str,
        config: Optional[CircuitBreakerConfig] = None
    ) -> None:
        """Initialize the circuit breaker.
        
        Args:
            name: Unique name for this circuit breaker
            config: Circuit breaker configuration
        """
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = 0.0
        self.last_state_change_time = time.time()
        
        # Store in class-level storage
        with self._lock:
            self._breakers[name] = self
        
    @classmethod
    def get(cls, name: str) -> CircuitBreaker:
        """Get a circuit breaker by name.
        
        Args:
            name: Circuit breaker name
            
        Returns:
            CircuitBreaker: Circuit breaker instance
            
        Raises:
            ValueError: If circuit breaker not found
        """
        with cls._lock:
            if name not in cls._breakers:
                raise ValueError(f"Circuit breaker not found: {name}")
            return cls._breakers[name]
            
    @classmethod
    def get_or_create(
        cls,
        name: str,
        config: Optional[CircuitBreakerConfig] = None
    ) -> CircuitBreaker:
        """Get a circuit breaker by name or create it if it doesn't exist.
        
        Args:
            name: Circuit breaker name
            config: Circuit breaker configuration
            
        Returns:
            CircuitBreaker: Circuit breaker instance
        """
        with cls._lock:
            if name not in cls._breakers:
                return cls(name, config)
            return cls._breakers[name]
            
    @classmethod
    def reset_all(cls) -> None:
        """Reset all circuit breakers."""
        with cls._lock:
            for breaker in cls._breakers.values():
                breaker.reset()
                
    @classmethod
    def get_all_states(cls) -> Dict[str, CircuitState]:
        """Get the states of all circuit breakers.
        
        Returns:
            Dict[str, CircuitState]: Dictionary of circuit breaker names and states
        """
        with cls._lock:
            return {name: breaker.state for name, breaker in cls._breakers.items()}
            
    def reset(self) -> None:
        """Reset the circuit breaker to its initial state."""
        with self._lock:
            self.state = CircuitState.CLOSED
            self.failure_count = 0
            self.success_count = 0
            self.last_failure_time = 0.0
            self.last_state_change_time = time.time()
            
    def check_state(self) -> None:
        """Check and update the circuit breaker state.
        
        This method checks if the circuit breaker should transition to a new state
        based on its current state and the elapsed time since the last state change.
        """
        with self._lock:
            # Check if we need to transition from OPEN to HALF_OPEN
            if self.state == CircuitState.OPEN:
                elapsed = time.time() - self.last_failure_time
                if elapsed >= self.config.timeout:
                    self._transition_to(CircuitState.HALF_OPEN)
                    
    def _transition_to(self, new_state: CircuitState) -> None:
        """Transition to a new state.
        
        Args:
            new_state: New circuit state
        """
        if self.state != new_state:
            logger.info(
                f"Circuit breaker '{self.name}' transitioning from {self.state.value} to {new_state.value}"
            )
            self.state = new_state
            self.last_state_change_time = time.time()
            
            # Reset counters on state change
            if new_state == CircuitState.CLOSED:
                self.failure_count = 0
            elif new_state == CircuitState.OPEN:
                self.success_count = 0
            elif new_state == CircuitState.HALF_OPEN:
                self.failure_count = 0
                self.success_count = 0
                
    def _on_success(self) -> None:
        """Handle a successful execution."""
        with self._lock:
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.config.success_threshold:
                    self._transition_to(CircuitState.CLOSED)
            elif self.state == CircuitState.CLOSED:
                self.failure_count = 0  # Reset failure count on success
                
    def _on_failure(self, exception: Exception) -> None:
        """Handle a failed execution.
        
        Args:
            exception: The exception that caused the failure
        """
        with self._lock:
            self.last_failure_time = time.time()
            
            # Only count if exception is of a tracked type
            if not any(isinstance(exception, exc_type) for exc_type in self.config.exception_types):
                return
                
            if self.state == CircuitState.CLOSED:
                self.failure_count += 1
                if self.failure_count >= self.config.failure_threshold:
                    self._transition_to(CircuitState.OPEN)
            elif self.state == CircuitState.HALF_OPEN:
                self._transition_to(CircuitState.OPEN)
                
    def __call__(self, func: F) -> F:
        """Decorate a function with circuit breaker.
        
        Args:
            func: Function to decorate
            
        Returns:
            F: Decorated function
        """
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Check if circuit is open
            self.check_state()
            
            if self.state == CircuitState.OPEN:
                logger.warning(f"Circuit breaker '{self.name}' is OPEN - fast failing")
                if self.config.fallback:
                    return self.config.fallback(*args, **kwargs)
                raise ServiceUnavailableException(
                    f"Service is unavailable (circuit breaker '{self.name}' is OPEN)"
                )
                
            try:
                # Execute function
                result = func(*args, **kwargs)
                self._on_success()
                return result
            except Exception as e:
                self._on_failure(e)
                raise
                
        return cast(F, wrapper)
        
    def async_call(self, func: F) -> F:
        """Decorate an async function with circuit breaker.
        
        Args:
            func: Async function to decorate
            
        Returns:
            F: Decorated async function
        """
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Check if circuit is open
            self.check_state()
            
            if self.state == CircuitState.OPEN:
                logger.warning(f"Circuit breaker '{self.name}' is OPEN - fast failing")
                if self.config.fallback:
                    if asyncio.iscoroutinefunction(self.config.fallback):
                        return await self.config.fallback(*args, **kwargs)
                    return self.config.fallback(*args, **kwargs)
                raise ServiceUnavailableException(
                    f"Service is unavailable (circuit breaker '{self.name}' is OPEN)"
                )
                
            try:
                # Execute function
                result = await func(*args, **kwargs)
                self._on_success()
                return result
            except Exception as e:
                self._on_failure(e)
                raise
                
        return cast(F, wrapper)

def circuit_breaker(
    name: str,
    failure_threshold: int = 5,
    success_threshold: int = 3,
    timeout: float = 60.0,
    exception_types: Optional[List[Type[Exception]]] = None,
    fallback: Optional[Callable] = None
) -> Callable[[F], F]:
    """Circuit breaker decorator.
    
    This decorator applies the circuit breaker pattern to a function.
    
    Args:
        name: Circuit breaker name
        failure_threshold: Number of failures before opening the circuit
        success_threshold: Number of successes before closing the circuit
        timeout: Time in seconds to wait before transitioning from OPEN to HALF_OPEN
        exception_types: Types of exceptions that increment the failure counter
        fallback: Optional fallback function to call when the circuit is open
        
    Returns:
        Callable: Function decorator
    """
    # Set default exception types
    if exception_types is None:
        exception_types = [Exception]
        
    # Create config
    config = CircuitBreakerConfig(
        failure_threshold=failure_threshold,
        success_threshold=success_threshold,
        timeout=timeout,
        exception_types=exception_types,
        fallback=fallback
    )
    
    # Get or create circuit breaker
    breaker = CircuitBreaker.get_or_create(name, config)
    
    def decorator(func: F) -> F:
        if asyncio.iscoroutinefunction(func):
            return breaker.async_call(func)
        return breaker(func)
        
    return decorator
