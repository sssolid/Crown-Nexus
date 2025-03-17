from __future__ import annotations
import logging
import time
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator, Callable, Optional
from fastapi import FastAPI, Request, Response, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import AppException, app_exception_handler, validation_exception_handler, http_exception_handler, generic_exception_handler
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.middleware.response_formatter import ResponseFormatterMiddleware
from app.middleware.security import SecurityHeadersMiddleware, SecureRequestMiddleware
from app.core.rate_limiter import RateLimitMiddleware, RateLimitRule, RateLimitStrategy
from app.api.deps import get_current_user
from app.api.v1.router import api_router
from app.core.config import Environment, settings
from app.core.logging import get_logger, request_context, set_user_id
from app.core.service_registry import register_services, initialize_services, shutdown_services
from app.core.cache.manager import initialize_cache
from app.fitment.api import router as fitment_router
from app.fitment.dependencies import initialize_mapping_engine
from app.models.user import User
import uvicorn
logger = get_logger('app.main')
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    initialize_cache()
    register_services()
    await initialize_services()
    await initialize_mapping_engine()
    logger.info(f'Application started in {settings.ENVIRONMENT.value} environment')
    yield
    await shutdown_services()
    logger.info('Application shutdown complete')
app = FastAPI(title=settings.PROJECT_NAME, description=settings.DESCRIPTION, version=settings.VERSION, openapi_url=f'{settings.API_V1_STR}/openapi.json', docs_url=f'{settings.API_V1_STR}/docs', redoc_url=f'{settings.API_V1_STR}/redoc', lifespan=lifespan)
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(CORSMiddleware, allow_origins=settings.BACKEND_CORS_ORIGINS, allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
class RequestContextMiddleware:
    def __init__(self, app: Callable) -> None:
        self.app = app
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        request_id = str(uuid.uuid4())
        start_time = time.time()
        request.state.request_id = request_id
        with request_context(request_id):
            logger.info(f'Request: {request.method} {request.url.path}', method=request.method, path=request.url.path, client=request.client.host if request.client else None)
            response = await call_next(request)
            execution_time = time.time() - start_time
            logger.info(f'Response: {response.status_code}', status_code=response.status_code, execution_time=f'{execution_time:.4f}s')
            response.headers['X-Request-ID'] = request_id
            response.headers['X-Execution-Time'] = f'{execution_time:.4f}s'
            return response
app.add_middleware(RequestContextMiddleware)
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(ResponseFormatterMiddleware)
if settings.ENVIRONMENT != Environment.DEVELOPMENT or settings.security.RATE_LIMIT_ENABLED:
    app.add_middleware(RateLimitMiddleware, rules=[RateLimitRule(requests_per_window=settings.security.RATE_LIMIT_REQUESTS_PER_MINUTE, window_seconds=60, strategy=RateLimitStrategy.IP, exclude_paths=['/api/v1/health', '/static/']), RateLimitRule(requests_per_window=10, window_seconds=60, strategy=RateLimitStrategy.IP, path_pattern='/api/v1/auth/')], use_redis=settings.security.RATE_LIMIT_STORAGE == 'redis', enable_headers=True, block_exceeding_requests=True)
app.add_middleware(SecurityHeadersMiddleware, content_security_policy=settings.security.CONTENT_SECURITY_POLICY, permissions_policy=settings.security.PERMISSIONS_POLICY)
app.add_middleware(SecureRequestMiddleware, block_suspicious_requests=True)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(fitment_router, prefix=f'{settings.API_V1_STR}/fitment', tags=['fitment'])
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