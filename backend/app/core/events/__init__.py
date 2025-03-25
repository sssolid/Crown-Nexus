# app/core/events/__init__.py
from __future__ import annotations

"""Domain Events System.

Provides the public API for publishing and subscribing to domain events.
"""

from app.core.events.backend import (
    EventBackendType,
    get_event_backend,
    init_domain_events,
    init_event_backend,
    publish_event,
    subscribe_to_event,
    register_event_handlers,
)

__all__ = [
    "EventBackendType",
    "get_event_backend",
    "init_domain_events",
    "init_event_backend",
    "publish_event",
    "subscribe_to_event",
    "register_event_handlers",  # Kept for backward compatibility
]
