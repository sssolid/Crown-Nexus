from __future__ import annotations
'\nBase interfaces and classes for core services.\n\nThis module defines the common interfaces and base classes that all core services\nshould implement to ensure consistent behavior and lifecycle management.\n'
import abc
import contextlib
from datetime import datetime, timezone
from typing import Any, AsyncContextManager, Callable, ClassVar, Dict, List, Optional, Protocol, Type, TypeVar, Union
from pydantic import BaseModel
from app.logging import get_logger
logger = get_logger('app.core.base')
T = TypeVar('T')
T_Service = TypeVar('T_Service', bound='CoreService')
T_Manager = TypeVar('T_Manager', bound='CoreManager')
T_Backend = TypeVar('T_Backend', bound='CoreBackend')
T_Component = TypeVar('T_Component', bound='InitializableComponent')
class HealthStatus(BaseModel):
    status: str
    component: str
    timestamp: str
    details: Optional[Dict[str, Any]] = None
    sub_components: Optional[List['HealthStatus']] = None
class ServiceConfig(BaseModel):
    enabled: bool = True
    log_level: str = 'INFO'
    @classmethod
    def from_settings(cls, settings_prefix: str, settings_obj: Any=None) -> 'ServiceConfig':
        from app.core.config import settings as global_settings
        settings_obj = settings_obj or global_settings
        config_dict = {}
        for field in cls.__annotations__:
            setting_key = f'{settings_prefix}_{field}'.upper()
            if hasattr(settings_obj, setting_key):
                config_dict[field] = getattr(settings_obj, setting_key)
        return cls(**config_dict)
class InitializableComponent(Protocol):
    async def initialize(self) -> None:
        ...
    async def shutdown(self) -> None:
        ...
class HealthCheckable(Protocol):
    async def health_check(self) -> Dict[str, Any]:
        ...
class MetricsEnabled(Protocol):
    def increment_counter(self, name: str, value: int=1, tags: Optional[Dict[str, str]]=None) -> None:
        ...
    def record_gauge(self, name: str, value: float, tags: Optional[Dict[str, str]]=None) -> None:
        ...
    def record_timing(self, name: str, value: float, tags: Optional[Dict[str, str]]=None) -> None:
        ...
class CoreBackend(InitializableComponent, Protocol):
    __backend_name__: ClassVar[str]
class CoreManager(InitializableComponent, HealthCheckable):
    def __init__(self) -> None:
        self.logger = get_logger(f'app.core.{self.component_name}.manager')
        self._initialized = False
        self._components: List[InitializableComponent] = []
    @property
    @abc.abstractmethod
    def component_name(self) -> str:
        pass
    def register_component(self, component: InitializableComponent) -> None:
        self._components.append(component)
        self.logger.debug(f'Registered component {component.__class__.__name__}')
    async def initialize(self) -> None:
        if self._initialized:
            self.logger.debug(f'{self.component_name} manager already initialized')
            return
        self.logger.info(f'Initializing {self.component_name} manager')
        for component in self._components:
            try:
                await component.initialize()
            except Exception as e:
                self.logger.error(f'Failed to initialize component {component.__class__.__name__}: {e}', exc_info=True)
                raise
        await self._initialize_manager()
        self._initialized = True
        self.logger.info(f'{self.component_name} manager initialized')
    async def _initialize_manager(self) -> None:
        pass
    async def shutdown(self) -> None:
        if not self._initialized:
            self.logger.debug(f'{self.component_name} manager not initialized, nothing to shut down')
            return
        self.logger.info(f'Shutting down {self.component_name} manager')
        await self._shutdown_manager()
        for component in reversed(self._components):
            try:
                await component.shutdown()
            except Exception as e:
                self.logger.error(f'Failed to shut down component {component.__class__.__name__}: {e}', exc_info=True)
        self._initialized = False
        self.logger.info(f'{self.component_name} manager shut down')
    async def _shutdown_manager(self) -> None:
        pass
    async def health_check(self) -> Dict[str, Any]:
        status = 'healthy'
        component_statuses = []
        for component in self._components:
            if hasattr(component, 'health_check'):
                try:
                    component_status = await component.health_check()
                    component_statuses.append(component_status)
                    if component_status.get('status') != 'healthy':
                        status = 'degraded'
                except Exception as e:
                    component_statuses.append({'status': 'unhealthy', 'component': component.__class__.__name__, 'error': str(e)})
                    status = 'degraded'
        return {'status': status, 'component': self.component_name, 'components': component_statuses, 'timestamp': datetime.now(timezone.utc).isoformat()}
