"""
Core module for service registry functionality.

This module provides a centralized registry for all application services,
enabling dependency injection and service discovery.
"""
from __future__ import annotations
import inspect
import logging
from typing import Any, Dict, Optional, Type, Union, cast

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConfigurationException, ErrorCode
from app.core.logging import get_logger

logger = get_logger('app.core.service_registry')

class ServiceRegistry:
    """Registry for all application services.

    This class implements the Singleton pattern and provides a centralized
    registry for services, enabling dependency injection and service discovery.
    """

    _instance = None
    _services: Dict[str, Any] = {}

    def __new__(cls, *args, **kwargs):
        """Create or return the singleton instance."""
        if cls._instance is None:
            cls._instance = super(ServiceRegistry, cls).__new__(cls)
            cls._instance._services = {}
            cls._instance._initialized = False
        return cls._instance

    @classmethod
    def register(cls, service_class: Type[Any], name: Optional[str]=None) -> None:
        """Register a service class.

        Args:
            service_class: The service class to register.
            name: Optional name for the service; defaults to class name.
        """
        if name is None:
            name = service_class.__name__

        logger.debug(f"Registering service: {name}")
        cls._services[name] = service_class

    @classmethod
    def get(cls, name: str, db: Optional[AsyncSession]=None) -> Any:
        """Get a service instance.

        Args:
            name: Name of the service.
            db: Optional database session to pass to the service.

        Returns:
            Service instance.

        Raises:
            ConfigurationException: If service not found.
        """
        if name not in cls._services:
            logger.error(f"Service not found: {name}")
            raise ConfigurationException(
                message=f"Service not found: {name}",
                code=ErrorCode.CONFIGURATION_ERROR
            )

        service_class = cls._services[name]

        # Check if the service is already instantiated as a singleton
        if isinstance(service_class, (staticmethod, classmethod)) or inspect.isfunction(service_class):
            return service_class(db) if db else service_class()

        # Check if a db session is required
        signature = inspect.signature(service_class.__init__)
        params = signature.parameters

        if 'db' in params and db is not None:
            return service_class(db)
        elif 'db' in params and db is None:
            logger.warning(f"Database session required for service: {name}")
            return None
        else:
            # Instantiate without db
            return service_class()

    @classmethod
    def get_all(cls, db: Optional[AsyncSession]=None) -> Dict[str, Any]:
        """Get all registered services.

        Args:
            db: Optional database session to pass to services.

        Returns:
            Dictionary of service name to instance.
        """
        return {name: cls.get(name, db) for name in cls._services}

# Singleton instance
service_registry = ServiceRegistry()

def register_services() -> None:
    """Register all services with the registry."""
    logger.info('Registering services')

    # Import services here to avoid circular imports
    from app.services.audit_service import AuditService
    from app.services.cache_service import CacheService
    from app.services.chat import ChatService
    from app.services.currency_service import ExchangeRateService
    from app.services.error_service import ErrorHandlingService
    from app.services.logging_service import LoggingService
    from app.services.media_service import MediaService
    from app.services.metrics_service import MetricsService
    from app.services.product_service import ProductService
    from app.services.search import SearchService
    from app.services.user_service import UserService
    from app.services.validation_service import ValidationService
    from app.services.vehicle import VehicleDataService

    dependency_manager.register_factory('logging_service', lambda: LoggingService())
    dependency_manager.register_factory('error_handling_service', lambda: ErrorHandlingService())
    dependency_manager.register_factory('validation_service', lambda: ValidationService())
    dependency_manager.register_factory('metrics_service', lambda: MetricsService())
    dependency_manager.register_factory('cache_service', lambda: CacheService())
    dependency_manager.register_factory('security_service', lambda: SecurityService())
    dependency_manager.register_factory('audit_service', lambda: AuditService())

    # Register DB-dependent services
    dependency_manager.register_factory('user_service', lambda db: UserService(db) if db else None)
    dependency_manager.register_factory('product_service', lambda db: ProductService(db) if db else None)
    dependency_manager.register_factory('chat_service', lambda db: ChatService(db) if db else None)
    dependency_manager.register_factory('search_service', lambda db: SearchService(db) if db else None)
    dependency_manager.register_factory('vehicle_service', lambda db: VehicleDataService(db) if db else None)
    dependency_manager.register_factory('media_service', lambda: MediaService())
    dependency_manager.register_factory('exchange_rate_service', lambda db: ExchangeRateService(db) if db else None)

    logger.info('Services registered successfully')

def get_service(service_name: str, db: Optional[AsyncSession]=None) -> Any:
    """Get a service by name.

    Args:
        service_name: Name of the service.
        db: Optional database session to pass to the service.

    Returns:
        Service instance.
    """
    from app.core.dependency_manager import get_dependency

    kwargs = {}
    if db:
        kwargs['db'] = db

    return get_dependency(service_name, **kwargs)

async def initialize_services() -> None:
    """Initialize all services in the correct order."""
    logger.info('Initializing services')

    # Order is important for initialization
    services_order = [
        'logging_service',
        'error_handling_service',
        'validation_service',
        'metrics_service',
        'cache_service',
        'security_service',
        'audit_service',
        'media_service',
        'user_service',
        'chat_service',
        'search_service',
        'product_service',
        'vehicle_service',
        'exchange_rate_service'
    ]

    from app.core.dependency_manager import get_dependency

    for service_name in services_order:
        try:
            service = get_dependency(service_name)
            if hasattr(service, 'initialize'):
                await service.initialize()
                logger.info(f'Initialized {service_name}')
        except Exception as e:
            logger.error(f'Error initializing {service_name}: {str(e)}', exc_info=e)

    logger.info('Services initialized successfully')

async def shutdown_services() -> None:
    """Shut down all services in reverse order."""
    logger.info('Shutting down services')

    # Reverse order from initialization
    services_order = [
        'exchange_rate_service',
        'vehicle_service',
        'product_service',
        'search_service',
        'chat_service',
        'user_service',
        'media_service',
        'audit_service',
        'security_service',
        'cache_service',
        'metrics_service',
        'validation_service',
        'error_handling_service',
        'logging_service'
    ]

    from app.core.dependency_manager import get_dependency

    for service_name in services_order:
        try:
            service = get_dependency(service_name)
            if hasattr(service, 'shutdown'):
                await service.shutdown()
                logger.info(f'Shut down {service_name}')
        except Exception as e:
            logger.error(f'Error shutting down {service_name}: {str(e)}', exc_info=e)

    logger.info('Services shut down successfully')
