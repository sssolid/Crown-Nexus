from __future__ import annotations

"""
Base interfaces and classes for core services.

This module defines the common interfaces and base classes that all core services
should implement to ensure consistent behavior and lifecycle management.
"""

import abc
import contextlib
from datetime import datetime, timezone
from typing import (
    Any,
    AsyncContextManager,
    Callable,
    ClassVar,
    Dict,
    List,
    Optional,
    Protocol,
    Type,
    TypeVar,
    Union,
)

from pydantic import BaseModel

from app.logging import get_logger

logger = get_logger("app.core.base")

T = TypeVar("T")
T_Service = TypeVar("T_Service", bound="CoreService")
T_Manager = TypeVar("T_Manager", bound="CoreManager")
T_Backend = TypeVar("T_Backend", bound="CoreBackend")
T_Component = TypeVar("T_Component", bound="InitializableComponent")


class HealthStatus(BaseModel):
    """Health status information for a component."""

    status: str
    component: str
    timestamp: str
    details: Optional[Dict[str, Any]] = None
    sub_components: Optional[List["HealthStatus"]] = None


class ServiceConfig(BaseModel):
    """Base model for service configuration."""

    enabled: bool = True
    log_level: str = "INFO"

    @classmethod
    def from_settings(
        cls, settings_prefix: str, settings_obj: Any = None
    ) -> "ServiceConfig":
        """Create configuration from settings.

        Args:
            settings_prefix: Prefix for settings keys.
            settings_obj: Settings object, defaults to global settings.

        Returns:
            ServiceConfig instance.
        """
        from app.core.config import settings as global_settings

        settings_obj = settings_obj or global_settings
        config_dict = {}

        for field in cls.__annotations__:
            setting_key = f"{settings_prefix}_{field}".upper()
            if hasattr(settings_obj, setting_key):
                config_dict[field] = getattr(settings_obj, setting_key)

        return cls(**config_dict)


class InitializableComponent(Protocol):
    """Protocol defining components that can be initialized and shut down."""

    async def initialize(self) -> None:
        """Initialize the component."""
        ...

    async def shutdown(self) -> None:
        """Shut down the component."""
        ...


class HealthCheckable(Protocol):
    """Protocol for components that can report health status."""

    async def health_check(self) -> Dict[str, Any]:
        """Perform a health check.

        Returns:
            Dict containing health status information.
        """
        ...


class MetricsEnabled(Protocol):
    """Protocol for components that track metrics."""

    def increment_counter(
        self, name: str, value: int = 1, tags: Optional[Dict[str, str]] = None
    ) -> None:
        """Increment a counter metric."""
        ...

    def record_gauge(
        self, name: str, value: float, tags: Optional[Dict[str, str]] = None
    ) -> None:
        """Record a gauge metric."""
        ...

    def record_timing(
        self, name: str, value: float, tags: Optional[Dict[str, str]] = None
    ) -> None:
        """Record a timing metric."""
        ...


class CoreBackend(InitializableComponent, Protocol):
    """Base protocol for all core service backends."""

    __backend_name__: ClassVar[str]


