from __future__ import annotations
from app.core.metrics import MetricName
from app.utils.circuit_breaker_utils import safe_observe_histogram
'\nTracing middleware for the application.\n\nThis middleware handles distributed tracing for request processing, allowing\nfor request tracking across services and components.\n'
import time
import uuid
from typing import Callable, Optional, Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.logging import get_logger, request_context
from app.core.dependency_manager import get_service
logger = get_logger('app.middleware.tracing')
class TracingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: Any, service_name: str='api', exclude_paths: Optional[list[str]]=None) -> None:
        super().__init__(app)
        self.service_name = service_name
        self.exclude_paths = exclude_paths or []
        logger.info('TracingMiddleware initialized', service_name=service_name)
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        path = request.url.path
        if any((path.startswith(exc) for exc in self.exclude_paths)):
            return await call_next(request)
        trace_id = request.headers.get('X-Trace-ID') or str(uuid.uuid4())
        span_id = str(uuid.uuid4())
        parent_span_id = request.headers.get('X-Span-ID')
        request.state.trace_id = trace_id
        request.state.span_id = span_id
        request.state.parent_span_id = parent_span_id
        metrics_service = None
        try:
            metrics_service = get_service('metrics_service')
        except Exception:
            pass
        start_time = time.monotonic()
        status_code = 500
        error = None
        with request_context(request_id=trace_id):
            logger.info('Starting request trace', trace_id=trace_id, span_id=span_id, parent_span_id=parent_span_id, path=path, method=request.method, service=self.service_name)
            try:
                response = await call_next(request)
                status_code = response.status_code
                response.headers['X-Trace-ID'] = trace_id
                response.headers['X-Span-ID'] = span_id
                if parent_span_id:
                    response.headers['X-Parent-Span-ID'] = parent_span_id
                return response
            except Exception as e:
                error = str(e)
                raise
            finally:
                duration = time.monotonic() - start_time
                logger.info('Completed request trace', trace_id=trace_id, span_id=span_id, duration=duration, status_code=status_code, path=path, method=request.method, service=self.service_name, error=error)
                if metrics_service:
                    try:
                        safe_observe_histogram(MetricName.REQUEST_TRACE_DURATION_SECONDS.value, duration, {'path': path, 'method': request.method, 'status_code': str(status_code // 100) + 'xx', 'error_code': 'true' if error else 'false'})
                    except Exception as e:
                        logger.debug(f'Failed to track tracing metrics: {str(e)}')