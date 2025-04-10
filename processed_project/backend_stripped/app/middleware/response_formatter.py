from __future__ import annotations
'\nResponse formatter middleware for the application.\n\nThis middleware ensures all API responses follow a consistent format,\nwith success flag, data, and metadata.\n'
import datetime
import json
import time
from typing import Callable, Optional, Any, Dict
from fastapi import Request, Response
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.logging import get_logger
from app.core.dependency_manager import get_service
from app.core.metrics import MetricName
from app.utils.circuit_breaker_utils import safe_observe_histogram
logger = get_logger('app.middleware.response_formatter')
class ResponseFormatterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: Any, exclude_paths: Optional[list[str]]=None, skip_binary_responses: bool=True) -> None:
        super().__init__(app)
        self.exclude_paths = exclude_paths or ['/docs', '/redoc', '/openapi.json', '/static/', '/media/']
        self.skip_binary_responses = skip_binary_responses
        logger.info('ResponseFormatterMiddleware initialized')
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        path = request.url.path
        if any((path.startswith(exc) for exc in self.exclude_paths)):
            return await call_next(request)
        metrics_service: Optional[Any] = None
        try:
            metrics_service = get_service('metrics_service')
        except Exception:
            pass
        start_time = time.time()
        formatted = False
        try:
            response = await call_next(request)
            if not isinstance(response, JSONResponse):
                if self.skip_binary_responses and (isinstance(response, (StreamingResponse, FileResponse)) or response.headers.get('Content-Type', '').startswith(('image/', 'audio/', 'video/', 'application/octet-stream'))):
                    return response
                return response
            try:
                body = response.body
                if not body:
                    return response
                try:
                    content = json.loads(body)
                except json.JSONDecodeError as e:
                    logger.warning(f'Failed to parse response JSON: {str(e)}', path=path, status_code=response.status_code)
                    return response
                if isinstance(content, dict) and 'success' in content:
                    if 'timestamp' not in content:
                        content['timestamp'] = datetime.datetime.now(datetime.UTC).isoformat()
                    formatted_response = JSONResponse(content=content, status_code=response.status_code, headers=dict(response.headers))
                    formatted = True
                    return formatted_response
                formatted_content = {'success': 200 <= response.status_code < 300, 'message': self._get_status_message(response.status_code), 'data': content, 'meta': self._build_metadata(request, response), 'timestamp': datetime.datetime.now(datetime.UTC).isoformat()}
                formatted_response = JSONResponse(content=formatted_content, status_code=response.status_code, headers=dict(response.headers))
                formatted = True
                return formatted_response
            except Exception as e:
                logger.error(f'Error formatting response: {str(e)}', exc_info=e, request_id=getattr(request.state, 'request_id', None), path=path, status_code=getattr(response, 'status_code', None))
                return response
        finally:
            if metrics_service:
                try:
                    duration = time.time() - start_time
                    safe_observe_histogram(MetricName.RESPONSE_FORMATTING_DURATION_SECONDS.value, duration, {'response_formatted': str(formatted), 'path': path})
                except Exception as e:
                    logger.debug(f'Failed to track formatting metrics: {str(e)}')
    def _get_status_message(self, status_code: int) -> str:
        if 200 <= status_code < 300:
            return 'OK'
        elif status_code == 400:
            return 'Bad Request'
        elif status_code == 401:
            return 'Unauthorized'
        elif status_code == 403:
            return 'Forbidden'
        elif status_code == 404:
            return 'Not Found'
        elif status_code == 422:
            return 'Validation Error'
        elif status_code == 429:
            return 'Too Many Requests'
        elif 400 <= status_code < 500:
            return 'Client Error'
        elif 500 <= status_code < 600:
            return 'Server Error'
        else:
            return 'Unknown'
    def _build_metadata(self, request: Request, response: Response) -> Dict[str, Any]:
        metadata: Dict[str, Any] = {'request_id': getattr(request.state, 'request_id', None)}
        pagination_headers = ['X-Total-Count', 'X-Page-Count', 'X-Page-Number', 'X-Page-Size', 'X-Has-Next', 'X-Has-Prev']
        pagination = {}
        for header in pagination_headers:
            if header in response.headers:
                key = header.replace('X-', '').replace('-', '_').lower()
                value = response.headers[header]
                if value.lower() in ('true', 'false'):
                    value = value.lower() == 'true'
                elif value.isdigit():
                    value = int(value)
                pagination[key] = value
        if pagination:
            metadata['pagination'] = pagination
        if hasattr(request.state, 'metadata') and isinstance(request.state.metadata, dict):
            metadata.update(request.state.metadata)
        return metadata