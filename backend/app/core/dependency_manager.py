# /app/core/dependency_manager.py
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

from typing import Any, Callable, Dict, Optional, Type, TypeVar, cast

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConfigurationException
from app.core.logging import get_logger

logger = get_logger("app.core.dependency_manager")

T = TypeVar("T")


class DependencyManager:
    """Unified dependency management system for application services and components."""

    _instance = None
    _dependencies: Dict[str, Any] = {}
    _services: Dict[str, Callable[..., Any]] = {}
    _initialized = False

    def __new__(cls) -> DependencyManager:
        """Create a singleton instance of the dependency manager.

        Returns:
            The singleton instance
        """
        if cls._instance is None:
            cls._instance = super(DependencyManager, cls).__new__(cls)
            cls._instance._dependencies = {}
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

    def register_service(self, provider: Callable[..., Any], name: str) -> None:
        """Register a service provider function.

        Args:
            provider: A callable that creates the service
            name: The name of the service
        """
        logger.debug(f"Registering service: {name}")
        self._services[name] = provider

    def get(self, name: str, **kwargs: Any) -> Any:
        """Get a dependency instance by name.

        Args:
            name: The name of the dependency
            **kwargs: Additional arguments to pass to the service provider if needed

        Returns:
            The dependency instance

        Raises:
            ConfigurationException: If the dependency is not registered
        """
        # Check for existing instance
        if name in self._dependencies:
            return self._dependencies[name]

        # Check for a service provider
        if name in self._services:
            instance = self._services[name](**kwargs)
            if instance is not None:  # Don't cache None results
                self._dependencies[name] = instance
            return instance

        logger.error(f"Dependency not registered: {name}")
        available_dependencies = list(self._dependencies.keys()) + list(
            self._services.keys()
        )
        raise ConfigurationException(
            message=f"Dependency not registered: {name}",
            details={
                "dependency_name": name,
                "available_dependencies": available_dependencies,
            },
        )

    def get_instance(self, cls: Type[T], **kwargs: Any) -> T:
        """Get an instance of a specific class.

        Args:
            cls: The class to get an instance of
            **kwargs: Additional arguments to pass to the service provider if needed

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

        # Get all services that are already instantiated
        service_names = list(self._dependencies.keys())

        # Also check for services that are registered but not yet instantiated
        for service_name in list(self._services.keys()):
            if service_name not in service_names:
                # Try to instantiate the service
                try:
                    service = self.get(service_name)
                    if service is not None:
                        service_names.append(service_name)
                except Exception as e:
                    logger.error(
                        f"Error instantiating service {service_name}: {str(e)}"
                    )

        # Add core services that should be initialized first
        core_services = [
            "logging_service",
        ]

        # Process core services first, then others
        for service_name in core_services + [
            s for s in service_names if s not in core_services
        ]:
            try:
                service = self._dependencies.get(service_name)
                if (
                    service
                    and hasattr(service, "initialize")
                    and callable(getattr(service, "initialize"))
                ):
                    await service.initialize()
                    logger.info(f"Initialized {service_name}")
            except Exception as e:
                logger.error(
                    f"Error initializing {service_name}: {str(e)}", exc_info=True
                )

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
                if (
                    service
                    and hasattr(service, "shutdown")
                    and callable(getattr(service, "shutdown"))
                ):
                    await service.shutdown()
                    logger.info(f"Shut down {service_name}")
            except Exception as e:
                logger.error(
                    f"Error shutting down {service_name}: {str(e)}", exc_info=True
                )

        logger.info("Services shut down successfully")


# Create a single instance of the dependency manager
dependency_manager = DependencyManager()


# Convenience functions
def get_dependency(name: str, **kwargs: Any) -> Any:
    """Get a dependency by name.

    Args:
        name: The name of the dependency
        **kwargs: Additional arguments to pass to the service provider if needed

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


def register_service(
    provider: Callable[..., Any], name: Optional[str] = None
) -> Callable[..., Any]:
    """Register a service provider with the dependency manager.

    This can be used as a decorator or called directly.

    Args:
        provider: The service provider function
        name: Optional name for the service (defaults to function name)

    Returns:
        The original provider function
    """
    if name is None:
        name = provider.__name__
    dependency_manager.register_service(provider, name)
    return provider


def register_services() -> None:
    """Register all application services with the dependency manager."""
    logger.info("Registering services")

    # Import services here to avoid circular imports
    try:
        from app.domains.audit.service import get_audit_service
        from app.services.search import get_search_service
        from app.services.media import get_media_service
        from app.services.as400_sync_service import as400_sync_service

        # Register all services with the dependency manager using snake_case naming
        dependency_manager.register_service(
            lambda db=None: get_audit_service(db), "audit_service"
        )
        dependency_manager.register_service(
            lambda db=None: get_search_service(db), "search_service"
        )
        dependency_manager.register_service(
            lambda: get_media_service(), "media_service"
        )
        dependency_manager.register_service(
            lambda: as400_sync_service, "as400_sync_service"
        )

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
