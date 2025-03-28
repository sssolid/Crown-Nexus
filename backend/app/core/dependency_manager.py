from __future__ import annotations

"""Dependency management system for application-wide service registration and resolution.

This module provides a unified dependency management system. It allows for:
- Registration of service implementations
- Lazy initialization of services
- Dependency injection
- Service lifecycle management
- Support for both class-based and function-based service implementations

The system provides a centralized way to manage application dependencies and services,
making it easier to maintain and test the application.
"""

import asyncio
import functools
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Type,
    TypeVar,
    cast,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConfigurationException
from app.logging import get_logger

logger = get_logger("app.core.dependency_manager")

T = TypeVar("T")


class DependencyManager:
    """Singleton manager for application dependencies and services."""

    _instance = None
    _dependencies: Dict[str, Any] = {}
    _services: Dict[str, Callable[..., Any]] = {}
    _initialized: Set[str] = set()
    _initializing: Set[str] = set()
    _dependency_graph: Dict[str, List[str]] = {}

    def __new__(cls) -> DependencyManager:
        """Create a new singleton instance if one doesn't exist."""
        if cls._instance is None:
            cls._instance = super(DependencyManager, cls).__new__(cls)
            cls._instance._dependencies = {}
            cls._instance._services = {}
            cls._instance._initialized = set()
            cls._instance._initializing = set()
            cls._instance._dependency_graph = {}
        return cls._instance

    def register_dependency(self, name: str, instance: Any) -> None:
        """Register an existing instance as a dependency.

        Args:
            name: Name of the dependency
            instance: The dependency instance
        """
        logger.debug(f"Registering dependency: {name}")
        self._dependencies[name] = instance

    def register_service(self, provider: Callable[..., Any], name: str) -> None:
        """Register a service provider function.

        Args:
            provider: Function that creates the service
            name: Name of the service
        """
        logger.debug(f"Registering service: {name}")
        self._services[name] = provider

    def register_dependency_relationship(
        self, service_name: str, depends_on: List[str]
    ) -> None:
        """Register dependencies between services for ordered initialization.

        Args:
            service_name: Name of the dependent service
            depends_on: Names of services this one depends on
        """
        self._dependency_graph[service_name] = depends_on

    def get(self, name: str, **kwargs: Any) -> Any:
        """Get or create a dependency by name.

        Args:
            name: Name of the dependency
            **kwargs: Additional arguments to pass to the service provider

        Returns:
            The dependency instance

        Raises:
            ConfigurationException: If the dependency is not registered
        """
        # Return existing instance if available
        if name in self._dependencies:
            return self._dependencies[name]

        # Create instance if service provider exists
        if name in self._services:
            try:
                instance = self._services[name](**kwargs)
                if instance is not None:
                    self._dependencies[name] = instance
                return instance
            except Exception as e:
                logger.error(
                    f"Error creating dependency {name}: {str(e)}", exc_info=True
                )
                raise ConfigurationException(
                    message=f"Failed to create dependency: {name}",
                    details={
                        "dependency_name": name,
                        "error": str(e),
                    },
                    original_exception=e,
                )

        # Error if dependency not found
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
        """Get an instance by its class type.

        Args:
            cls: The class type to get an instance of
            **kwargs: Additional arguments to pass to the service provider

        Returns:
            An instance of the specified class
        """
        class_name = cls.__name__
        return cast(T, self.get(class_name, **kwargs))

    def get_all(self, db: Optional[AsyncSession] = None) -> Dict[str, Any]:
        """Get all available services.

        Args:
            db: Optional database session to pass to service providers

        Returns:
            Dictionary of service name to service instance
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
        """Clear all dependency instances."""
        self._dependencies.clear()
        self._initialized.clear()
        self._initializing.clear()
        logger.debug("Cleared all dependency instances")

    def clear_instance(self, name: str) -> None:
        """Clear a specific dependency instance.

        Args:
            name: Name of the dependency to clear
        """
        if name in self._dependencies:
            del self._dependencies[name]
            if name in self._initialized:
                self._initialized.remove(name)
            logger.debug(f"Cleared dependency instance: {name}")

    async def _initialize_service(self, service_name: str) -> None:
        """Initialize a single service, resolving dependencies as needed.

        Args:
            service_name: Name of the service to initialize

        Raises:
            ConfigurationException: If circular dependencies are detected
        """
        # Skip if already initialized
        if service_name in self._initialized:
            return

        # Detect circular dependencies
        if service_name in self._initializing:
            deps_chain = " -> ".join(self._initializing) + f" -> {service_name}"
            raise ConfigurationException(
                message=f"Circular dependency detected: {deps_chain}",
                details={"dependency_chain": deps_chain},
            )

        # Mark as initializing
        self._initializing.add(service_name)

        try:
            # Initialize dependencies first
            if service_name in self._dependency_graph:
                for dep_name in self._dependency_graph[service_name]:
                    await self._initialize_service(dep_name)

            # Get or create service instance
            service = None
            if service_name in self._dependencies:
                service = self._dependencies[service_name]
            elif service_name in self._services:
                try:
                    service = self.get(service_name)
                except Exception as e:
                    logger.error(
                        f"Error instantiating service {service_name}: {str(e)}",
                        exc_info=True,
                    )
                    return

            # Initialize if has initialize method
            if (
                service
                and hasattr(service, "initialize")
                and callable(getattr(service, "initialize"))
            ):
                try:
                    await service.initialize()
                    logger.info(f"Initialized {service_name}")
                except Exception as e:
                    logger.error(
                        f"Error initializing {service_name}: {str(e)}", exc_info=True
                    )
                    return

            # Mark as initialized
            self._initialized.add(service_name)

        finally:
            # Always remove from initializing set
            self._initializing.remove(service_name)

    async def initialize_services(self) -> None:
        """Initialize all registered services in dependency order."""
        logger.info("Initializing services")

        # Create initial service list
        service_names = list(self._dependencies.keys())

        # Try to get instances for services that don't have instances yet
        for service_name in list(self._services.keys()):
            if service_name not in service_names:
                try:
                    # Try to instantiate service
                    service = self.get(service_name)
                    if service is not None:
                        service_names.append(service_name)
                except Exception as e:
                    logger.error(
                        f"Error instantiating service {service_name}: {str(e)}"
                    )

        # Core services to initialize first
        core_services = ["logging_service", "error_service", "cache_service"]

        # Initialize core services first, then others
        priority_services = [s for s in core_services if s in service_names]
        other_services = [s for s in service_names if s not in core_services]

        # Initialize priority services first
        for service_name in priority_services:
            await self._initialize_service(service_name)

        # Initialize other services
        for service_name in other_services:
            await self._initialize_service(service_name)

        logger.info("Services initialized successfully")

    async def shutdown_services(self) -> None:
        """Shut down all services in reverse initialization order."""
        logger.info("Shutting down services")

        # Get services in reverse initialization order
        service_names = list(self._initialized)
        service_names.reverse()  # Shutdown in reverse order of initialization

        for service_name in service_names:
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

        # Clear initialization state
        self._initialized.clear()
        logger.info("Services shut down successfully")


# Create a singleton instance
dependency_manager = DependencyManager()


def get_dependency(name: str, **kwargs: Any) -> Any:
    """Get a dependency by name.

    Args:
        name: Name of the dependency
        **kwargs: Additional arguments to pass to the service provider

    Returns:
        The dependency instance
    """
    return dependency_manager.get(name, **kwargs)


def inject_dependency(dependency_name: str) -> Callable:
    """Decorator for injecting dependencies into functions.

    Args:
        dependency_name: Name of the dependency to inject

    Returns:
        Decorator function
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            dependency = get_dependency(dependency_name)
            kwargs[dependency_name] = dependency
            return func(*args, **kwargs)

        return wrapper

    return decorator


