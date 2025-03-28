from __future__ import annotations
import time
from typing import Callable
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.routing import Route, Match
from app.logging import get_logger
from app.core.metrics import track_request, set_gauge, MetricName, MetricTag
logger = get_logger('app.middleware.metrics')
class MetricsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)
        self._fastapi_app = app
        logger.info('MetricsMiddleware initialized')
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.monotonic()
        endpoint = self._get_endpoint_name(request)
        labels = {MetricTag.METHOD: request.method, MetricTag.ENDPOINT: endpoint}
        try:
            set_gauge(MetricName.HTTP_IN_PROGRESS, 1, labels)
        except Exception as e:
            logger.error(f'Error tracking in-progress request: {str(e)}')
        error_code = None
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
            error_code = response.headers.get('X-Error-Code')
            return response
        except Exception as e:
            logger.error(f'Uncaught exception in request: {str(e)}')
            status_code = 500
            error_code = type(e).__name__
            raise
        finally:
            duration = time.monotonic() - start_time
            try:
                track_request(method=request.method, endpoint=endpoint, status_code=status_code, duration=duration, error_code=error_code)
                set_gauge(MetricName.HTTP_IN_PROGRESS, 0, labels)
            except Exception as e:
                logger.error(f'Error tracking request metrics: {str(e)}')
    def _get_endpoint_name(self, request: Request) -> str:
        if hasattr(self, '_fastapi_app') and hasattr(self._fastapi_app, 'routes'):
            try:
                for route in self._fastapi_app.routes:
                    match, scope = route.matches(request.scope)
                    if match == Match.FULL:
                        if isinstance(route, Route):
                            return route.name or route.path
                        return route.path
            except Exception as e:
                logger.warning(f'Error getting endpoint from routes: {str(e)}')
        path = request.url.path
        if path.endswith('/') and len(path) > 1:
            path = path[:-1]
        parts = path.split('/')
        if len(parts) > 3 and parts[1] == 'api' and parts[2].startswith('v'):
            return '/'.join(parts[3:])
        return path