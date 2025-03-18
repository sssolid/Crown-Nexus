from __future__ import annotations

"""Dependency management system for application-wide service registration and resolution.

This module provides a unified dependency management. It allows for:
- Registration of service implementations
- Lazy initialization of services
- Dependency injection
- Service lifecycle management
- Support for both class-based and function-based service implementations

The system provides a centralized way to manage application dependencies and services,
making it easier to maintain and test the application.
"""

import inspect
import logging
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union, cast

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConfigurationException, ErrorCode
from app.core.logging import get_logger

logger = get_logger("app.core.dependency_manager")

T = TypeVar("T")


class DependencyManager:
    """Unified dependency management system for application services and components."""

    _instance = None
    _dependencies: Dict[str, Any] = {}
    _factories: Dict[str, Callable[..., Any]] = {}
    _services: Dict[str, Any] = {}
    _initialized = False

    def __new__(cls) -> DependencyManager:
        """Create a singleton instance of the dependency manager.

        Returns:
            The singleton instance
        """
        if cls._instance is None:
            cls._instance = super(DependencyManager, cls).__new__(cls)
            cls._instance._dependencies = {}
            cls._instance._factories = {}
            cls._instance._services = {}
            cls._instance._initialized = False
        return cls._instance

    def register_dependency(self, name: str, instance: Any) -> None:
        """Register a dependency instance with the manager.

        Args:
            name: The name of the dependency
            instance: The dependency instance
        """
        logger.debug(f"Registering dependency: {name}")
        self._dependencies[name] = instance

    def register_factory(self, name: str, factory: Callable[..., Any]) -> None:
        """Register a factory function for creating a dependency.

        Args:
            name: The name of the dependency
            factory: A callable that creates the dependency
        """
        logger.debug(f"Registering factory: {name}")
        self._factories[name] = factory

    def register_service(self, service_class: Type[Any], name: Optional[str] = None) -> None:
        """Register a service class with the manager.

        Args:
            service_class: The service class to register
            name: Optional name for the service (defaults to class name)
        """
        if name is None:
            name = service_class.__name__
        logger.debug(f"Registering service: {name}")
        self._services[name] = service_class

    def get(self, name: str, **kwargs: Any) -> Any:
        """Get a dependency instance by name.

        Args:
            name: The name of the dependency
            **kwargs: Additional arguments to pass to the factory if needed

        Returns:
            The dependency instance

        Raises:
            ConfigurationException: If the dependency is not registered
        """
        # Check for existing instance
        if name in self._dependencies:
            return self._dependencies[name]

        # Check for a factory
        if name in self._factories:
            instance = self._factories[name](**kwargs)
            if instance is not None:  # Don't cache None results
                self._dependencies[name] = instance
            return instance

        # Check for a service
        if name in self._services:
            return self._create_service_instance(name, **kwargs)

        logger.error(f"Dependency not registered: {name}")
        raise ConfigurationException(
            message=f"Dependency not registered: {name}",
            code=ErrorCode.CONFIGURATION_ERROR,
            details={"dependency_name": name, "available_dependencies": list(self._dependencies.keys())},
            status_code=500,
        )

    def _create_service_instance(self, name: str, **kwargs: Any) -> Any:
        """Create an instance of a registered service.

        Args:
            name: The name of the service
            **kwargs: Arguments to pass to the service constructor

        Returns:
            The service instance
        """
        service_class = self._services[name]

        # Handle function/method services
        if isinstance(service_class, (staticmethod, classmethod)) or inspect.isfunction(service_class):
            db = kwargs.get("db")
            return service_class(db) if db else service_class()

        # Handle class-based services
        signature = inspect.signature(service_class.__init__)
        params = signature.parameters

        # Check if service expects a db parameter
        if "db" in params and "db" in kwargs:
            return service_class(db=kwargs["db"])
        elif "db" in params and "db" not in kwargs:
            logger.warning(f"Database session required for service: {name}")
            return None
        else:
            return service_class()

    def get_instance(self, cls: Type[T], **kwargs: Any) -> T:
        """Get an instance of a specific class.

        Args:
            cls: The class to get an instance of
            **kwargs: Additional arguments to pass to the factory if needed

        Returns:
            An instance of the specified class
        """
        class_name = cls.__name__
        return cast(T, self.get(class_name, **kwargs))

    def get_all(self, db: Optional[AsyncSession] = None) -> Dict[str, Any]:
        """Get all registered services.

        Args:
            db: Optional database session to pass to services

        Returns:
            A dictionary of service names to service instances
        """
        kwargs = {}
        if db is not None:
            kwargs["db"] = db

        all_services = {}
        for name in self._services:
            try:
                service = self.get(name, **kwargs)
                if service is not None:
                    all_services[name] = service
            except Exception as e:
                logger.error(f"Error creating service {name}: {str(e)}")

        return all_services

    def clear(self) -> None:
        """Clear all registered dependencies."""
        self._dependencies.clear()
        logger.debug("Cleared all dependency instances")

    def clear_instance(self, name: str) -> None:
        """Clear a specific dependency instance.

        Args:
            name: The name of the dependency to clear
        """
        if name in self._dependencies:
            del self._dependencies[name]
            logger.debug(f"Cleared dependency instance: {name}")

    # Service registry specific functionality
    async def initialize_services(self) -> None:
        """Initialize all registered services.

        This calls the initialize method on each service that has one.
        """
        logger.info("Initializing services")
        service_names = list(self._services.keys())

        # Add core services that should be initialized first
        core_services = [
            "logging_service",
            "error_handling_service",
            "validation_service",
            "metrics_service",
            "cache_service",
            "security_service",
        ]

        # Process core services first, then others
        for service_name in core_services + [s for s in service_names if s not in core_services]:
            try:
                if service_name not in self._services:
                    continue

                service = self.get(service_name)
                if hasattr(service, "initialize") and callable(getattr(service, "initialize")):
                    await service.initialize()
                    logger.info(f"Initialized {service_name}")
            except Exception as e:
                logger.error(f"Error initializing {service_name}: {str(e)}", exc_info=True)

        self._initialized = True
        logger.info("Services initialized successfully")

    async def shutdown_services(self) -> None:
        """Shutdown all registered services.

        This calls the shutdown method on each service that has one.
        """
        logger.info("Shutting down services")
        # Shutdown in reverse order of initialization (approximately)
        service_names = list(self._dependencies.keys())

        # Process services in roughly reverse order of initialization
        for service_name in reversed(service_names):
            try:
                service = self._dependencies.get(service_name)
                if service and hasattr(service, "shutdown") and callable(getattr(service, "shutdown")):
                    await service.shutdown()
                    logger.info(f"Shut down {service_name}")
            except Exception as e:
                logger.error(f"Error shutting down {service_name}: {str(e)}", exc_info=True)

        logger.info("Services shut down successfully")