def register_service(
    provider: Callable[..., Any], name: Optional[str] = None
) -> Callable[..., Any]:
    """Decorator to register a service provider.

    Args:
        provider: Function that creates the service
        name: Optional name for the service (defaults to function name)

    Returns:
        The original provider function
    """
    service_name = name or provider.__name__
    dependency_manager.register_service(provider, service_name)
    return provider


def register_async_service(
    async_provider: Callable[..., Awaitable[T]], name: Optional[str] = None
) -> Callable[..., Awaitable[T]]:
    """Register an async service provider.

    Args:
        async_provider: Async function that creates the service
        name: Optional name for the service (defaults to function name)

    Returns:
        The original async provider function
    """
    service_name = name or async_provider.__name__

    # Create a sync wrapper that doesn't use run_until_complete
    def sync_provider(**kwargs: Any) -> T:
        # Create non-initialized instance now
        # Actual initialization happens when the service is used
        try:
            # For media service, just create without initializing
            if service_name == "media_service":
                from app.domains.media.service.service import MediaService

                return MediaService(storage_type=kwargs.get("storage_type"))

            # For other services, create a task that will be awaited later
            loop = asyncio.get_running_loop()
            task = loop.create_task(async_provider(**kwargs))
            future = asyncio.run_coroutine_threadsafe(async_provider(**kwargs), loop)
            return future.result(timeout=0.1)  # Small timeout for quick creation
        except RuntimeError:
            # If no event loop is running, create a new one
            # This is for cases outside of FastAPI request handling
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(async_provider(**kwargs))
            finally:
                loop.close()

    dependency_manager.register_service(sync_provider, service_name)
    return async_provider


