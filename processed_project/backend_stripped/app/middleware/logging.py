from __future__ import annotations
'\nLogging middleware for the application.\n\nThis middleware handles request logging, including request ID generation,\ntiming, and structured log output for requests and responses.\n'
import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.logging.context import get_logger, request_context
logger = get_logger('app.middleware.logging')
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        logger.info('RequestLoggingMiddleware initialized')
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get('X-Request-ID') or str(uuid.uuid4())
        start_time = time.time()
        request.state.request_id = request_id
        with request_context(request_id):
            logger.info(f'Request: {request.method} {request.url.path}', method=request.method, path=request.url.path, query=str(request.query_params), client=request.client.host if request.client else None)
            try:
                response = await call_next(request)
                execution_time = time.time() - start_time
                logger.info(f'Response: {response.status_code}', status_code=response.status_code, execution_time=f'{execution_time:.4f}s')
                response.headers['X-Request-ID'] = request_id
                response.headers['X-Execution-Time'] = f'{execution_time:.4f}s'
                return response
            except Exception as e:
                execution_time = time.time() - start_time
                logger.exception(f'Error processing request: {str(e)}', exc_info=e, execution_time=f'{execution_time:.4f}s')
                raise