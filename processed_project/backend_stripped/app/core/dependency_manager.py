from __future__ import annotations
'Dependency management system for application-wide service registration and resolution.\n\nThis module provides a unified dependency management. It allows for:\n- Registration of service implementations\n- Lazy initialization of services\n- Dependency injection\n- Service lifecycle management\n- Support for both class-based and function-based service implementations\n\nThe system provides a centralized way to manage application dependencies and services,\nmaking it easier to maintain and test the application.\n'
import inspect
from typing import Any, Callable, Dict, Optional, Type, TypeVar, cast
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ConfigurationException
from app.core.logging import get_logger
logger = get_logger('app.core.dependency_manager')
T = TypeVar('T')
class DependencyManager:
    _instance = None
    _dependencies: Dict[str, Any] = {}
    _services: Dict[str, Callable[..., Any]] = {}
    _initialized = False
    def __new__(cls) -> DependencyManager:
        if cls._instance is None:
            cls._instance = super(DependencyManager, cls).__new__(cls)
            cls._instance._dependencies = {}
            cls._instance._services = {}
            cls._instance._initialized = False
        return cls._instance
    def register_dependency(self, name: str, instance: Any) -> None:
        logger.debug(f'Registering dependency: {name}')
        self._dependencies[name] = instance
    def register_service(self, provider: Callable[..., Any], name: str) -> None:
        logger.debug(f'Registering service: {name}')
        self._services[name] = provider
    def get(self, name: str, **kwargs: Any) -> Any:
        if name in self._dependencies:
            return self._dependencies[name]
        if name in self._services:
            instance = self._services[name](**kwargs)
            if instance is not None:
                self._dependencies[name] = instance
            return instance
        logger.error(f'Dependency not registered: {name}')
        available_dependencies = list(self._dependencies.keys()) + list(self._services.keys())
        raise ConfigurationException(message=f'Dependency not registered: {name}', details={'dependency_name': name, 'available_dependencies': available_dependencies})
    def get_instance(self, cls: Type[T], **kwargs: Any) -> T:
        class_name = cls.__name__
        return cast(T, self.get(class_name, **kwargs))
    def get_all(self, db: Optional[AsyncSession]=None) -> Dict[str, Any]:
        kwargs = {}
        if db is not None:
            kwargs['db'] = db
        all_services = {}
        for name in self._services:
            try:
                service = self.get(name, **kwargs)
                if service is not None:
                    all_services[name] = service
            except Exception as e:
                logger.error(f'Error creating service {name}: {str(e)}')
        return all_services
    def clear(self) -> None:
        self._dependencies.clear()
        logger.debug('Cleared all dependency instances')
    def clear_instance(self, name: str) -> None:
        if name in self._dependencies:
            del self._dependencies[name]
            logger.debug(f'Cleared dependency instance: {name}')
    async def initialize_services(self) -> None:
        logger.info('Initializing services')
        service_names = list(self._dependencies.keys())
        for service_name in list(self._services.keys()):
            if service_name not in service_names:
                try:
                    service = self.get(service_name)
                    if service is not None:
                        service_names.append(service_name)
                except Exception as e:
                    logger.error(f'Error instantiating service {service_name}: {str(e)}')
        core_services = ['logging_service']
        for service_name in core_services + [s for s in service_names if s not in core_services]:
            try:
                service = self._dependencies.get(service_name)
                if service and hasattr(service, 'initialize') and callable(getattr(service, 'initialize')):
                    await service.initialize()
                    logger.info(f'Initialized {service_name}')
            except Exception as e:
                logger.error(f'Error initializing {service_name}: {str(e)}', exc_info=True)
        self._initialized = True
        logger.info('Services initialized successfully')
    async def shutdown_services(self) -> None:
        logger.info('Shutting down services')
        service_names = list(self._dependencies.keys())
        for service_name in reversed(service_names):
            try:
                service = self._dependencies.get(service_name)
                if service and hasattr(service, 'shutdown') and callable(getattr(service, 'shutdown')):
                    await service.shutdown()
                    logger.info(f'Shut down {service_name}')
            except Exception as e:
                logger.error(f'Error shutting down {service_name}: {str(e)}', exc_info=True)
        logger.info('Services shut down successfully')
dependency_manager = DependencyManager()
def get_dependency(name: str, **kwargs: Any) -> Any:
    return dependency_manager.get(name, **kwargs)
def inject_dependency(dependency_name: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            dependency = get_dependency(dependency_name)
            kwargs[dependency_name] = dependency
            return func(*args, **kwargs)
        return wrapper
    return decorator
def register_service(provider: Callable[..., Any], name: Optional[str]=None) -> Callable[..., Any]:
    if name is None:
        name = provider.__name__
    dependency_manager.register_service(provider, name)
    return provider
def register_services() -> None:
    logger.info('Registering services')
    try:
        from app.services.audit import get_audit_service
        from app.services.search import get_search_service
        from app.services.media import get_media_service
        from app.services.as400_sync_service import as400_sync_service
        dependency_manager.register_service(lambda db=None: get_audit_service(db), 'audit_service')
        dependency_manager.register_service(lambda db=None: get_search_service(db), 'search_service')
        dependency_manager.register_service(lambda: get_media_service(), 'media_service')
        dependency_manager.register_service(lambda: as400_sync_service, 'as400_sync_service')
    except ImportError as e:
        logger.warning(f'Could not import all services: {str(e)}')
    logger.info('Services registered successfully')
async def initialize_services() -> None:
    await dependency_manager.initialize_services()
async def shutdown_services() -> None:
    await dependency_manager.shutdown_services()
def get_service(service_name: str, db: Optional[AsyncSession]=None) -> Any:
    kwargs = {}
    if db:
        kwargs['db'] = db
    return get_dependency(service_name, **kwargs)