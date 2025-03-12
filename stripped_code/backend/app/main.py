from __future__ import annotations
import logging
import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.v1.router import api_router
from app.core.config import settings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info('Starting up application')
    yield
    logger.info('Shutting down application')
app = FastAPI(title=settings.PROJECT_NAME, description=settings.DESCRIPTION, version=settings.VERSION, openapi_url=f'{settings.API_V1_STR}/openapi.json', docs_url=f'{settings.API_V1_STR}/docs', redoc_url=f'{settings.API_V1_STR}/redoc', lifespan=lifespan)
@app.middleware('http')
async def add_process_time_header(request: Request, call_next: Callable) -> Response:
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers['X-Process-Time'] = f'{process_time:.4f}'
        return response
    except Exception as e:
        logger.exception(f'Request failed: {str(e)}')
        return JSONResponse(status_code=500, content={'detail': 'Internal server error'})
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(CORSMiddleware, allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
app.include_router(api_router, prefix=settings.API_V1_STR)
@app.get('/health')
async def health_check() -> dict:
    return {'status': 'ok', 'version': settings.VERSION, 'service': settings.PROJECT_NAME}
if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app.main:app', host='0.0.0.0', port=8000, reload=True)