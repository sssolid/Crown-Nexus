# app/core/events/init.py
from __future__ import annotations

"""
Event system initialization module.

This module handles the initialization of the event system and registration
of domain event handlers.
"""

import asyncio
import importlib
import inspect
from app.logging import get_logger
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Protocol

# Logger
logger = get_logger("app.core.events.init")

# Event handler type
EventHandler = Callable[[Dict[str, Any]], Any]


class EventBackendType(Enum):
    """Types of event backends supported."""

    CELERY = auto()
    MEMORY = auto()
    # Add other backend types as needed (like REDIS, KAFKA, etc.)


class EventPublisher(Protocol):
    """Protocol defining the interface for publishing events."""

    def publish_event(self, event_name: str, payload: Dict[str, Any]) -> None:
        """Publish an event to subscribers.

        Args:
            event_name: The name of the event to publish
            payload: Event data to be sent to subscribers
        """
        ...


class EventSubscriber(Protocol):
    """Protocol defining the interface for subscribing to events."""

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        """Subscribe a handler to an event.

        Args:
            event_name: The name of the event to subscribe to
            handler: The function to call when the event is published
        """
        ...


class EventBackend(ABC, EventPublisher, EventSubscriber):
    """Abstract base class for event backend implementations."""

    @abstractmethod
    def publish_event(self, event_name: str, payload: Dict[str, Any]) -> None:
        """Publish an event to subscribers.

        Args:
            event_name: The name of the event to publish
            payload: Event data to be sent to subscribers
        """
        pass

    @abstractmethod
    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        """Subscribe a handler to an event.

        Args:
            event_name: The name of the event to subscribe to
            handler: The function to call when the event is published
        """
        pass


class CeleryEventBackend(EventBackend):
    """Celery implementation of the event backend."""

    def __init__(self, celery_app: Any) -> None:
        """Initialize with a Celery application.

        Args:
            celery_app: The Celery application instance
        """
        self.celery_app = celery_app
        self.logger = get_logger("app.core.events.init")

    def publish_event(self, event_name: str, payload: Dict[str, Any]) -> None:
        """Publish an event using Celery tasks.

        Args:
            event_name: The name of the event to publish
            payload: Event data to be sent to subscribers
        """
        task_name = f"domain_events.{event_name}"
        self.logger.info(f"Publishing domain event {event_name} with Celery")
        self.celery_app.send_task(task_name, kwargs={"payload": payload})

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        """Subscribe a handler to an event using Celery task decoration.

        Args:
            event_name: The name of the event to subscribe to
            handler: The function to call when the event is published
        """
        task_name = f"domain_events.{event_name}"

        # Skip if already registered
        if task_name in self.celery_app.tasks:
            self.logger.debug(f"Handler for {event_name} already registered")
            return

        # Create Celery task for this handler
        @self.celery_app.task(name=task_name)
        def task_handler(payload: Dict[str, Any]) -> Any:
            self.logger.info(f"Handling domain event {event_name} with Celery")

            # If handler is async, we need to run it in an event loop
            if inspect.iscoroutinefunction(handler):
                return asyncio.run(handler(payload))

            return handler(payload)

        self.logger.info(f"Registered handler for {event_name} with Celery")


class MemoryEventBackend(EventBackend):
    """In-memory implementation of the event backend for testing or simple apps."""

    def __init__(self) -> None:
        """Initialize the in-memory event registry."""
        self.handlers: Dict[str, List[EventHandler]] = {}
        self.logger = get_logger("app.core.events.init")

    def publish_event(self, event_name: str, payload: Dict[str, Any]) -> None:
        """Publish an event to all subscribers immediately in-process.

        Args:
            event_name: The name of the event to publish
            payload: Event data to be sent to subscribers
        """
        self.logger.info(f"Publishing domain event {event_name} in-memory")

        if event_name not in self.handlers:
            self.logger.debug(f"No handlers for event {event_name}")
            return

        for handler in self.handlers[event_name]:
            try:
                # If handler is async, we need to run it in an event loop
                if inspect.iscoroutinefunction(handler):
                    asyncio.create_task(handler(payload))
                else:
                    handler(payload)
            except Exception as e:
                self.logger.error(f"Error in event handler for {event_name}: {e}")

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        """Subscribe a handler to an event for in-memory processing.

        Args:
            event_name: The name of the event to subscribe to
            handler: The function to call when the event is published
        """
        self.logger.info(f"Subscribing handler to {event_name} in-memory")

        if event_name not in self.handlers:
            self.handlers[event_name] = []

        self.handlers[event_name].append(handler)


