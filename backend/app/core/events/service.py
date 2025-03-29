from __future__ import annotations

"""
Event service implementation.

This module provides a service wrapper around the event system,
making it available through the dependency manager and integrating
with other application systems like metrics, error handling, and logging.
"""

import asyncio
import inspect
import time
from typing import Any, Callable, Dict, List, Optional, TypeVar, cast

from app.core.events.backend import (
    EventBackend,
    EventBackendType,
    EventHandler,
    get_event_backend,
    init_event_backend,
    init_domain_events,
    publish_event as backend_publish_event,
    subscribe_to_event as backend_subscribe_to_event,
)
from app.core.events.exceptions import (
    EventConfigurationException,
    EventPublishException,
    EventServiceException,
    EventHandlerException,
)
from app.logging import get_logger

logger = get_logger("app.core.events.service")

T = TypeVar("T")
Event = Dict[str, Any]

# Try to import metrics service if available
try:
    from app.core.dependency_manager import get_dependency

    HAS_METRICS = True
except ImportError:
    HAS_METRICS = False


class EventService:
    """
    Service for managing domain events in the application.

    This service provides:
    - Event publishing with metrics tracking
    - Subscription management
    - Integration with error handling, logging, and metrics
    - Advanced event filtering capabilities
    - Support for both sync and async event handlers
    """

    def __init__(self) -> None:
        """Initialize the event service."""
        self._initialized = False
        self._event_backend: Optional[EventBackend] = None
        self._default_context: Dict[str, Any] = {}

    async def initialize(
        self, backend_type: EventBackendType = EventBackendType.MEMORY
    ) -> None:
        """
        Initialize the event service with the specified backend.

        Args:
            backend_type: The type of event backend to use (MEMORY or CELERY)
        """
        if self._initialized:
            logger.debug("Event service already initialized, skipping")
            return

        logger.info(f"Initializing event service with {backend_type.name} backend")

        try:
            # Initialize the backend
            init_event_backend(backend_type)
            self._event_backend = get_event_backend()

            # Initialize domain events
            init_domain_events()

            # Register metrics if available
            if HAS_METRICS:
                try:
                    metrics_service = get_dependency("metrics_service")
                    metrics_service.create_counter(
                        "events_published_total",
                        "Total number of domain events published",
                        ["event_type", "backend"],
                    )
                    metrics_service.create_counter(
                        "event_handler_errors_total",
                        "Total number of errors in event handlers",
                        ["event_type", "handler"],
                    )
                    metrics_service.create_histogram(
                        "event_handler_duration_seconds",
                        "Time spent processing events in handlers",
                        ["event_type", "handler"],
                    )
                    logger.info("Event system metrics registered")
                except Exception as e:
                    logger.debug(f"Could not register event metrics: {str(e)}")

            self._initialized = True
            logger.info("Event service initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing event service: {str(e)}", exc_info=True)
            raise EventServiceException(
                message=f"Failed to initialize event service: {str(e)}",
                details={"backend_type": backend_type.name},
                original_exception=e,
            ) from e

    async def shutdown(self) -> None:
        """Shut down the event service."""
        if not self._initialized:
            return

        logger.info("Shutting down event service")
        # No specific shutdown needed for current backends
        self._initialized = False
        self._event_backend = None
        logger.info("Event service shut down")

    def set_default_context(self, context: Dict[str, Any]) -> None:
        """
        Set default context data to be included with all published events.

        Args:
            context: Dictionary of context data
        """
        self._default_context = context

    async def publish(
        self,
        event_name: str,
        payload: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Publish an event with the given name and payload.

        Args:
            event_name: The name of the event
            payload: The event payload data
            context: Additional context data for this event

        Raises:
            EventPublishException: If there's an error publishing the event
            EventServiceException: If the event service is not initialized
        """
        self._ensure_initialized()

        metrics_service = None
        start_time = time.monotonic()
        backend_type = "unknown"

        try:
            if HAS_METRICS:
                try:
                    metrics_service = get_dependency("metrics_service")
                except Exception as e:
                    logger.debug(f"Could not get metrics service: {str(e)}")

            if self._event_backend:
                backend_type = self._event_backend.__class__.__name__

            # Combine payload with default and event-specific context
            full_payload = {**self._default_context}
            if context:
                full_payload.update(context)
            full_payload["data"] = payload

            # Add timestamp if not present
            if "timestamp" not in full_payload:
                full_payload["timestamp"] = time.time()

            logger.info(
                f"Publishing event: {event_name}",
                event_name=event_name,
                payload_size=len(str(payload)),
                backend=backend_type,
            )

            # Publish the event
            backend_publish_event(event_name, full_payload)

            logger.debug(f"Event published: {event_name}", event_name=event_name)

        except Exception as e:
            logger.error(
                f"Error publishing event {event_name}: {str(e)}",
                exc_info=True,
                event_name=event_name,
            )
            raise EventPublishException(
                message=f"Failed to publish event {event_name}: {str(e)}",
                event_name=event_name,
                details={"payload_size": len(str(payload))},
                original_exception=e,
            ) from e

        finally:
            # Record metrics if available
            if metrics_service and HAS_METRICS:
                try:
                    duration = time.monotonic() - start_time
                    metrics_service.increment_counter(
                        "events_published_total",
                        1,
                        {"event_type": event_name, "backend": backend_type},
                    )
                    metrics_service.observe_histogram(
                        "event_publish_duration_seconds",
                        duration,
                        {"event_type": event_name, "backend": backend_type},
                    )
                except Exception as metrics_err:
                    logger.warning(
                        f"Failed to record event metrics: {str(metrics_err)}"
                    )

    def subscribe(self, event_name: str) -> Callable[[EventHandler], EventHandler]:
        """
        Decorator to subscribe a function to an event.

        Args:
            event_name: The name of the event to subscribe to

        Returns:
            Decorator function that registers the handler

        Example:
            @event_service.subscribe("user.created")
            async def handle_user_created(event):
                user_id = event["data"]["user_id"]
                # Process the event
        """
        return backend_subscribe_to_event(event_name)

    def event_handler(
        self,
        event_name: str,
        filter_func: Optional[Callable[[Dict[str, Any]], bool]] = None,
    ) -> Callable[[EventHandler], EventHandler]:
        """
        Advanced decorator to subscribe a function to an event with filtering.

        Args:
            event_name: The name of the event to subscribe to
            filter_func: Optional function to filter events before processing

        Returns:
            Decorator function that registers the handler

        Example:
            @event_service.event_handler(
                "order.status_changed",
                filter_func=lambda event: event["data"]["new_status"] == "completed"
            )
            async def handle_order_completed(event):
                order_id = event["data"]["order_id"]
                # Process completed orders
        """

        def decorator(handler: EventHandler) -> EventHandler:
            @backend_subscribe_to_event(event_name)
            async def wrapper(event: Dict[str, Any]) -> Any:
                metrics_service = None
                start_time = time.monotonic()
                handler_name = handler.__name__
                error = None

                try:
                    if HAS_METRICS:
                        try:
                            metrics_service = get_dependency("metrics_service")
                        except Exception as e:
                            logger.debug(f"Could not get metrics service: {str(e)}")

                    # Apply filter if provided
                    if filter_func and not filter_func(event):
                        logger.debug(
                            f"Event filtered out for handler {handler_name}",
                            event_name=event_name,
                            handler=handler_name,
                        )
                        return None

                    logger.debug(
                        f"Handling event {event_name} with {handler_name}",
                        event_name=event_name,
                        handler=handler_name,
                    )

                    # Invoke the handler with appropriate awaiting
                    if inspect.iscoroutinefunction(handler):
                        result = await handler(event)
                    else:
                        result = handler(event)

                    logger.debug(
                        f"Event {event_name} handled successfully by {handler_name}",
                        event_name=event_name,
                        handler=handler_name,
                    )

                    return result

                except Exception as e:
                    error = str(e)
                    logger.error(
                        f"Error in event handler {handler_name} for {event_name}: {error}",
                        exc_info=True,
                        event_name=event_name,
                        handler=handler_name,
                    )

                    # Create a handler exception, but don't raise it (just for reporting)
                    handler_exception = EventHandlerException(
                        message=f"Error in event handler {handler_name}: {error}",
                        event_name=event_name,
                        handler_name=handler_name,
                        original_exception=e,
                    )

                    # Handle errors but don't re-raise to avoid breaking event processing
                    if HAS_METRICS:
                        try:
                            error_metrics = get_dependency("metrics_service")
                            error_metrics.increment_counter(
                                "event_handler_errors_total",
                                1,
                                {"event_type": event_name, "handler": handler_name},
                            )
                        except Exception:
                            pass

                    # Try to report the error using the error service if available
                    try:
                        from app.core.dependency_manager import get_service
                        from app.core.error.base import ErrorContext

                        error_service = get_service("error_service")
                        context = ErrorContext(
                            function=f"event_handler:{handler_name}",
                            args=[],
                            kwargs={"event": event},
                            user_id=(
                                event.get("user_id")
                                if isinstance(event, dict)
                                else None
                            ),
                            request_id=(
                                event.get("request_id")
                                if isinstance(event, dict)
                                else None
                            ),
                        )
                        asyncio.create_task(error_service.report_error(e, context))
                    except Exception as report_err:
                        logger.debug(
                            f"Could not report event handler error: {str(report_err)}"
                        )

                    return None

                finally:
                    # Record metrics if available
                    if metrics_service and HAS_METRICS:
                        try:
                            duration = time.monotonic() - start_time
                            metrics_service.observe_histogram(
                                "event_handler_duration_seconds",
                                duration,
                                {"event_type": event_name, "handler": handler_name},
                            )
                        except Exception as metrics_err:
                            logger.warning(
                                f"Failed to record event handler metrics: {str(metrics_err)}"
                            )

            # Keep a reference to the original handler to maintain metadata
            wrapper.__name__ = handler.__name__
            wrapper.__doc__ = handler.__doc__

            # Return the original handler (the decorator in backend_subscribe_to_event
            # already registers the wrapper)
            return handler

        return decorator

    def _ensure_initialized(self) -> None:
        """Ensure that the event service is initialized."""
        if not self._initialized or not self._event_backend:
            logger.error("Event service accessed before initialization")
            raise EventServiceException(
                message="Event service not initialized",
                details={"initialized": self._initialized},
            )


# Global instance
_event_service: Optional[EventService] = None


def get_event_service() -> EventService:
    """
    Get or create the event service instance.

    Returns:
        EventService: The global event service instance
    """
    global _event_service
    if _event_service is None:
        _event_service = EventService()
    return _event_service


# Register with dependency manager if available
try:
    from app.core.dependency_manager import register_service

    register_service(get_event_service, "event_service")
except ImportError:
    logger.debug(
        "Dependency manager not available, skipping event service registration"
    )