class CoreService(abc.ABC):
    _instances: ClassVar[Dict[Type[T_Service], T_Service]] = {}
    def __new__(cls, *args: Any, **kwargs: Any) -> T_Service:
        if cls in cls._instances:
            return cls._instances[cls]
        instance = super().__new__(cls)
        cls._instances[cls] = instance
        return instance
    def __init__(self) -> None:
        self.logger = get_logger(f'app.core.{self.service_name}')
        self._initialized = False
        self._manager: Optional[CoreManager] = None
        if not hasattr(self, '_components'):
            self._components: List[InitializableComponent] = []
            self.logger.debug(f'Created {self.service_name} service')
    @property
    @abc.abstractmethod
    def service_name(self) -> str:
        pass
    @property
    def is_initialized(self) -> bool:
        return self._initialized
    def register_component(self, component: InitializableComponent) -> None:
        self._components.append(component)
        self.logger.debug(f'Registered component {component.__class__.__name__}')
    async def initialize(self) -> None:
        if self._initialized:
            self.logger.debug(f'{self.service_name} service already initialized')
            return
        self.logger.info(f'Initializing {self.service_name} service')
        for component in self._components:
            try:
                await component.initialize()
            except Exception as e:
                self.logger.error(f'Failed to initialize component {component.__class__.__name__}: {e}', exc_info=True)
                raise
        await self._initialize_service()
        self._initialized = True
        self.logger.info(f'{self.service_name} service initialized')
    async def _initialize_service(self) -> None:
        pass
    async def shutdown(self) -> None:
        if not self._initialized:
            self.logger.debug(f'{self.service_name} service not initialized, nothing to shut down')
            return
        self.logger.info(f'Shutting down {self.service_name} service')
        await self._shutdown_service()
        for component in reversed(self._components):
            try:
                await component.shutdown()
            except Exception as e:
                self.logger.error(f'Failed to shut down component {component.__class__.__name__}: {e}', exc_info=True)
        self._initialized = False
        self.logger.info(f'{self.service_name} service shut down')
    async def _shutdown_service(self) -> None:
        pass
    async def __aenter__(self) -> 'CoreService':
        if not self._initialized:
            await self.initialize()
        return self
    async def __aexit__(self, *args: Any) -> None:
        await self.shutdown()
    def context(self) -> 'AsyncContextManager[CoreService]':
        return contextlib.AsyncExitStack()
    @classmethod
    def get_instance(cls: Type[T_Service]) -> T_Service:
        if cls not in cls._instances:
            raise RuntimeError(f'No instance of {cls.__name__} exists')
        return cls._instances[cls]
    async def health_check(self) -> Dict[str, Any]:
        status = 'healthy'
        component_statuses = []
        for component in self._components:
            if hasattr(component, 'health_check'):
                try:
                    component_status = await component.health_check()
                    component_statuses.append(component_status)
                    if component_status.get('status') != 'healthy':
                        status = 'degraded'
                except Exception as e:
                    component_statuses.append({'status': 'unhealthy', 'component': component.__class__.__name__, 'error': str(e)})
                    status = 'degraded'
        return {'status': status, 'service': self.service_name, 'components': component_statuses, 'timestamp': datetime.now(timezone.utc).isoformat()}
class ServiceRegistry:
    _services: Dict[str, CoreService] = {}
    @classmethod
    def register(cls, service_name: str, service: CoreService) -> None:
        cls._services[service_name] = service
    @classmethod
    def get(cls, service_name: str) -> Optional[CoreService]:
        return cls._services.get(service_name)
    @classmethod
    def get_all(cls) -> Dict[str, CoreService]:
        return cls._services.copy()
    @classmethod
    async def initialize_all(cls) -> None:
        for service_name, service in cls._services.items():
            await service.initialize()
    @classmethod
    async def shutdown_all(cls) -> None:
        for service_name, service in reversed(list(cls._services.items())):
            await service.shutdown()
def discover_backends(package_path: str) -> Dict[str, Type[Any]]:
    import importlib
    import inspect
    import pkgutil
    backends = {}
    package = importlib.import_module(package_path)
    for _, name, is_pkg in pkgutil.iter_modules(package.__path__, package.__name__ + '.'):
        if not is_pkg:
            module = importlib.import_module(name)
            for cls_name, cls in inspect.getmembers(module, inspect.isclass):
                if cls.__module__ == name and hasattr(cls, '__backend_name__'):
                    backends[cls.__backend_name__] = cls
    return backends