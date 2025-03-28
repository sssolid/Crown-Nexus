from __future__ import annotations

"""
AS400 synchronization startup module.

This module handles the initialization and shutdown of the AS400 sync service
during application startup and shutdown.
"""

from app.core.config.integrations.as400 import as400_settings
from app.logging import get_logger
from app.services.as400_sync_service import as400_sync_service, SyncEntityType

logger = get_logger("app.core.startup.as400_sync")

# Track initialization status
_initialized = False


async def initialize_as400_sync() -> None:
    """
    Initialize the AS400 sync service.

    This function should be called during application startup.
    """
    global _initialized

    if _initialized:
        logger.debug("AS400 sync service already initialized")
        return

    logger.info("Initializing AS400 sync service")

    try:
        # Check if sync is enabled
        if not as400_settings.AS400_SYNC_ENABLED:
            logger.info("AS400 sync is disabled in configuration")
            return

        # Initialize the service
        await as400_sync_service.initialize()

        # Schedule initial syncs
        for entity_type in SyncEntityType:
            await as400_sync_service.schedule_sync(
                entity_type,
                delay_seconds=30 + (15 * list(SyncEntityType).index(entity_type)),
            )

        _initialized = True
        logger.info("AS400 sync service initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize AS400 sync service: {str(e)}")
        # Don't raise - allow application to start even if sync initialization fails


async def shutdown_as400_sync() -> None:
    """
    Shut down the AS400 sync service.

    This function should be called during application shutdown.
    """
    global _initialized

    if not _initialized:
        logger.debug("AS400 sync service not initialized, skipping shutdown")
        return

    logger.info("Shutting down AS400 sync service")

    try:
        await as400_sync_service.shutdown()
        _initialized = False
        logger.info("AS400 sync service shut down successfully")
    except Exception as e:
        logger.error(f"Error shutting down AS400 sync service: {str(e)}")
