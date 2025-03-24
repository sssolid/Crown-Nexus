from __future__ import annotations

"""Domain Events System.

Provides the public API for publishing and subscribing to domain events.
"""

from app.core.events.backend import (
    EventBackendType,
    publish_event,
    subscribe_to_event,
    register_event_handlers,
)

__all__ = [
    "publish_event",
    "subscribe_to_event",
    "register_event_handlers",
    "EventBackendType",
]