def register_services() -> None:
    """Register all application services with the dependency manager."""
    logger.info("Registering services")

    try:
        # Import and register core services
        try:
            from app.core.error.service import get_error_service

            dependency_manager.register_service(get_error_service, "error_service")
        except ImportError:
            logger.warning("Error service not available")

        # Import and register domain services
        try:
            from app.domains.audit.service import get_audit_service

            dependency_manager.register_service(
                lambda db=None: get_audit_service(db), "audit_service"
            )
            dependency_manager.register_dependency_relationship(
                "audit_service", ["error_service"]
            )
        except ImportError:
            logger.warning("Audit service not available")

        try:
            from app.services.search import get_search_service

            dependency_manager.register_service(
                lambda db=None: get_search_service(db), "search_service"
            )
        except ImportError:
            logger.warning("Search service not available")

        try:
            from app.domains.media.service import get_media_service_factory

            register_async_service(get_media_service_factory, "media_service")
        except ImportError:
            logger.warning("Media service not available")

        try:
            from app.services.as400_sync_service import as400_sync_service

            dependency_manager.register_service(
                lambda: as400_sync_service, "as400_sync_service"
            )
        except ImportError:
            logger.warning("AS400 sync service not available")

    except Exception as e:
        logger.error(f"Error registering services: {str(e)}", exc_info=True)

    logger.info("Services registered successfully")


async def initialize_services() -> None:
    """Initialize all registered services."""
    await dependency_manager.initialize_services()


async def shutdown_services() -> None:
    """Shut down all services."""
    await dependency_manager.shutdown_services()


def get_service(service_name: str, db: Optional[AsyncSession] = None) -> Any:
    """Get a service by name.

    Args:
        service_name: Name of the service to retrieve
        db: Optional database session to pass to the service provider

    Returns:
        The service instance with the following type mappings:
        - "error_service" -> ErrorService
        - "user_service" -> UserService
        - "audit_service" -> AuditService
        - "search_service" -> SearchService
        - "media_service" -> MediaService

    Examples:
        ```python
        # Get error service (returns ErrorService)
        error_service = get_service("error_service")

        # Get user service with DB session (returns UserService)
        user_service = get_service("user_service", db=session)
        ```
    """
    kwargs = {}
    if db:
        kwargs["db"] = db
    return get_dependency(service_name, **kwargs)


def with_dependencies(**dependencies: str) -> Callable:
    """Decorator for injecting multiple dependencies into a function.

    Args:
        **dependencies: Mapping of parameter names to dependency names

    Returns:
        Decorator function
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for param_name, dependency_name in dependencies.items():
                if param_name not in kwargs:
                    kwargs[param_name] = get_dependency(dependency_name)
            return func(*args, **kwargs)

        return wrapper

    return decorator
