from __future__ import annotations

"""
Domain Events Backend Implementations.

This module implements the core event system functionality with different backend options,
providing the foundational components for the event service.
"""

import asyncio
import inspect
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Protocol

from app.core.events.exceptions import (
    EventBackendException,
    EventConfigurationException,
)
from app.logging import get_logger

logger = get_logger("app.core.events.backend")

# Type definitions
EventHandler = Callable[[Dict[str, Any]], Any]


class EventBackendType(Enum):
    """Supported types of event backends."""

    CELERY = auto()
    MEMORY = auto()


class EventPublisher(Protocol):
    """Protocol defining the event publishing interface."""

    def publish_event(self, event_name: str, payload: Dict[str, Any]) -> None:
        """
        Publish an event with the given name and payload.

        Args:
            event_name: The name of the event
            payload: The event payload data
        """
        ...


class EventSubscriber(Protocol):
    """Protocol defining the event subscription interface."""

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        """
        Subscribe a handler to an event.

        Args:
            event_name: The name of the event to subscribe to
            handler: The function to call when the event occurs
        """
        ...


class EventBackend(ABC, EventPublisher, EventSubscriber):
    """Abstract base class for event backends."""

    @abstractmethod
    def publish_event(self, event_name: str, payload: Dict[str, Any]) -> None:
        """Publish an event with the given name and payload."""
        pass

    @abstractmethod
    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        """Subscribe a handler to an event."""
        pass


class CeleryEventBackend(EventBackend):
    """Event backend implementation using Celery."""

    def __init__(self, celery_app: Any) -> None:
        """
        Initialize the Celery event backend.

        Args:
            celery_app: The Celery application instance
        """
        self.celery_app = celery_app
        self.logger = get_logger("app.core.events.backend.celery")

    def publish_event(self, event_name: str, payload: Dict[str, Any]) -> None:
        """
        Publish an event with the given name and payload using Celery.

        Args:
            event_name: The name of the event
            payload: The event payload data

        Raises:
            EventBackendException: If there's an error publishing the event
        """
        try:
            task_name = f"domain_events.{event_name}"
            self.logger.info(f"Publishing domain event {event_name} with Celery")
            self.celery_app.send_task(task_name, kwargs={"payload": payload})
        except Exception as e:
            self.logger.error(
                f"Error publishing event {event_name} with Celery: {str(e)}",
                exc_info=True,
            )
            raise EventBackendException(
                message=f"Failed to publish event {event_name} with Celery",
                backend_type="celery",
                original_exception=e,
            ) from e

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        """
        Subscribe a handler to an event using Celery.

        Args:
            event_name: The name of the event to subscribe to
            handler: The function to call when the event occurs

        Raises:
            EventBackendException: If there's an error subscribing to the event
        """
        try:
            task_name = f"domain_events.{event_name}"
            if task_name in self.celery_app.tasks:
                self.logger.debug(f"Handler for {event_name} already registered")
                return

            @self.celery_app.task(name=task_name)
            def task_handler(payload: Dict[str, Any]) -> Any:
                self.logger.info(f"Handling domain event {event_name} with Celery")
                if inspect.iscoroutinefunction(handler):
                    return asyncio.run(handler(payload))
                return handler(payload)

            self.logger.info(f"Registered handler for {event_name} with Celery")
        except Exception as e:
            self.logger.error(
                f"Error subscribing to event {event_name} with Celery: {str(e)}",
                exc_info=True,
            )
            raise EventBackendException(
                message=f"Failed to subscribe to event {event_name} with Celery",
                backend_type="celery",
                original_exception=e,
            ) from e


