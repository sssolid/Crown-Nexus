from __future__ import annotations
'\nRequest context middleware for the application.\n\nThis middleware sets up the request context for each incoming request,\nincluding request ID generation and logging of request/response information.\n'
import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.logging.context import get_logger, request_context
logger = get_logger('app.middleware.request_context')
class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get('X-Request-ID') or str(uuid.uuid4())
        start_time = time.time()
        request.state.request_id = request_id
        with request_context(request_id):
            logger.info(f'Request: {request.method} {request.url.path}', method=request.method, path=request.url.path, query=str(request.query_params), client=request.client.host if request.client else None)
            response = await call_next(request)
            execution_time = time.time() - start_time
            logger.info(f'Response: {response.status_code}', status_code=response.status_code, execution_time=f'{execution_time:.4f}s')
            response.headers['X-Request-ID'] = request_id
            response.headers['X-Execution-Time'] = f'{execution_time:.4f}s'
            return response