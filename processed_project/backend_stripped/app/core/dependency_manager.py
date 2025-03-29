from __future__ import annotations
'Dependency management system for application-wide service registration and resolution.\n\nThis module provides a unified dependency management system. It allows for:\n- Registration of service implementations\n- Lazy initialization of services\n- Dependency injection\n- Service lifecycle management\n- Support for both class-based and function-based service implementations\n\nThe system provides a centralized way to manage application dependencies and services,\nmaking it easier to maintain and test the application.\n'
import asyncio
import functools
from typing import Any, Awaitable, Callable, Dict, List, Optional, Set, Type, TypeVar, cast
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ConfigurationException
from app.logging import get_logger
logger = get_logger('app.core.dependency_manager')
T = TypeVar('T')
class DependencyManager:
    _instance = None
    _dependencies: Dict[str, Any] = {}
    _services: Dict[str, Callable[..., Any]] = {}
    _initialized: Set[str] = set()
    _initializing: Set[str] = set()
    _dependency_graph: Dict[str, List[str]] = {}
    def __new__(cls) -> DependencyManager:
        if cls._instance is None:
            cls._instance = super(DependencyManager, cls).__new__(cls)
            cls._instance._dependencies = {}
            cls._instance._services = {}
            cls._instance._initialized = set()
            cls._instance._initializing = set()
            cls._instance._dependency_graph = {}
        return cls._instance
    def register_dependency(self, name: str, instance: Any) -> None:
        logger.debug(f'Registering dependency: {name}')
        self._dependencies[name] = instance
    def register_service(self, provider: Callable[..., Any], name: str) -> None:
        logger.debug(f'Registering service: {name}')
        self._services[name] = provider
    def register_dependency_relationship(self, service_name: str, depends_on: List[str]) -> None:
        self._dependency_graph[service_name] = depends_on
    def get(self, name: str, **kwargs: Any) -> Any:
        if name in self._dependencies:
            return self._dependencies[name]
        if name in self._services:
            try:
                instance = self._services[name](**kwargs)
                if instance is not None:
                    self._dependencies[name] = instance
                return instance
            except Exception as e:
                logger.error(f'Error creating dependency {name}: {str(e)}', exc_info=True)
                raise ConfigurationException(message=f'Failed to create dependency: {name}', details={'dependency_name': name, 'error': str(e)}, original_exception=e)
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
        self._initialized.clear()
        self._initializing.clear()
        logger.debug('Cleared all dependency instances')
    def clear_instance(self, name: str) -> None:
        if name in self._dependencies:
            del self._dependencies[name]
            if name in self._initialized:
                self._initialized.remove(name)
            logger.debug(f'Cleared dependency instance: {name}')
    async def _initialize_service(self, service_name: str) -> None:
        if service_name in self._initialized:
            return
        if service_name in self._initializing:
            deps_chain = ' -> '.join(self._initializing) + f' -> {service_name}'
            raise ConfigurationException(message=f'Circular dependency detected: {deps_chain}', details={'dependency_chain': deps_chain})
        self._initializing.add(service_name)
        try:
            if service_name in self._dependency_graph:
                for dep_name in self._dependency_graph[service_name]:
                    await self._initialize_service(dep_name)
            service = None
            if service_name in self._dependencies:
                service = self._dependencies[service_name]
            elif service_name in self._services:
                try:
                    service = self.get(service_name)
                except Exception as e:
                    logger.error(f'Error instantiating service {service_name}: {str(e)}', exc_info=True)
                    return
            if service and hasattr(service, 'initialize') and callable(getattr(service, 'initialize')):
                try:
                    await service.initialize()
                    logger.info(f'Initialized {service_name}')
                except Exception as e:
                    logger.error(f'Error initializing {service_name}: {str(e)}', exc_info=True)
                    return
            self._initialized.add(service_name)
        finally:
            self._initializing.remove(service_name)
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
        core_services = ['logging_service', 'error_service', 'cache_service']
        priority_services = [s for s in core_services if s in service_names]
        other_services = [s for s in service_names if s not in core_services]
        for service_name in priority_services:
            await self._initialize_service(service_name)
        for service_name in other_services:
            await self._initialize_service(service_name)
        logger.info('Services initialized successfully')
    async def shutdown_services(self) -> None:
        logger.info('Shutting down services')
        service_names = list(self._initialized)
        service_names.reverse()
        for service_name in service_names:
            try:
                service = self._dependencies.get(service_name)
                if service and hasattr(service, 'shutdown') and callable(getattr(service, 'shutdown')):
                    await service.shutdown()
                    logger.info(f'Shut down {service_name}')
            except Exception as e:
                logger.error(f'Error shutting down {service_name}: {str(e)}', exc_info=True)
        self._initialized.clear()
        logger.info('Services shut down successfully')
