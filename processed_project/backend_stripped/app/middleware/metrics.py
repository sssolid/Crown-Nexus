from __future__ import annotations
from app.utils.circuit_breaker_utils import safe_observe_histogram, safe_increment_counter
'\nMetrics middleware for the application.\n\nThis middleware collects and tracks metrics for HTTP requests, providing\ninsights into application performance and usage patterns.\n'
import time
from typing import Callable, Dict, Optional, Any, List
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.routing import Route, Match
from app.logging import get_logger
from app.core.metrics import track_request, set_gauge, increment_counter, observe_histogram, MetricName, MetricTag
from app.core.dependency_manager import get_service
logger = get_logger('app.middleware.metrics')
class MetricsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, ignore_paths: Optional[List[str]]=None, track_paths_without_match: bool=False) -> None:
        super().__init__(app)
        self._fastapi_app = app
        self.ignore_paths = ignore_paths or ['/metrics', '/api/v1/metrics']
        self.track_paths_without_match = track_paths_without_match
        logger.info('MetricsMiddleware initialized', ignore_paths=self.ignore_paths, track_paths_without_match=track_paths_without_match)
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        path = request.url.path
        if any((path.startswith(ignore) for ignore in self.ignore_paths)):
            return await call_next(request)
        start_time = time.monotonic()
        endpoint = self._get_endpoint_name(request)
        if not endpoint and (not self.track_paths_without_match):
            return await call_next(request)
        labels = {MetricTag.METHOD: request.method, MetricTag.ENDPOINT: endpoint or path}
        try:
            set_gauge(MetricName.HTTP_IN_PROGRESS, 1, labels)
        except Exception as e:
            logger.error(f'Error tracking in-progress request: {str(e)}')
        error_code = None
        status_code = 500
        exception_name = None
        try:
            metrics_service = None
            try:
                metrics_service = get_service('metrics_service')
            except Exception:
                pass
            if metrics_service:
                try:
                    user_agent = request.headers.get('User-Agent', 'unknown')
                    user_agent_type = self._classify_user_agent(user_agent)
                    safe_increment_counter(MetricName.HTTP_REQUESTS_BY_AGENT_TOTAL.value, 1, {'agent_type': user_agent_type, 'endpoint': endpoint or path})
                except Exception as e:
                    logger.debug(f'Failed to track user agent metrics: {e}')
            response = await call_next(request)
            status_code = response.status_code
            error_code = response.headers.get('X-Error-Code')
            if metrics_service and 'Content-Length' in response.headers:
                try:
                    content_length = int(response.headers['Content-Length'])
                    safe_observe_histogram(MetricName.HTTP_RESPONSE_SIZE_BYTES.value, content_length, {'path': endpoint or path, 'method': request.method})
                except (ValueError, Exception) as e:
                    logger.debug(f'Failed to track response size metrics: {e}')
            return response
        except Exception as e:
            logger.error(f'Uncaught exception in request: {str(e)}')
            status_code = 500
            error_code = type(e).__name__
            exception_name = type(e).__name__
            raise
        finally:
            duration = time.monotonic() - start_time
            try:
                track_request(method=request.method, endpoint=endpoint or path, status_code=status_code, duration=duration, error_code=error_code)
                if exception_name:
                    try:
                        increment_counter('http_exceptions_total', 1, {'method': request.method, 'endpoint': endpoint or path, 'exception': exception_name})
                    except Exception as e:
                        logger.debug(f'Failed to track exception metrics: {e}')
                try:
                    status_code = f'{status_code // 100}xx'
                    increment_counter(MetricName.HTTP_STATUS_CODES_TOTAL.value, 1, {'method': request.method, 'endpoint': endpoint or path, 'status_code': status_code})
                except Exception as e:
                    logger.debug(f'Failed to track status code metrics: {e}')
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
                            return route.name or self._normalize_path(route.path)
                        return self._normalize_path(route.path)
            except Exception as e:
                logger.warning(f'Error getting endpoint from routes: {str(e)}')
        return self._normalize_path(request.url.path)
    def _normalize_path(self, path: str) -> str:
        if path.endswith('/') and len(path) > 1:
            path = path[:-1]
        parts = path.split('/')
        if len(parts) > 3 and parts[1] == 'api' and parts[2].startswith('v'):
            return '/'.join(parts[3:])
        return path
    def _classify_user_agent(self, user_agent: str) -> str:
        user_agent = user_agent.lower()
        if 'mozilla' in user_agent:
            if 'chrome' in user_agent:
                return 'browser_chrome'
            elif 'firefox' in user_agent:
                return 'browser_firefox'
            elif 'safari' in user_agent and 'chrome' not in user_agent:
                return 'browser_safari'
            elif 'edg' in user_agent:
                return 'browser_edge'
            else:
                return 'browser_other'
        elif 'curl' in user_agent:
            return 'tool_curl'
        elif 'wget' in user_agent:
            return 'tool_wget'
        elif 'postman' in user_agent:
            return 'tool_postman'
        elif 'python' in user_agent:
            return 'script_python'
        elif 'java' in user_agent:
            return 'script_java'
        elif 'bot' in user_agent or 'crawler' in user_agent or 'spider' in user_agent:
            return 'bot'
        elif not user_agent or user_agent == 'unknown':
            return 'unknown'
        else:
            return 'other'