from __future__ import annotations
'\nMain application module.\n\nThis module initializes and configures the FastAPI application, including\nmiddleware, exception handlers, and application components.\n'
import os
import multiprocessing
multiprocessing.set_start_method('spawn', force=True)
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncGenerator, Optional, List
import uvicorn
from fastapi import FastAPI, Depends, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from app.logging import reinitialize_logging, shutdown_logging, get_logger, set_user_id
import app.db.base
from app.api.deps import get_current_user
from app.core.cache.manager import initialize_cache
from app.core.config import Environment, settings
from app.core.dependency_manager import register_services, initialize_services, shutdown_services, get_service
from app.core.audit import get_audit_service
from app.core.error import initialize as initialize_error_system, shutdown as shutdown_error_system
from app.core.events import EventBackendType, init_event_backend, init_domain_events, EventConfigurationException
from app.core.exceptions import AppException, app_exception_handler, validation_exception_handler, generic_exception_handler
from app.core.metrics import initialize as initialize_metrics_system, shutdown as shutdown_metrics_system
from app.core.pagination import initialize as initialize_pagination_system, shutdown as shutdown_pagination_system
from app.core.rate_limiting import initialize as initialize_ratelimiting_system, shutdown as shutdown_ratelimiting_system, RateLimitRule, RateLimitStrategy
from app.core.startup.as400_sync import initialize_as400_sync, shutdown_as400_sync
from app.core.validation import initialize as initialize_validation_system, shutdown as shutdown_validation_system
from app.domains.users.models import User
from app.middleware.request_context import RequestContextMiddleware
from app.middleware.tracing import TracingMiddleware
from app.middleware.metrics import MetricsMiddleware
from app.middleware.timeout import TimeoutMiddleware
from app.middleware.compression import CompressionMiddleware
from app.middleware.security import SecurityHeadersMiddleware, SecureRequestMiddleware
from app.middleware.rate_limiting import RateLimitMiddleware
from app.middleware.cache_control import CacheControlMiddleware
from app.middleware.response_formatter import ResponseFormatterMiddleware
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.middleware.cors import EnhancedCORSMiddleware
from app.api.v1.router import api_router
logger = get_logger('app.main')
def add_typed_middleware(app: FastAPI, middleware_class: Any, **options: Any) -> None:
    app.add_middleware(middleware_class, **options)
def initialize_event_system() -> bool:
    for backend in [EventBackendType.CELERY, EventBackendType.MEMORY]:
        try:
            logger.info(f'Attempting to initialize event system with backend: {backend}')
            init_event_backend(backend)
            init_domain_events()
            logger.info(f'Successfully initialized event system with backend: {backend}')
            return True
        except EventConfigurationException as e:
            logger.warning(f'Event configuration failed for backend {backend}: {e}')
        except Exception as e:
            logger.exception(f'Unexpected error initializing event system with backend {backend}')
    logger.critical('Failed to initialize any event system backend.')
    return False
initialized_components: List[str] = []
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    global initialized_components
    initialized_components = []
    await reinitialize_logging()
    initialized_components.append('logging')
    logger.info('Starting application initialization')
    try:
        await initialize_error_system()
        initialized_components.append('error_system')
        logger.info('Error system initialized')
    except Exception as e:
        logger.critical(f'Failed to initialize error system: {str(e)}', exc_info=True)
        raise
    register_services()
    initialized_components.append('services_registered')
    logger.info('Services registered')
    await initialize_validation_system()
    initialized_components.append('validation_system')
    logger.info('Validation system initialized')
    await initialize_metrics_system()
    initialized_components.append('metrics_system')
    logger.info('Metrics system initialized')
    await initialize_pagination_system()
    initialized_components.append('pagination_system')
    logger.info('Pagination system initialized')
    await initialize_ratelimiting_system()
    initialized_components.append('ratelimiting_system')
    logger.info('Rate limiting system initialized')
    await initialize_cache()
    initialized_components.append('cache')
    logger.info('Cache system initialized')
    if initialize_event_system():
        initialized_components.append('event_system')
        logger.info('Event system initialized')
    audit_service = get_audit_service()
    await audit_service.initialize()
    initialized_components.append('audit_service')
    logger.info('Audit service initialized')
    await initialize_services()
    initialized_components.append('services_initialized')
    logger.info('Services initialized')
    await initialize_as400_sync()
    initialized_components.append('as400_sync')
    logger.info('AS400 sync initialized')
    try:
        media_service = get_service('media_service')
        await media_service.initialize()
        initialized_components.append('media_service')
        logger.info('Media service initialized')
    except Exception as e:
        logger.error(f'Error initializing media service: {str(e)}', exc_info=True)
    logger.info(f'Application started in {settings.ENVIRONMENT.value} environment')
    yield
    logger.info('Beginning application shutdown sequence')
    for component in reversed(initialized_components):
        try:
            logger.info(f'Shutting down {component}')
            if component == 'as400_sync':
                await shutdown_as400_sync()
            elif component == 'services_initialized':
                await shutdown_services()
            elif component == 'ratelimiting_system':
                await shutdown_ratelimiting_system()
            elif component == 'pagination_system':
                await shutdown_pagination_system()
            elif component == 'metrics_system':
                await shutdown_metrics_system()
            elif component == 'validation_system':
                await shutdown_validation_system()
            elif component == 'error_system':
                await shutdown_error_system()
            logger.info(f'{component} shutdown complete')
        except Exception as e:
            logger.error(f'Error during {component} shutdown: {str(e)}', exc_info=True)
    logger.info('Application shutdown complete')
    try:
        if 'logging' in initialized_components:
            await shutdown_logging()
    except Exception as e:
        print(f'Error during logging shutdown: {str(e)}')
