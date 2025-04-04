from __future__ import annotations
from app.core.metrics import MetricName
from app.utils.circuit_breaker_utils import safe_increment_counter, safe_observe_histogram
'\nRequest context middleware for the application.\n\nThis middleware sets up the request context for each incoming request,\nincluding request ID generation and logging of request/response information.\n'
import time
import uuid
from typing import Callable, Any, Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.logging.context import get_logger, request_context, set_user_id, clear_user_id
from app.core.dependency_manager import get_service
logger = get_logger('app.middleware.request_context')
class RequestContextMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: Any) -> None:
        super().__init__(app)
        logger.info('RequestContextMiddleware initialized')
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        metrics_service: Optional[Any] = None
        try:
            metrics_service = get_service('metrics_service')
        except Exception:
            pass
        request_id = request.headers.get('X-Request-ID') or str(uuid.uuid4())
        start_time = time.time()
        user_id = request.headers.get('X-User-ID')
        request.state.request_id = request_id
        if user_id:
            request.state.user_id = user_id
        with request_context(request_id, user_id=user_id):
            logger.info(f'Request: {request.method} {request.url.path}', method=request.method, path=request.url.path, query=str(request.query_params), client=request.client.host if request.client else None, user_agent=request.headers.get('User-Agent'), referrer=request.headers.get('Referer'), content_type=request.headers.get('Content-Type'), accept=request.headers.get('Accept'))
            try:
                response = await call_next(request)
                execution_time = time.time() - start_time
                logger.info(f'Response: {response.status_code}', status_code=response.status_code, execution_time=f'{execution_time:.4f}s', content_type=response.headers.get('Content-Type'), content_length=response.headers.get('Content-Length'))
                if metrics_service:
                    try:
                        safe_observe_histogram(MetricName.HTTP_REQUEST_DURATION_SECONDS.value, execution_time, {'method': request.method, 'endpoint': request.url.path, 'status_code': str(response.status_code // 100) + 'xx'})
                    except Exception as e:
                        logger.debug(f'Failed to record metrics: {e}')
                response.headers['X-Request-ID'] = request_id
                response.headers['X-Execution-Time'] = f'{execution_time:.4f}s'
                return response
            except Exception as e:
                execution_time = time.time() - start_time
                logger.exception(f'Error processing request: {str(e)}', exc_info=e, method=request.method, path=request.url.path, execution_time=f'{execution_time:.4f}s')
                if metrics_service:
                    try:
                        safe_increment_counter(MetricName.HTTP_REQUEST_ERRORS_TOTAL.value, 1, {'method': request.method, 'endpoint': request.url.path, 'error_type': type(e).__name__})
                    except Exception as metrics_err:
                        logger.debug(f'Failed to record error metrics: {metrics_err}')
                raise
            finally:
                if user_id:
                    clear_user_id()