class MemoryEventBackend(EventBackend):
    """Event backend implementation using in-memory handlers."""

    def __init__(self) -> None:
        """Initialize the in-memory event backend."""
        self.handlers: Dict[str, List[EventHandler]] = {}
        self.logger = get_logger("app.core.events.backend.memory")

    def publish_event(self, event_name: str, payload: Dict[str, Any]) -> None:
        """
        Publish an event with the given name and payload in-memory.

        Args:
            event_name: The name of the event
            payload: The event payload data

        Raises:
            EventBackendException: If there's an error publishing the event
        """
        try:
            self.logger.info(f"Publishing domain event {event_name} in-memory")
            if event_name not in self.handlers:
                self.logger.debug(f"No handlers for event {event_name}")
                return

            for handler in self.handlers[event_name]:
                try:
                    if inspect.iscoroutinefunction(handler):
                        asyncio.create_task(handler(payload))
                    else:
                        handler(payload)
                except Exception as e:
                    self.logger.error(f"Error in event handler for {event_name}: {e}")
        except Exception as e:
            self.logger.error(
                f"Error publishing event {event_name} in-memory: {str(e)}",
                exc_info=True,
            )
            raise EventBackendException(
                message=f"Failed to publish event {event_name} in-memory",
                backend_type="memory",
                original_exception=e,
            ) from e

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        """
        Subscribe a handler to an event in-memory.

        Args:
            event_name: The name of the event to subscribe to
            handler: The function to call when the event occurs

        Raises:
            EventBackendException: If there's an error subscribing to the event
        """
        try:
            self.logger.info(f"Subscribing handler to {event_name} in-memory")
            if event_name not in self.handlers:
                self.handlers[event_name] = []
            self.handlers[event_name].append(handler)
        except Exception as e:
            self.logger.error(
                f"Error subscribing to event {event_name} in-memory: {str(e)}",
                exc_info=True,
            )
            raise EventBackendException(
                message=f"Failed to subscribe to event {event_name} in-memory",
                backend_type="memory",
                original_exception=e,
            ) from e


# Global state
_event_backend: Optional[EventBackend] = None
_pending_handlers: Dict[str, List[EventHandler]] = {}
_is_initialized = False


def get_event_backend() -> EventBackend:
    """
    Get the current event backend.

    Returns:
        EventBackend: The current event backend

    Raises:
        EventConfigurationException: If the event backend is not initialized
    """
    if _event_backend is None:
        logger.error("Event backend accessed before initialization")
        raise EventConfigurationException(
            message="Event backend not initialized. Call init_event_backend first."
        )
    return _event_backend


def init_event_backend(backend_type: EventBackendType, **kwargs: Any) -> EventBackend:
    """
    Initialize the event backend.

    Args:
        backend_type: The type of event backend to use
        **kwargs: Additional configuration options for the backend

    Returns:
        EventBackend: The initialized event backend

    Raises:
        EventConfigurationException: If there's an error initializing the backend
    """
    global _event_backend, _is_initialized

    if _is_initialized:
        logger.warning("Event backend already initialized")
        return _event_backend

    logger.info(f"Initializing event backend: {backend_type.name}")

    try:
        if backend_type == EventBackendType.CELERY:
            from app.core.celery_app import celery_app

            _event_backend = CeleryEventBackend(celery_app)
        elif backend_type == EventBackendType.MEMORY:
            _event_backend = MemoryEventBackend()
        else:
            raise ValueError(f"Unsupported event backend type: {backend_type}")

        _is_initialized = True
        logger.info(f"Event backend initialized: {backend_type.name}")
        return _event_backend
    except ImportError as e:
        logger.error(
            f"Failed to import required module for {backend_type.name} backend: {str(e)}"
        )
        raise EventConfigurationException(
            message=f"Failed to initialize {backend_type.name} backend: {str(e)}",
            details={"backend_type": backend_type.name},
            original_exception=e,
        ) from e
    except Exception as e:
        logger.error(
            f"Error initializing {backend_type.name} backend: {str(e)}", exc_info=True
        )
        raise EventConfigurationException(
            message=f"Failed to initialize {backend_type.name} backend: {str(e)}",
            details={"backend_type": backend_type.name},
            original_exception=e,
        ) from e


