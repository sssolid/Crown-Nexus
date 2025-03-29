from __future__ import annotations
'\nEvent service implementation.\n\nThis module provides a service wrapper around the event system,\nmaking it available through the dependency manager and integrating\nwith other application systems like metrics, error handling, and logging.\n'
import asyncio
import inspect
import time
from typing import Any, Callable, Dict, List, Optional, TypeVar, cast
from app.core.events.backend import EventBackend, EventBackendType, EventHandler, get_event_backend, init_event_backend, init_domain_events, publish_event as backend_publish_event, subscribe_to_event as backend_subscribe_to_event
from app.core.events.exceptions import EventConfigurationException, EventPublishException, EventServiceException, EventHandlerException
from app.logging import get_logger
logger = get_logger('app.core.events.service')
T = TypeVar('T')
Event = Dict[str, Any]
try:
    from app.core.dependency_manager import get_dependency
    HAS_METRICS = True
except ImportError:
    HAS_METRICS = False
class EventService:
    def __init__(self) -> None:
        self._initialized = False
        self._event_backend: Optional[EventBackend] = None
        self._default_context: Dict[str, Any] = {}
    async def initialize(self, backend_type: EventBackendType=EventBackendType.MEMORY) -> None:
        if self._initialized:
            logger.debug('Event service already initialized, skipping')
            return
        logger.info(f'Initializing event service with {backend_type.name} backend')
        try:
            init_event_backend(backend_type)
            self._event_backend = get_event_backend()
            init_domain_events()
            if HAS_METRICS:
                try:
                    metrics_service = get_dependency('metrics_service')
                    metrics_service.create_counter('events_published_total', 'Total number of domain events published', ['event_type', 'backend'])
                    metrics_service.create_counter('event_handler_errors_total', 'Total number of errors in event handlers', ['event_type', 'handler'])
                    metrics_service.create_histogram('event_handler_duration_seconds', 'Time spent processing events in handlers', ['event_type', 'handler'])
                    logger.info('Event system metrics registered')
                except Exception as e:
                    logger.debug(f'Could not register event metrics: {str(e)}')
            self._initialized = True
            logger.info('Event service initialized successfully')
        except Exception as e:
            logger.error(f'Error initializing event service: {str(e)}', exc_info=True)
            raise EventServiceException(message=f'Failed to initialize event service: {str(e)}', details={'backend_type': backend_type.name}, original_exception=e) from e
    async def shutdown(self) -> None:
        if not self._initialized:
            return
        logger.info('Shutting down event service')
        self._initialized = False
        self._event_backend = None
        logger.info('Event service shut down')
    def set_default_context(self, context: Dict[str, Any]) -> None:
        self._default_context = context
    async def publish(self, event_name: str, payload: Dict[str, Any], context: Optional[Dict[str, Any]]=None) -> None:
        self._ensure_initialized()
        metrics_service = None
        start_time = time.monotonic()
        backend_type = 'unknown'
        try:
            if HAS_METRICS:
                try:
                    metrics_service = get_dependency('metrics_service')
                except Exception as e:
                    logger.debug(f'Could not get metrics service: {str(e)}')
            if self._event_backend:
                backend_type = self._event_backend.__class__.__name__
            full_payload = {**self._default_context}
            if context:
                full_payload.update(context)
            full_payload['data'] = payload
            if 'timestamp' not in full_payload:
                full_payload['timestamp'] = time.time()
            logger.info(f'Publishing event: {event_name}', event_name=event_name, payload_size=len(str(payload)), backend=backend_type)
            backend_publish_event(event_name, full_payload)
            logger.debug(f'Event published: {event_name}', event_name=event_name)
        except Exception as e:
            logger.error(f'Error publishing event {event_name}: {str(e)}', exc_info=True, event_name=event_name)
            raise EventPublishException(message=f'Failed to publish event {event_name}: {str(e)}', event_name=event_name, details={'payload_size': len(str(payload))}, original_exception=e) from e
        finally:
            if metrics_service and HAS_METRICS:
                try:
                    duration = time.monotonic() - start_time
                    metrics_service.increment_counter('events_published_total', 1, {'event_type': event_name, 'backend': backend_type})
                    metrics_service.observe_histogram('event_publish_duration_seconds', duration, {'event_type': event_name, 'backend': backend_type})
                except Exception as metrics_err:
                    logger.warning(f'Failed to record event metrics: {str(metrics_err)}')
    def subscribe(self, event_name: str) -> Callable[[EventHandler], EventHandler]:
        return backend_subscribe_to_event(event_name)
    def event_handler(self, event_name: str, filter_func: Optional[Callable[[Dict[str, Any]], bool]]=None) -> Callable[[EventHandler], EventHandler]:
        def decorator(handler: EventHandler) -> EventHandler:
            @backend_subscribe_to_event(event_name)
            async def wrapper(event: Dict[str, Any]) -> Any:
                metrics_service = None
                start_time = time.monotonic()
                handler_name = handler.__name__
                error = None
                try:
                    if HAS_METRICS:
                        try:
                            metrics_service = get_dependency('metrics_service')
                        except Exception as e:
                            logger.debug(f'Could not get metrics service: {str(e)}')
                    if filter_func and (not filter_func(event)):
                        logger.debug(f'Event filtered out for handler {handler_name}', event_name=event_name, handler=handler_name)
                        return None
                    logger.debug(f'Handling event {event_name} with {handler_name}', event_name=event_name, handler=handler_name)
                    if inspect.iscoroutinefunction(handler):
                        result = await handler(event)
                    else:
                        result = handler(event)
                    logger.debug(f'Event {event_name} handled successfully by {handler_name}', event_name=event_name, handler=handler_name)
                    return result
                except Exception as e:
                    error = str(e)
                    logger.error(f'Error in event handler {handler_name} for {event_name}: {error}', exc_info=True, event_name=event_name, handler=handler_name)
                    handler_exception = EventHandlerException(message=f'Error in event handler {handler_name}: {error}', event_name=event_name, handler_name=handler_name, original_exception=e)
                    if HAS_METRICS:
                        try:
                            error_metrics = get_dependency('metrics_service')
                            error_metrics.increment_counter('event_handler_errors_total', 1, {'event_type': event_name, 'handler': handler_name})
                        except Exception:
                            pass
                    try:
                        from app.core.dependency_manager import get_service
                        from app.core.error.base import ErrorContext
                        error_service = get_service('error_service')
                        context = ErrorContext(function=f'event_handler:{handler_name}', args=[], kwargs={'event': event}, user_id=event.get('user_id') if isinstance(event, dict) else None, request_id=event.get('request_id') if isinstance(event, dict) else None)
                        asyncio.create_task(error_service.report_error(e, context))
                    except Exception as report_err:
                        logger.debug(f'Could not report event handler error: {str(report_err)}')
                    return None
                finally:
                    if metrics_service and HAS_METRICS:
                        try:
                            duration = time.monotonic() - start_time
                            metrics_service.observe_histogram('event_handler_duration_seconds', duration, {'event_type': event_name, 'handler': handler_name})
                        except Exception as metrics_err:
                            logger.warning(f'Failed to record event handler metrics: {str(metrics_err)}')
            wrapper.__name__ = handler.__name__
            wrapper.__doc__ = handler.__doc__
            return handler
        return decorator
    def _ensure_initialized(self) -> None:
        if not self._initialized or not self._event_backend:
            logger.error('Event service accessed before initialization')
            raise EventServiceException(message='Event service not initialized', details={'initialized': self._initialized})
_event_service: Optional[EventService] = None
def get_event_service() -> EventService:
    global _event_service
    if _event_service is None:
        _event_service = EventService()
    return _event_service
try:
    from app.core.dependency_manager import register_service
    register_service(get_event_service, 'event_service')
except ImportError:
    logger.debug('Dependency manager not available, skipping event service registration')