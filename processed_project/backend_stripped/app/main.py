from __future__ import annotations
'\nMain application module.\n\nThis module initializes and configures the FastAPI application, including\nmiddleware, exception handlers, and application components.\n'
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncGenerator, Callable, Optional
import uvicorn
from fastapi import FastAPI, Depends, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from app.logging import reinitialize_logging, shutdown_logging, get_logger, set_user_id
import app.db.base
from app.api.deps import get_current_user
from app.core.cache.manager import initialize_cache
from app.core.config import Environment, settings
from app.core.dependency_manager import register_services, initialize_services, shutdown_services, get_service
from app.core.error import initialize as initialize_error_system, shutdown as shutdown_error_system
from app.core.events import EventBackendType, init_event_backend, init_domain_events, EventConfigurationException
from app.core.exceptions import AppException, app_exception_handler, validation_exception_handler, generic_exception_handler
from app.middleware.logging import RequestLoggingMiddleware
from app.core.metrics import initialize as initialize_metrics_system, shutdown as shutdown_metrics_system
from app.core.pagination import initialize as initialize_pagination_system, shutdown as shutdown_pagination_system
from app.core.rate_limiting import initialize as initialize_ratelimiting_system, shutdown as shutdown_ratelimiting_system, RateLimitRule, RateLimitStrategy
from app.core.startup.as400_sync import initialize_as400_sync, shutdown_as400_sync
from app.core.validation import initialize as initialize_validation_system, shutdown as shutdown_validation_system
from app.domains.users.models import User
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.middleware.metrics import MetricsMiddleware
from app.middleware.rate_limiting import RateLimitMiddleware
from app.middleware.response_formatter import ResponseFormatterMiddleware
from app.middleware.security import SecurityHeadersMiddleware, SecureRequestMiddleware
logger = get_logger('app.main')
def add_typed_middleware(app: FastAPI, middleware_class: Any, **options: Any) -> None:
    app.add_middleware(middleware_class, **options)
ExceptionHandlerType = Callable[[Request, Exception], Response | JSONResponse]
def initialize_event_system() -> None:
    for backend in [EventBackendType.CELERY, EventBackendType.MEMORY]:
        try:
            logger.info(f'Attempting to initialize event system with backend: {backend}')
            init_event_backend(backend)
            init_domain_events()
            logger.info(f'Successfully initialized event system with backend: {backend}')
            return
        except EventConfigurationException as e:
            logger.warning(f'Event configuration failed for backend {backend}: {e}')
        except Exception as e:
            logger.exception(f'Unexpected error initializing event system with backend {backend}')
    logger.critical('Failed to initialize any event system backend.')
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await reinitialize_logging()
    logger.info('Starting application initialization')
    await initialize_error_system()
    register_services()
    await initialize_validation_system()
    await initialize_metrics_system()
    await initialize_pagination_system()
    await initialize_ratelimiting_system()
    await initialize_cache()
    initialize_event_system()
    await initialize_services()
    await initialize_as400_sync()
    media_service = get_service('media_service')
    try:
        await media_service.initialize()
        logger.info('Media service initialized during startup')
    except Exception as e:
        logger.error(f'Error initializing media service: {str(e)}', exc_info=True)
    logger.info(f'Application started in {settings.ENVIRONMENT.value} environment')
    from app.api.v1.router import api_router
    app.include_router(api_router, prefix=settings.API_V1_STR)
    yield
    logger.info('Beginning application shutdown sequence')
    await shutdown_as400_sync()
    await shutdown_services()
    await shutdown_ratelimiting_system()
    await shutdown_pagination_system()
    await shutdown_metrics_system()
    await shutdown_validation_system()
    await shutdown_error_system()
    logger.info('Application shutdown complete')
    await shutdown_logging()
app = FastAPI(title=settings.PROJECT_NAME, description=settings.DESCRIPTION, version=settings.VERSION, openapi_url=f'{settings.API_V1_STR}/openapi.json', docs_url=f'{settings.API_V1_STR}/docs', redoc_url=f'{settings.API_V1_STR}/redoc', lifespan=lifespan)
if settings.BACKEND_CORS_ORIGINS:
    add_typed_middleware(app, CORSMiddleware, allow_origins=settings.BACKEND_CORS_ORIGINS, allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
add_typed_middleware(app, RequestLoggingMiddleware)
add_typed_middleware(app, MetricsMiddleware)
add_typed_middleware(app, ErrorHandlerMiddleware)
add_typed_middleware(app, ResponseFormatterMiddleware)
add_typed_middleware(app, SecurityHeadersMiddleware, content_security_policy=settings.CONTENT_SECURITY_POLICY, permissions_policy=settings.PERMISSIONS_POLICY)
add_typed_middleware(app, SecureRequestMiddleware, block_suspicious_requests=True)
if settings.ENVIRONMENT != Environment.DEVELOPMENT or settings.RATE_LIMIT_ENABLED:
    add_typed_middleware(app, RateLimitMiddleware, rules=[RateLimitRule(requests_per_window=settings.RATE_LIMIT_REQUESTS_PER_MINUTE, window_seconds=60, strategy=RateLimitStrategy.IP, exclude_paths=['/api/v1/health', '/static/']), RateLimitRule(requests_per_window=10, window_seconds=60, strategy=RateLimitStrategy.IP, path_pattern='/api/v1/auth/')], use_redis=settings.RATE_LIMIT_STORAGE == 'redis', enable_headers=True, block_exceeding_requests=True)
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
if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8000
    uvicorn.run('app.main:app', host=host, port=port, reload=settings.ENVIRONMENT == Environment.DEVELOPMENT)