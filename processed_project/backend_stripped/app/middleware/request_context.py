from __future__ import annotations
import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import get_logger, request_context
logger = get_logger('app.middleware.request_context')
class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = str(uuid.uuid4())
        start_time = time.time()
        request.state.request_id = request_id
        with request_context(request_id):
            logger.info(f'Request: {request.method} {request.url.path}', extra={'method': request.method, 'path': request.url.path, 'client': request.client.host if request.client else None})
            response = await call_next(request)
            execution_time = time.time() - start_time
            logger.info(f'Response: {response.status_code}', extra={'status_code': response.status_code, 'execution_time': f'{execution_time:.4f}s'})
            response.headers['X-Request-ID'] = request_id
            response.headers['X-Execution-Time'] = f'{execution_time:.4f}s'
            return response