DEFAULT_MIDDLEWARE_EXCLUDE_PATHS = getattr(settings, 'MIDDLEWARE_EXCLUDE_PATHS', ['/api/v1/docs', '/api/v1/redoc', '/api/v1/openapi.json', '/static/', '/media/'])
app = FastAPI(title=settings.PROJECT_NAME, description=settings.DESCRIPTION, version=settings.VERSION, openapi_url=f'{settings.API_V1_STR}/openapi.json', docs_url=f'{settings.API_V1_STR}/docs', redoc_url=f'{settings.API_V1_STR}/redoc', lifespan=lifespan)
app.include_router(api_router, prefix=settings.API_V1_STR)
add_typed_middleware(app, ErrorHandlerMiddleware)
add_typed_middleware(app, CompressionMiddleware, minimum_size=getattr(settings, 'COMPRESSION_MINIMUM_SIZE', 1000), compression_level=getattr(settings, 'COMPRESSION_LEVEL', 6), exclude_paths=DEFAULT_MIDDLEWARE_EXCLUDE_PATHS)
add_typed_middleware(app, ResponseFormatterMiddleware, exclude_paths=DEFAULT_MIDDLEWARE_EXCLUDE_PATHS)
add_typed_middleware(app, CacheControlMiddleware, exclude_paths=DEFAULT_MIDDLEWARE_EXCLUDE_PATHS)
add_typed_middleware(app, SecurityHeadersMiddleware, content_security_policy=settings.CONTENT_SECURITY_POLICY, permissions_policy=settings.PERMISSIONS_POLICY, exclude_paths=DEFAULT_MIDDLEWARE_EXCLUDE_PATHS)
if settings.BACKEND_CORS_ORIGINS:
    add_typed_middleware(app, EnhancedCORSMiddleware, allow_origins=settings.BACKEND_CORS_ORIGINS, allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
if settings.ENVIRONMENT != Environment.DEVELOPMENT:
    add_typed_middleware(app, TimeoutMiddleware, timeout_seconds=getattr(settings, 'REQUEST_TIMEOUT_SECONDS', 30.0), exclude_paths=DEFAULT_MIDDLEWARE_EXCLUDE_PATHS)
if settings.ENVIRONMENT != Environment.DEVELOPMENT or settings.RATE_LIMIT_ENABLED:
    add_typed_middleware(app, RateLimitMiddleware, rules=[RateLimitRule(requests_per_window=settings.RATE_LIMIT_REQUESTS_PER_MINUTE, window_seconds=60, strategy=RateLimitStrategy.IP, exclude_paths=DEFAULT_MIDDLEWARE_EXCLUDE_PATHS + ['/health']), RateLimitRule(requests_per_window=10, window_seconds=60, strategy=RateLimitStrategy.IP, path_pattern='/api/v1/auth/')], use_redis=settings.RATE_LIMIT_STORAGE == 'redis', enable_headers=True, block_exceeding_requests=True, fallback_to_memory=True)
add_typed_middleware(app, SecureRequestMiddleware, block_suspicious_requests=True, exclude_paths=DEFAULT_MIDDLEWARE_EXCLUDE_PATHS)
add_typed_middleware(app, MetricsMiddleware, ignore_paths=getattr(settings, 'METRICS_IGNORE_PATHS', ['/metrics', '/api/v1/metrics']))
add_typed_middleware(app, TracingMiddleware, service_name=settings.PROJECT_NAME)
add_typed_middleware(app, RequestContextMiddleware)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
media_path = Path(settings.MEDIA_ROOT).resolve()
app.mount('/media', StaticFiles(directory=media_path), name='media')
async def log_current_user(current_user: User=Depends(get_current_user)) -> Optional[User]:
    if current_user:
        set_user_id(str(current_user.id))
    return current_user
@app.get('/health')
async def health_check() -> dict:
    return {'status': 'healthy', 'environment': settings.ENVIRONMENT.value, 'version': settings.VERSION}
if __name__ == '__main__' and os.getenv('RUN_MAIN') != 'true':
    host = '0.0.0.0'
    port = 8000
    uvicorn.run('app.main:app', host=host, port=port, reload=settings.ENVIRONMENT == Environment.DEVELOPMENT)