# Global event backend instance and pending handlers
_event_backend: Optional[EventBackend] = None
_pending_handlers: Dict[str, List[EventHandler]] = {}
_is_initialized = False


def init_event_backend(backend_type: EventBackendType, **kwargs: Any) -> None:
    """
    Initialize the event backend.

    Args:
        backend_type: Type of event backend to use
        **kwargs: Additional arguments for the backend
    """
    global _event_backend, _is_initialized

    if _is_initialized:
        logger.warning("Event backend already initialized")
        return

    logger.info(f"Initializing event backend: {backend_type.name}")

    if backend_type == EventBackendType.CELERY:
        # Dynamically import celery to avoid hard dependency
        from app.core.celery_app import celery_app

        _event_backend = CeleryEventBackend(celery_app)
    elif backend_type == EventBackendType.MEMORY:
        _event_backend = MemoryEventBackend()
    else:
        raise ValueError(f"Unsupported event backend type: {backend_type}")

    _is_initialized = True
    logger.info(f"Event backend initialized: {backend_type.name}")


def get_event_backend() -> EventBackend:
    """
    Get the configured event backend.

    Returns:
        The configured event backend instance

    Raises:
        RuntimeError: If event backend is not initialized
    """
    if _event_backend is None:
        raise RuntimeError(
            "Event backend not initialized. Call init_event_backend first."
        )
    return _event_backend


def subscribe_to_event(event_name: str) -> Callable[[EventHandler], EventHandler]:
    """
    Decorator to register a handler for a domain event.

    During application initialization, this will store the handler for later registration.
    After the event system is initialized, handlers will be registered with the backend.

    Args:
        event_name: Name of the event to subscribe to

    Returns:
        Decorator function
    """

    def decorator(handler: EventHandler) -> EventHandler:
        # Store the handler for deferred registration
        if event_name not in _pending_handlers:
            _pending_handlers[event_name] = []

        _pending_handlers[event_name].append(handler)
        logger.debug(f"Queued handler {handler.__name__} for event {event_name}")

        # If backend is already initialized, register immediately
        if _is_initialized and _event_backend is not None:
            _event_backend.subscribe(event_name, handler)
            logger.debug(
                f"Registered handler {handler.__name__} for event {event_name}"
            )

        return handler

    return decorator


def init_domain_events() -> None:
    """
    Initialize domain events by registering all pending handlers.

    This should be called after the event backend is initialized.
    """
    global _event_backend

    if not _is_initialized or _event_backend is None:
        raise RuntimeError(
            "Event backend not initialized. Call init_event_backend first."
        )

    logger.info("Registering domain event handlers")

    # Register all pending handlers
    for event_name, handlers in _pending_handlers.items():
        for handler in handlers:
            logger.debug(
                f"Registering handler {handler.__name__} for event {event_name}"
            )
            _event_backend.subscribe(event_name, handler)

    # Import domain event modules to trigger decorator execution
    _import_event_handlers()

    logger.info(
        f"Registered {sum(len(handlers) for handlers in _pending_handlers.values())} event handlers"
    )


def publish_event(event_name: str, payload: Dict[str, Any]) -> None:
    """
    Publish a domain event.

    Args:
        event_name: The name of the event to publish
        payload: Event data to be sent to subscribers
    """
    backend = get_event_backend()
    backend.publish_event(event_name, payload)


def _import_event_handlers() -> None:
    """Import all domain event handler modules."""
    # Import event handlers from domains
    try:
        # These imports will cause the handler decorators to execute
        import app.domains.products.handlers

        # Add more domain handler imports as needed
        # Try to import other handlers, but don't fail if modules don't exist
        try:
            import app.domains.orders.handlers
        except ImportError:
            pass

        try:
            import app.domains.inventory.handlers
        except ImportError:
            pass

        logger.debug("Imported domain event handler modules")
    except Exception as e:
        logger.warning(f"Error importing event handler modules: {str(e)}")
