from __future__ import annotations
from app.utils.circuit_breaker_utils import safe_increment_counter
"\nEnhanced CORS middleware for the application.\n\nThis middleware provides more detailed logging and metrics for CORS requests\nwhile extending the functionality of FastAPI's built-in CORSMiddleware.\n"
from typing import Callable, Optional, Any, List, Dict, Union
from fastapi import Request, Response
from starlette.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp
from app.logging import get_logger
from app.core.dependency_manager import get_service
logger = get_logger('app.middleware.cors')
class EnhancedCORSMiddleware(CORSMiddleware):
    def __init__(self, app: ASGIApp, allow_origins: Union[List[str], str]=(), allow_methods: Union[List[str], str]=('GET',), allow_headers: Union[List[str], str]=(), allow_credentials: bool=False, allow_origin_regex: Optional[str]=None, expose_headers: Union[List[str], str]=(), max_age: int=600) -> None:
        super().__init__(app=app, allow_origins=allow_origins, allow_methods=allow_methods, allow_headers=allow_headers, allow_credentials=allow_credentials, allow_origin_regex=allow_origin_regex, expose_headers=expose_headers, max_age=max_age)
        if isinstance(allow_origins, list):
            allow_origins_str = ', '.join(allow_origins)
        else:
            allow_origins_str = allow_origins
        if isinstance(allow_methods, list):
            allow_methods_str = ', '.join(allow_methods)
        else:
            allow_methods_str = allow_methods
        if isinstance(allow_headers, list):
            allow_headers_str = ', '.join(allow_headers)
        else:
            allow_headers_str = allow_headers
        logger.info('EnhancedCORSMiddleware initialized', allow_origins=allow_origins_str, allow_methods=allow_methods_str, allow_headers=allow_headers_str, allow_credentials=allow_credentials, allow_origin_regex=allow_origin_regex, max_age=max_age)
    async def __call__(self, scope: Dict[str, Any], receive: Callable, send: Callable) -> None:
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return
        request = Request(scope)
        origin = request.headers.get('origin')
        is_cors_request = origin is not None
        is_preflight_request = is_cors_request and request.method == 'OPTIONS'
        metrics_service = None
        try:
            metrics_service = get_service('metrics_service')
        except Exception:
            pass
        if is_cors_request:
            logger.debug('CORS request received', path=request.url.path, origin=origin, method=request.method, is_preflight=is_preflight_request)
            if metrics_service:
                try:
                    safe_increment_counter('cors_requests_total', 1, {'path': request.url.path, 'method': request.method, 'is_preflight': str(is_preflight_request)})
                except Exception as e:
                    logger.debug(f'Failed to track CORS metrics: {str(e)}')
        async def wrapped_send(message: Dict[str, Any]) -> None:
            if message['type'] == 'http.response.start' and is_cors_request:
                headers = dict(message.get('headers', []))
                headers_dict = {k.decode(): v.decode() for k, v in headers.items()}
                is_allowed = 'access-control-allow-origin' in headers_dict
                if is_allowed:
                    logger.debug('CORS request allowed', path=request.url.path, origin=origin, method=request.method, is_preflight=is_preflight_request)
                else:
                    logger.warning('CORS request denied', path=request.url.path, origin=origin, method=request.method, is_preflight=is_preflight_request)
                if metrics_service:
                    try:
                        safe_increment_counter('cors_responses_total', 1, {'path': request.url.path, 'method': request.method, 'is_preflight': str(is_preflight_request), 'is_allowed': str(is_allowed)})
                    except Exception as e:
                        logger.debug(f'Failed to track CORS metrics: {str(e)}')
            await send(message)
        await super().__call__(scope, receive, wrapped_send)