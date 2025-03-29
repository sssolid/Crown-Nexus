from __future__ import annotations

"""
Domain Events System.

Provides the public API for publishing and subscribing to domain events.
This package supports event-driven architecture patterns throughout the application.
"""

from app.core.events.backend import (
    EventBackendType,
    get_event_backend,
    init_domain_events,
    init_event_backend,
    publish_event,
    subscribe_to_event,
)
from app.core.events.exceptions import (
    EventBackendException,
    EventConfigurationException,
    EventException,
    EventHandlerException,
    EventPublishException,
    EventServiceException,
)
from app.core.events.service import (
    EventService,
    get_event_service,
)

# Re-export all public API
__all__ = [
    # Backend
    "EventBackendType",
    "get_event_backend",
    "init_domain_events",
    "init_event_backend",
    "publish_event",
    "subscribe_to_event",
    # Service
    "EventService",
    "get_event_service",
    # Exceptions
    "EventException",
    "EventPublishException",
    "EventHandlerException",
    "EventConfigurationException",
    "EventBackendException",
    "EventServiceException",
]