# Create a single instance of the dependency manager
dependency_manager = DependencyManager()


# Convenience functions
def get_dependency(name: str, **kwargs: Any) -> Any:
    """Get a dependency by name.

    Args:
        name: The name of the dependency
        **kwargs: Additional arguments to pass to the factory if needed

    Returns:
        The dependency instance
    """
    return dependency_manager.get(name, **kwargs)


def inject_dependency(dependency_name: str) -> Callable:
    """Create a decorator that injects a dependency into a function.

    Args:
        dependency_name: The name of the dependency to inject

    Returns:
        A decorator function
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            dependency = get_dependency(dependency_name)
            kwargs[dependency_name] = dependency
            return func(*args, **kwargs)

        return wrapper

    return decorator


def register_service(service_class: Type[Any], name: Optional[str] = None) -> Type[Any]:
    """Register a service class with the dependency manager.

    This can be used as a decorator or called directly.

    Args:
        service_class: The service class to register
        name: Optional name for the service (defaults to class name)

    Returns:
        The original service class
    """
    dependency_manager.register_service(service_class, name)
    return service_class


def register_services() -> None:
    """Register all application services with the dependency manager."""
    logger.info("Registering services")

    # Import services here to avoid circular imports
    # These would typically be your service imports
    try:
        from app.services.audit_service import AuditService
        from app.services.cache_service import CacheService
        from app.services.chat import ChatService
        from app.services.currency_service import ExchangeRateService
        from app.services.error_service import ErrorService
        from app.services.logging_service import LoggingService
        from app.services.media_service import MediaService
        from app.services.metrics_service import MetricsService
        from app.services.product_service import ProductService
        from app.services.search import SearchService
        from app.services.user_service import UserService
        from app.services.validation_service import ValidationService
        from app.services.vehicle import VehicleDataService
        from app.services.security_service import SecurityService

        # Register dependencies as factories
        dependency_manager.register_factory("logging_service", lambda: LoggingService())
        dependency_manager.register_factory("error_service", lambda: ErrorService())
        dependency_manager.register_factory("validation_service", lambda: ValidationService())
        dependency_manager.register_factory("metrics_service", lambda: MetricsService())
        dependency_manager.register_factory("cache_service", lambda: CacheService())
        dependency_manager.register_factory("security_service", lambda: SecurityService())
        dependency_manager.register_factory("audit_service", lambda: AuditService())
        dependency_manager.register_factory("user_service", lambda db: UserService(db) if db else None)
        dependency_manager.register_factory("product_service", lambda db: ProductService(db) if db else None)
        dependency_manager.register_factory("chat_service", lambda db: ChatService(db) if db else None)
        dependency_manager.register_factory("search_service", lambda db: SearchService(db) if db else None)
        dependency_manager.register_factory("vehicle_service", lambda db: VehicleDataService(db) if db else None)
        dependency_manager.register_factory("media_service", lambda: MediaService())
        dependency_manager.register_factory("exchange_rate_service", lambda db: ExchangeRateService(db) if db else None)

        # Register service classes
        dependency_manager.register_service(LoggingService, "LoggingService")
        dependency_manager.register_service(ErrorService, "ErrorService")
        dependency_manager.register_service(ValidationService, "ValidationService")
        dependency_manager.register_service(MetricsService, "MetricsService")
        dependency_manager.register_service(CacheService, "CacheService")
        dependency_manager.register_service(SecurityService, "SecurityService")
        dependency_manager.register_service(AuditService, "AuditService")
        dependency_manager.register_service(UserService, "UserService")
        dependency_manager.register_service(ProductService, "ProductService")
        dependency_manager.register_service(ChatService, "ChatService")
        dependency_manager.register_service(SearchService, "SearchService")
        dependency_manager.register_service(VehicleDataService, "VehicleDataService")
        dependency_manager.register_service(MediaService, "MediaService")
        dependency_manager.register_service(ExchangeRateService, "ExchangeRateService")

    except ImportError as e:
        logger.warning(f"Could not import all services: {str(e)}")

    logger.info("Services registered successfully")


async def initialize_services() -> None:
    """Initialize all registered services."""
    await dependency_manager.initialize_services()


async def shutdown_services() -> None:
    """Shutdown all registered services."""
    await dependency_manager.shutdown_services()


def get_service(service_name: str, db: Optional[AsyncSession] = None) -> Any:
    """Get a service by name.

    Args:
        service_name: The name of the service
        db: Optional database session to pass to the service

    Returns:
        The service instance
    """
    kwargs = {}
    if db:
        kwargs["db"] = db
    return get_dependency(service_name, **kwargs)
