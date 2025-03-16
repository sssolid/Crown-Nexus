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
from app.api.deps import get_current_user
from app.api.v1.router import api_router
from app.core.config import Environment, settings
from app.core.logging import setup_logging, get_logger, request_context, set_user_id
from app.fitment.api import router as fitment_router
from app.fitment.dependencies import initialize_mapping_engine
from app.models.user import User
setup_logging()
logger = get_logger('app.main')
class RequestContextMiddleware:
    def __init__(self, app: FastAPI) -> None:
        self.app = app
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
        start_time = time.time()
        with request_context(request_id=request_id):
            try:
                request.state.request_id = request_id
                response = await call_next(request)
                process_time = time.time() - start_time
                response.headers['X-Process-Time'] = f'{process_time:.4f}'
                response.headers['X-Request-ID'] = request_id
                status_code = response.status_code
                log_method = logger.info if status_code < 400 else logger.warning if status_code < 500 else logger.error
                log_method('Request completed', method=request.method, path=request.url.path, status_code=status_code, process_time=process_time)
                return response
            except Exception as e:
                process_time = time.time() - start_time
                logger.exception('Request failed', method=request.method, path=request.url.path, error=str(e), process_time=process_time)
                return JSONResponse(status_code=500, content={'detail': 'Internal server error'}, headers={'X-Request-ID': request_id})
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info('Application starting', app_name=settings.PROJECT_NAME, version=settings.VERSION, environment=settings.ENVIRONMENT.value)
    logger.info('Initializing fitment mapping engine')
    await initialize_mapping_engine()
    logger.info('Application startup complete')
    yield
    logger.info('Application shutting down')
    logger.info('Application shutdown complete')
app = FastAPI(title=settings.PROJECT_NAME, description=settings.DESCRIPTION, version=settings.VERSION, openapi_url=f'{settings.API_V1_STR}/openapi.json', docs_url=f'{settings.API_V1_STR}/docs', redoc_url=f'{settings.API_V1_STR}/redoc', lifespan=lifespan)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(RequestContextMiddleware)
app.add_middleware(ResponseFormatterMiddleware)
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(CORSMiddleware, allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
if settings.MEDIA_STORAGE_TYPE == 'local':
    media_path = Path(settings.MEDIA_ROOT).resolve()
    media_path.mkdir(parents=True, exist_ok=True)
    app.mount('/media', StaticFiles(directory=str(media_path)), name='media')
    logger.info('Media directory mounted', path=str(media_path))
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(fitment_router)
async def log_current_user(current_user: Optional[User]=Depends(get_current_user)) -> Optional[User]:
    if current_user:
        set_user_id(str(current_user.id))
    return current_user
@app.get('/health')
async def health_check() -> dict:
    return {'status': 'ok', 'version': settings.VERSION, 'service': settings.PROJECT_NAME, 'environment': settings.ENVIRONMENT.value}
if __name__ == '__main__':
    import uvicorn
    host = '0.0.0.0'
    port = 8000
    logger.info('Starting development server', host=host, port=port, url=f'http://{host}:{port}')
    uvicorn.run('app.main:app', host=host, port=port, reload=True, log_level=settings.fitment.FITMENT_LOG_LEVEL.lower())