class CoreManager(InitializableComponent, HealthCheckable):
    """Base class for all core service managers.

    Managers handle component coordination and lifecycle management.
    """

    def __init__(self) -> None:
        """Initialize the manager."""
        self.logger = get_logger(f"app.core.{self.component_name}.manager")
        self._initialized = False
        self._components: List[InitializableComponent] = []

    @property
    @abc.abstractmethod
    def component_name(self) -> str:
        """Get the component name.

        Returns:
            The component name.
        """
        pass

    def register_component(self, component: InitializableComponent) -> None:
        """Register a component with the manager.

        Components will be initialized and shut down along with the manager.

        Args:
            component: The component to register.
        """
        self._components.append(component)
        self.logger.debug(f"Registered component {component.__class__.__name__}")

    async def initialize(self) -> None:
        """Initialize the manager and all its components."""
        if self._initialized:
            self.logger.debug(f"{self.component_name} manager already initialized")
            return

        self.logger.info(f"Initializing {self.component_name} manager")

        # Initialize all components
        for component in self._components:
            try:
                await component.initialize()
            except Exception as e:
                self.logger.error(
                    f"Failed to initialize component {component.__class__.__name__}: {e}",
                    exc_info=True,
                )
                raise

        # Initialize manager-specific logic
        await self._initialize_manager()

        self._initialized = True
        self.logger.info(f"{self.component_name} manager initialized")

    async def _initialize_manager(self) -> None:
        """Initialize manager-specific logic.

        This method should be overridden by subclasses to implement
        manager-specific initialization logic.
        """
        pass

    async def shutdown(self) -> None:
        """Shut down the manager and all its components."""
        if not self._initialized:
            self.logger.debug(
                f"{self.component_name} manager not initialized, nothing to shut down"
            )
            return

        self.logger.info(f"Shutting down {self.component_name} manager")

        # Shut down manager-specific logic
        await self._shutdown_manager()

        # Shut down all components in reverse order
        for component in reversed(self._components):
            try:
                await component.shutdown()
            except Exception as e:
                self.logger.error(
                    f"Failed to shut down component {component.__class__.__name__}: {e}",
                    exc_info=True,
                )

        self._initialized = False
        self.logger.info(f"{self.component_name} manager shut down")

    async def _shutdown_manager(self) -> None:
        """Shut down manager-specific logic.

        This method should be overridden by subclasses to implement
        manager-specific shutdown logic.
        """
        pass

    async def health_check(self) -> Dict[str, Any]:
        """Perform a health check.

        Returns:
            Dict containing health status information.
        """
        status = "healthy"
        component_statuses = []

        for component in self._components:
            if hasattr(component, "health_check"):
                try:
                    component_status = await component.health_check()  # type: ignore
                    component_statuses.append(component_status)

                    if component_status.get("status") != "healthy":
                        status = "degraded"
                except Exception as e:
                    component_statuses.append(
                        {
                            "status": "unhealthy",
                            "component": component.__class__.__name__,
                            "error": str(e),
                        }
                    )
                    status = "degraded"

        return {
            "status": status,
            "component": self.component_name,
            "components": component_statuses,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


class CoreService(abc.ABC):
    """Base class for all core services in the application.

    All core services should inherit from this class to ensure consistent
    behavior and lifecycle management.
    """

    # Registry for tracking service instances
    _instances: ClassVar[Dict[Type[T_Service], T_Service]] = {}

    def __new__(cls, *args: Any, **kwargs: Any) -> T_Service:
        """Create a new service instance or return existing one.

        Args:
            *args: Positional arguments for the service constructor.
            **kwargs: Keyword arguments for the service constructor.

        Returns:
            The service instance.
        """
        # If we already have an instance of this class, return it
        if cls in cls._instances:
            return cls._instances[cls]

        # Otherwise create a new instance
        instance = super().__new__(cls)
        cls._instances[cls] = instance
        return instance

    def __init__(self) -> None:
        """Initialize the service."""
        self.logger = get_logger(f"app.core.{self.service_name}")
        self._initialized = False
        self._manager: Optional[CoreManager] = None

        # Don't re-initialize if already done
        if not hasattr(self, "_components"):
            self._components: List[InitializableComponent] = []
            self.logger.debug(f"Created {self.service_name} service")

    @property
    @abc.abstractmethod
    def service_name(self) -> str:
        """Get the service name.

        Returns:
            The service name.
        """
        pass

    @property
    def is_initialized(self) -> bool:
        """Check if the service is initialized.

        Returns:
            True if the service is initialized, False otherwise.
        """
        return self._initialized

    def register_component(self, component: InitializableComponent) -> None:
        """Register a component with the service.

        Components will be initialized and shut down along with the service.

        Args:
            component: The component to register.
        """
        self._components.append(component)
        self.logger.debug(f"Registered component {component.__class__.__name__}")

    async def initialize(self) -> None:
        """Initialize the service and all its components.

        This method should be called before using the service.
        """
        if self._initialized:
            self.logger.debug(f"{self.service_name} service already initialized")
            return

        self.logger.info(f"Initializing {self.service_name} service")

        # Initialize all components
        for component in self._components:
            try:
                await component.initialize()
            except Exception as e:
                self.logger.error(
                    f"Failed to initialize component {component.__class__.__name__}: {e}",
                    exc_info=True,
                )
                raise

        # Initialize service-specific logic
        await self._initialize_service()

        self._initialized = True
        self.logger.info(f"{self.service_name} service initialized")

    async def _initialize_service(self) -> None:
        """Initialize service-specific logic.

        This method should be overridden by subclasses to implement
        service-specific initialization logic.
        """
        pass

    async def shutdown(self) -> None:
        """Shut down the service and all its components.

        This method should be called when the service is no longer needed.
        """
        if not self._initialized:
            self.logger.debug(
                f"{self.service_name} service not initialized, nothing to shut down"
            )
            return

        self.logger.info(f"Shutting down {self.service_name} service")

        # Shut down service-specific logic
        await self._shutdown_service()

        # Shut down all components in reverse order
        for component in reversed(self._components):
            try:
                await component.shutdown()
            except Exception as e:
                self.logger.error(
                    f"Failed to shut down component {component.__class__.__name__}: {e}",
                    exc_info=True,
                )

        self._initialized = False
        self.logger.info(f"{self.service_name} service shut down")

    async def _shutdown_service(self) -> None:
        """Shut down service-specific logic.

        This method should be overridden by subclasses to implement
        service-specific shutdown logic.
        """
        pass

    async def __aenter__(self) -> "CoreService":
        """Enter the context manager.

        Returns:
            The service instance.
        """
        if not self._initialized:
            await self.initialize()
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Exit the context manager."""
        await self.shutdown()

    def context(self) -> "AsyncContextManager[CoreService]":
        """Get a context manager for the service.

        Returns:
            Context manager that initializes and shuts down the service.
        """
        return contextlib.AsyncExitStack()  # type: ignore

    @classmethod
    def get_instance(cls: Type[T_Service]) -> T_Service:
        """Get the service instance.

        Returns:
            The service instance.

        Raises:
            RuntimeError: If the service instance doesn't exist.
        """
        if cls not in cls._instances:
            raise RuntimeError(f"No instance of {cls.__name__} exists")
        return cls._instances[cls]

    async def health_check(self) -> Dict[str, Any]:
        """Perform a health check.

        Returns:
            Dict containing health status information.
        """
        status = "healthy"
        component_statuses = []

        for component in self._components:
            if hasattr(component, "health_check"):
                try:
                    component_status = await component.health_check()  # type: ignore
                    component_statuses.append(component_status)

                    if component_status.get("status") != "healthy":
                        status = "degraded"
                except Exception as e:
                    component_statuses.append(
                        {
                            "status": "unhealthy",
                            "component": component.__class__.__name__,
                            "error": str(e),
                        }
                    )
                    status = "degraded"

        return {
            "status": status,
            "service": self.service_name,
            "components": component_statuses,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


class ServiceRegistry:
    """Registry for all core services."""

    _services: Dict[str, CoreService] = {}

    @classmethod
    def register(cls, service_name: str, service: CoreService) -> None:
        """Register a service.

        Args:
            service_name: Name of the service.
            service: Service instance.
        """
        cls._services[service_name] = service

    @classmethod
    def get(cls, service_name: str) -> Optional[CoreService]:
        """Get a service by name.

        Args:
            service_name: Name of the service.

        Returns:
            Service instance or None if not found.
        """
        return cls._services.get(service_name)

    @classmethod
    def get_all(cls) -> Dict[str, CoreService]:
        """Get all registered services.

        Returns:
            Dictionary of service names to service instances.
        """
        return cls._services.copy()

    @classmethod
    async def initialize_all(cls) -> None:
        """Initialize all registered services."""
        for service_name, service in cls._services.items():
            await service.initialize()

    @classmethod
    async def shutdown_all(cls) -> None:
        """Shut down all registered services."""
        # Shutdown in reverse registration order
        for service_name, service in reversed(list(cls._services.items())):
            await service.shutdown()


def discover_backends(package_path: str) -> Dict[str, Type[Any]]:
    """Discover backend implementations in a package.

    Args:
        package_path: Import path to the package to scan.

    Returns:
        Dict mapping backend names to backend classes.
    """
    import importlib
    import inspect
    import pkgutil

    backends = {}
    package = importlib.import_module(package_path)

    # Get all modules in the package
    for _, name, is_pkg in pkgutil.iter_modules(
        package.__path__, package.__name__ + "."
    ):
        if not is_pkg:
            module = importlib.import_module(name)
            # Find all classes in the module
            for cls_name, cls in inspect.getmembers(module, inspect.isclass):
                # Check if the class is a backend implementation
                if cls.__module__ == name and hasattr(cls, "__backend_name__"):
                    backends[cls.__backend_name__] = cls

    return backends
