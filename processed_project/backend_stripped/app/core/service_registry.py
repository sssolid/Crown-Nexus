from __future__ import annotations
import inspect
from typing import Any, Dict, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependency_manager import dependency_manager
from app.core.logging import get_logger
from app.services.error_handling_service import ErrorHandlingService
from app.services.logging_service import LoggingService
from app.services.metrics_service import MetricsService
from app.services.validation_service import ValidationService
from app.services.cache_service import CacheService
logger = get_logger('app.core.service_registry')
def register_services() -> None:
    logger.info('Registering services')
    dependency_manager.register_factory('logging_service', lambda: LoggingService())
    dependency_manager.register_factory('error_handling_service', lambda: ErrorHandlingService())
    dependency_manager.register_factory('validation_service', lambda: ValidationService())
    dependency_manager.register_factory('metrics_service', lambda: MetricsService())
    dependency_manager.register_factory('cache_service', lambda: CacheService())
    logger.info('Services registered successfully')
def get_service(service_name: str, db: Optional[AsyncSession]=None) -> Any:
    kwargs = {}
    if db:
        kwargs['db'] = db
    return dependency_manager.get(service_name, **kwargs)
async def initialize_services() -> None:
    logger.info('Initializing services')
    logging_service = dependency_manager.get('logging_service')
    await logging_service.initialize()
    error_handling_service = dependency_manager.get('error_handling_service')
    await error_handling_service.initialize()
    validation_service = dependency_manager.get('validation_service')
    await validation_service.initialize()
    metrics_service = dependency_manager.get('metrics_service')
    await metrics_service.initialize()
    cache_service = dependency_manager.get('cache_service')
    await cache_service.initialize()
    logger.info('Services initialized successfully')
async def shutdown_services() -> None:
    logger.info('Shutting down services')
    logging_service = dependency_manager.get('logging_service')
    await logging_service.shutdown()
    error_handling_service = dependency_manager.get('error_handling_service')
    await error_handling_service.shutdown()
    validation_service = dependency_manager.get('validation_service')
    await validation_service.shutdown()
    metrics_service = dependency_manager.get('metrics_service')
    await metrics_service.shutdown()
    cache_service = dependency_manager.get('cache_service')
    await cache_service.shutdown()
    logger.info('Services shut down successfully')