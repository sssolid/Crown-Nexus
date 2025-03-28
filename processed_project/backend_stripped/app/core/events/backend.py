from __future__ import annotations
'Domain Events Backend Implementations.\n\nThis module implements the core event system functionality with different backend options.\n'
import asyncio
import inspect
from app.logging import get_logger
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Protocol
logger = get_logger('app.core.events.backend')
EventHandler = Callable[[Dict[str, Any]], Any]
class EventBackendType(Enum):
    CELERY = auto()
    MEMORY = auto()
class EventPublisher(Protocol):
    def publish_event(self, event_name: str, payload: Dict[str, Any]) -> None:
        ...
class EventSubscriber(Protocol):
    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        ...
class EventBackend(ABC, EventPublisher, EventSubscriber):
    @abstractmethod
    def publish_event(self, event_name: str, payload: Dict[str, Any]) -> None:
        pass
    @abstractmethod
    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        pass
class CeleryEventBackend(EventBackend):
    def __init__(self, celery_app: Any) -> None:
        self.celery_app = celery_app
        self.logger = get_logger('app.core.events.backend')
    def publish_event(self, event_name: str, payload: Dict[str, Any]) -> None:
        task_name = f'domain_events.{event_name}'
        self.logger.info(f'Publishing domain event {event_name} with Celery')
        self.celery_app.send_task(task_name, kwargs={'payload': payload})
    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        task_name = f'domain_events.{event_name}'
        if task_name in self.celery_app.tasks:
            self.logger.debug(f'Handler for {event_name} already registered')
            return
        @self.celery_app.task(name=task_name)
        def task_handler(payload: Dict[str, Any]) -> Any:
            self.logger.info(f'Handling domain event {event_name} with Celery')
            if inspect.iscoroutinefunction(handler):
                return asyncio.run(handler(payload))
            return handler(payload)
        self.logger.info(f'Registered handler for {event_name} with Celery')
class MemoryEventBackend(EventBackend):
    def __init__(self) -> None:
        self.handlers: Dict[str, List[EventHandler]] = {}
        self.logger = get_logger('app.core.events.backend')
    def publish_event(self, event_name: str, payload: Dict[str, Any]) -> None:
        self.logger.info(f'Publishing domain event {event_name} in-memory')
        if event_name not in self.handlers:
            self.logger.debug(f'No handlers for event {event_name}')
            return
        for handler in self.handlers[event_name]:
            try:
                if inspect.iscoroutinefunction(handler):
                    asyncio.create_task(handler(payload))
                else:
                    handler(payload)
            except Exception as e:
                self.logger.error(f'Error in event handler for {event_name}: {e}')
    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        self.logger.info(f'Subscribing handler to {event_name} in-memory')
        if event_name not in self.handlers:
            self.handlers[event_name] = []
        self.handlers[event_name].append(handler)
_event_backend: Optional[EventBackend] = None
_pending_handlers: Dict[str, List[EventHandler]] = {}
_is_initialized = False
def get_event_backend() -> EventBackend:
    if _event_backend is None:
        raise RuntimeError('Event backend not initialized. Call init_event_backend first.')
    return _event_backend
def init_event_backend(backend_type: EventBackendType, **kwargs: Any) -> EventBackend:
    global _event_backend, _is_initialized
    if _is_initialized:
        logger.warning('Event backend already initialized')
        return _event_backend
    logger.info(f'Initializing event backend: {backend_type.name}')
    if backend_type == EventBackendType.CELERY:
        from app.core.celery_app import celery_app
        _event_backend = CeleryEventBackend(celery_app)
    elif backend_type == EventBackendType.MEMORY:
        _event_backend = MemoryEventBackend()
    else:
        raise ValueError(f'Unsupported event backend type: {backend_type}')
    _is_initialized = True
    logger.info(f'Event backend initialized: {backend_type.name}')
    return _event_backend
def publish_event(event_name: str, payload: Dict[str, Any]) -> None:
    backend = get_event_backend()
    backend.publish_event(event_name, payload)
def subscribe_to_event(event_name: str) -> Callable[[EventHandler], EventHandler]:
    def decorator(handler: EventHandler) -> EventHandler:
        global _pending_handlers, _is_initialized, _event_backend
        if event_name not in _pending_handlers:
            _pending_handlers[event_name] = []
        _pending_handlers[event_name].append(handler)
        logger.debug(f'Queued handler {handler.__name__} for event {event_name}')
        if _is_initialized and _event_backend is not None:
            try:
                _event_backend.subscribe(event_name, handler)
                logger.debug(f'Registered handler {handler.__name__} for event {event_name}')
            except Exception as e:
                logger.error(f'Error registering handler: {str(e)}')
        return handler
    return decorator
def init_domain_events() -> None:
    global _event_backend, _is_initialized, _pending_handlers
    if not _is_initialized or _event_backend is None:
        raise RuntimeError('Event backend not initialized. Call init_event_backend first.')
    logger.info('Registering domain event handlers')
    for event_name, handlers in _pending_handlers.items():
        for handler in handlers:
            try:
                logger.debug(f'Registering handler {handler.__name__} for event {event_name}')
                _event_backend.subscribe(event_name, handler)
            except Exception as e:
                logger.error(f'Error registering handler: {str(e)}')
    _import_event_handlers()
    logger.info(f'Registered {sum((len(handlers) for handlers in _pending_handlers.values()))} event handlers')
def register_event_handlers(*modules: Any) -> None:
    logger.warning('register_event_handlers is deprecated. Use init_domain_events instead.')
def _import_event_handlers() -> None:
    logger.debug('Importing domain event handler modules')
    try:
        import importlib
        modules_to_import = ['app.domains.products.handlers', 'app.domains.orders.handlers', 'app.domains.inventory.handlers']
        for module_name in modules_to_import:
            try:
                importlib.import_module(module_name)
                logger.debug(f'Imported event handlers from {module_name}')
            except ImportError:
                logger.debug(f'Could not import event handlers from {module_name} (module may not exist)')
    except Exception as e:
        logger.warning(f'Error importing event handler modules: {str(e)}')