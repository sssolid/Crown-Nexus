from __future__ import annotations
import time
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator, Callable, Optional
from fastapi import FastAPI, Request, Response, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import AppException, app_exception_handler, validation_exception_handler, generic_exception_handler
from app.middleware.metrics import MetricsMiddleware
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.middleware.request_context import RequestContextMiddleware
from app.middleware.response_formatter import ResponseFormatterMiddleware
from app.middleware.security import SecurityHeadersMiddleware, SecureRequestMiddleware
from app.middleware.rate_limiting import RateLimitMiddleware
from app.api.deps import get_current_user
from app.core.config import Environment, settings
from app.core.logging import get_logger, request_context, set_user_id
from app.core.error import initialize as initialize_error_system, shutdown as shutdown_error_system
from app.core.validation import initialize as initialize_validation_system, shutdown as shutdown_validation_system
from app.core.metrics import initialize as initialize_metrics_system, shutdown as shutdown_metrics_system
from app.core.rate_limiting import initialize as initialize_ratelimiting_system, shutdown as shutdown_ratelimiting_system, RateLimitRule, RateLimitStrategy
from app.core.pagination import initialize as initialize_pagination_system, shutdown as shutdown_pagination_system
from app.core.dependency_manager import register_services, initialize_services, shutdown_services
from app.core.cache.manager import initialize_cache
from app.fitment.api import router as fitment_router
from app.fitment.dependencies import initialize_mapping_engine
from app.core.startup.as400_sync import initialize_as400_sync, shutdown_as400_sync
from app.models.user import User
import uvicorn
logger = get_logger('app.main')
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    register_services()
    await initialize_error_system()
    await initialize_validation_system()
    await initialize_metrics_system()
    await initialize_pagination_system()
    await initialize_ratelimiting_system()
    await initialize_cache()
    await initialize_services()
    await initialize_mapping_engine()
    await initialize_as400_sync()
    logger.info(f'Application started in {settings.ENVIRONMENT.value} environment')
    from app.api.v1.router import api_router
    app.include_router(api_router, prefix=settings.API_V1_STR)
    app.include_router(fitment_router, prefix=f'{settings.API_V1_STR}/fitment', tags=['fitment'])
    yield
    await shutdown_as400_sync()
    await shutdown_services()
    await shutdown_ratelimiting_system()
    await shutdown_pagination_system()
    await shutdown_metrics_system()
    await shutdown_validation_system()
    await shutdown_error_system()
    logger.info('Application shutdown complete')
app = FastAPI(title=settings.PROJECT_NAME, description=settings.DESCRIPTION, version=settings.VERSION, openapi_url=f'{settings.API_V1_STR}/openapi.json', docs_url=f'{settings.API_V1_STR}/docs', redoc_url=f'{settings.API_V1_STR}/redoc', lifespan=lifespan)
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(CORSMiddleware, allow_origins=settings.BACKEND_CORS_ORIGINS, allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
app.add_middleware(RequestContextMiddleware)
app.add_middleware(MetricsMiddleware)
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(ResponseFormatterMiddleware)
app.add_middleware(SecurityHeadersMiddleware, content_security_policy=settings.CONTENT_SECURITY_POLICY, permissions_policy=settings.PERMISSIONS_POLICY)
app.add_middleware(SecureRequestMiddleware, block_suspicious_requests=True)
if settings.ENVIRONMENT != Environment.DEVELOPMENT or settings.RATE_LIMIT_ENABLED:
    app.add_middleware(RateLimitMiddleware, rules=[RateLimitRule(requests_per_window=settings.RATE_LIMIT_REQUESTS_PER_MINUTE, window_seconds=60, strategy=RateLimitStrategy.IP, exclude_paths=['/api/v1/health', '/static/']), RateLimitRule(requests_per_window=10, window_seconds=60, strategy=RateLimitStrategy.IP, path_pattern='/api/v1/auth/')], use_redis=settings.RATE_LIMIT_STORAGE == 'redis', enable_headers=True, block_exceeding_requests=True)
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