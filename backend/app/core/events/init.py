from __future__ import annotations

"""Event system initialization.

This module initializes the event system during application startup.
"""

import importlib
import logging
from typing import Any, List

from fastapi import FastAPI

from app.core.events.backend import EventBackendType, init_event_backend

logger = logging.getLogger(__name__)


def init_domain_events(
    app: FastAPI, backend_type: EventBackendType = EventBackendType.CELERY
) -> None:
    """Initialize the domain event system and register handlers.

    Args:
        app: The FastAPI application instance
        backend_type: Type of event backend to use
    """
    logger.info(f"Initializing domain event system with backend: {backend_type.name}")

    # Initialize event backend
    init_event_backend(backend_type)

    # Register startup event to import handlers
    @app.on_event("startup")
    async def register_event_handlers() -> None:
        import_domain_event_handlers()


def import_domain_event_handlers() -> None:
    """Import all domain event handlers to register them with the event system."""
    # List of domain handler modules to import
    handler_modules = [
        "app.domains.products.handlers",
        "app.domains.inventory.handlers",
        "app.domains.orders.handlers",
        # Add other domain handler modules as they're created
    ]

    for module_name in handler_modules:
        try:
            importlib.import_module(module_name)
            logger.info(f"Imported event handlers from {module_name}")
        except ImportError as e:
            logger.warning(f"Could not import event handlers from {module_name}: {e}")
