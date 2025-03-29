from __future__ import annotations
'\nAS400 synchronization startup module.\n\nThis module handles the initialization and shutdown of the AS400 sync service\nduring application startup and shutdown.\n'
from app.core.config.integrations.as400 import as400_settings
from app.logging import get_logger
from app.services.as400_sync_service import as400_sync_service, SyncEntityType
logger = get_logger('app.core.startup.as400_sync')
_initialized = False
async def initialize_as400_sync() -> None:
    global _initialized
    if _initialized:
        logger.debug('AS400 sync service already initialized')
        return
    logger.info('Initializing AS400 sync service')
    try:
        if not as400_settings.AS400_SYNC_ENABLED:
            logger.info('AS400 sync is disabled in configuration')
            return
        await as400_sync_service.initialize()
        for entity_type in SyncEntityType:
            await as400_sync_service.schedule_sync(entity_type, delay_seconds=30 + 15 * list(SyncEntityType).index(entity_type))
        _initialized = True
        logger.info('AS400 sync service initialized successfully')
    except Exception as e:
        logger.error(f'Failed to initialize AS400 sync service: {str(e)}')
async def shutdown_as400_sync() -> None:
    global _initialized
    if not _initialized:
        logger.debug('AS400 sync service not initialized, skipping shutdown')
        return
    logger.info('Shutting down AS400 sync service')
    try:
        await as400_sync_service.shutdown()
        _initialized = False
        logger.info('AS400 sync service shut down successfully')
    except Exception as e:
        logger.error(f'Error shutting down AS400 sync service: {str(e)}')