dependency_manager = DependencyManager()
def get_dependency(name: str, **kwargs: Any) -> Any:
    return dependency_manager.get(name, **kwargs)
def inject_dependency(dependency_name: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            dependency = get_dependency(dependency_name)
            kwargs[dependency_name] = dependency
            return func(*args, **kwargs)
        return wrapper
    return decorator
def register_service(provider: Callable[..., Any], name: Optional[str]=None) -> Callable[..., Any]:
    service_name = name or provider.__name__
    dependency_manager.register_service(provider, service_name)
    return provider
def register_async_service(async_provider: Callable[..., Awaitable[T]], name: Optional[str]=None) -> Callable[..., Awaitable[T]]:
    service_name = name or async_provider.__name__
    def sync_provider(**kwargs: Any) -> T:
        try:
            if service_name == 'media_service':
                from app.domains.media.service.service import MediaService
                return MediaService(storage_type=kwargs.get('storage_type'))
            loop = asyncio.get_running_loop()
            task = loop.create_task(async_provider(**kwargs))
            future = asyncio.run_coroutine_threadsafe(async_provider(**kwargs), loop)
            return future.result(timeout=0.1)
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(async_provider(**kwargs))
            finally:
                loop.close()
    dependency_manager.register_service(sync_provider, service_name)
    return async_provider
def register_services() -> None:
    logger.info('Registering services')
    try:
        try:
            from app.core.error.service import get_error_service
            dependency_manager.register_service(get_error_service, 'error_service')
        except ImportError:
            logger.warning('Error service not available')
        try:
            from app.core.validation.service import get_validation_service
            dependency_manager.register_service(get_validation_service, 'error_service')
        except ImportError:
            logger.warning('Validation service not available')
        try:
            from app.core.metrics.service import get_metrics_service
            dependency_manager.register_service(get_metrics_service, 'metrics_service')
        except ImportError:
            logger.warning('Metrics service not available')
        try:
            from app.core.pagination.service import get_pagination_service
            dependency_manager.register_service(lambda db=None: get_pagination_service(db), 'pagination_service')
        except ImportError:
            logger.warning('Pagination service not available')
        try:
            from app.core.rate_limiting.service import get_rate_limiting_service
            dependency_manager.register_service(lambda db=None: get_rate_limiting_service, 'rate_limiting_service')
        except ImportError:
            logger.warning('Rate Limiting service not available')
        try:
            from app.core.cache.service import get_cache_service
            dependency_manager.register_service(lambda db=None: get_cache_service, 'cache_service')
        except ImportError:
            logger.warning('Cache service not available')
        try:
            from app.domains.audit.service import get_audit_service
            dependency_manager.register_service(lambda db=None: get_audit_service(db), 'audit_service')
            dependency_manager.register_dependency_relationship('audit_service', ['error_service'])
        except ImportError:
            logger.warning('Audit service not available')
        try:
            from app.services.search import get_search_service
            dependency_manager.register_service(lambda db=None: get_search_service(db), 'search_service')
        except ImportError:
            logger.warning('Search service not available')
        try:
            from app.domains.media.service import get_media_service_factory
            register_async_service(get_media_service_factory, 'media_service')
        except ImportError:
            logger.warning('Media service not available')
        try:
            from app.services.as400_sync_service import as400_sync_service
            dependency_manager.register_service(lambda: as400_sync_service, 'as400_sync_service')
        except ImportError:
            logger.warning('AS400 sync service not available')
    except Exception as e:
        logger.error(f'Error registering services: {str(e)}', exc_info=True)
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
def with_dependencies(**dependencies: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for param_name, dependency_name in dependencies.items():
                if param_name not in kwargs:
                    kwargs[param_name] = get_dependency(dependency_name)
            return func(*args, **kwargs)
        return wrapper
    return decorator