def publish_event(event_name: str, payload: Dict[str, Any]) -> None:
    """
    Publish an event with the given name and payload.

    Args:
        event_name: The name of the event
        payload: The event payload data

    Raises:
        EventConfigurationException: If the event backend is not initialized
        EventBackendException: If there's an error publishing the event
    """
    backend = get_event_backend()
    backend.publish_event(event_name, payload)


def subscribe_to_event(event_name: str) -> Callable[[EventHandler], EventHandler]:
    """
    Decorator to subscribe a function to an event.

    Args:
        event_name: The name of the event to subscribe to

    Returns:
        Decorator function that registers the handler

    Raises:
        EventConfigurationException: If there's an error with the event configuration
    """

    def decorator(handler: EventHandler) -> EventHandler:
        global _pending_handlers, _is_initialized, _event_backend

        if event_name not in _pending_handlers:
            _pending_handlers[event_name] = []

        _pending_handlers[event_name].append(handler)
        logger.debug(f"Queued handler {handler.__name__} for event {event_name}")

        if _is_initialized and _event_backend is not None:
            try:
                _event_backend.subscribe(event_name, handler)
                logger.debug(
                    f"Registered handler {handler.__name__} for event {event_name}"
                )
            except Exception as e:
                logger.error(f"Error registering handler: {str(e)}")
                raise EventConfigurationException(
                    message=f"Failed to register handler for {event_name}: {str(e)}",
                    details={"event_name": event_name, "handler": handler.__name__},
                    original_exception=e,
                ) from e

        return handler

    return decorator


def init_domain_events() -> None:
    """
    Initialize domain event handlers.

    This function registers all pending event handlers with the event backend
    and imports domain event modules.

    Raises:
        EventConfigurationException: If the event backend is not initialized or
            there's an error initializing domain events
    """
    global _event_backend, _is_initialized, _pending_handlers

    if not _is_initialized or _event_backend is None:
        logger.error("Cannot initialize domain events: Event backend not initialized")
        raise EventConfigurationException(
            message="Event backend not initialized. Call init_event_backend first."
        )

    try:
        logger.info("Registering domain event handlers")

        for event_name, handlers in _pending_handlers.items():
            for handler in handlers:
                try:
                    logger.debug(
                        f"Registering handler {handler.__name__} for event {event_name}"
                    )
                    _event_backend.subscribe(event_name, handler)
                except Exception as e:
                    logger.error(
                        f"Error registering handler for {event_name}: {str(e)}"
                    )
                    raise EventConfigurationException(
                        message=f"Failed to register handler for {event_name}: {str(e)}",
                        details={"event_name": event_name, "handler": handler.__name__},
                        original_exception=e,
                    ) from e

        _import_event_handlers()

        logger.info(
            f"Registered {sum(len(handlers) for handlers in _pending_handlers.values())} event handlers"
        )
    except Exception as e:
        if not isinstance(e, EventConfigurationException):
            logger.error(f"Error initializing domain events: {str(e)}", exc_info=True)
            raise EventConfigurationException(
                message=f"Failed to initialize domain events: {str(e)}",
                original_exception=e,
            ) from e
        raise


def _import_event_handlers() -> None:
    """
    Import event handler modules.

    This function attempts to import domain-specific event handler modules
    to ensure their handlers are registered.
    """
    logger.debug("Importing domain event handler modules")

    try:
        import importlib

        # Modules that might contain event handlers
        modules_to_import = [
            "app.domains.products.handlers",
            "app.domains.orders.handlers",
            "app.domains.inventory.handlers",
            "app.domains.users.events",  # Our new example module
        ]

        for module_name in modules_to_import:
            try:
                importlib.import_module(module_name)
                logger.debug(f"Imported event handlers from {module_name}")
            except ImportError:
                logger.debug(
                    f"Could not import event handlers from {module_name} (module may not exist)"
                )
    except Exception as e:
        logger.warning(f"Error importing event handler modules: {str(e)}")
