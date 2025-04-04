from __future__ import annotations
'\nCache control middleware for the application.\n\nThis middleware adds appropriate cache control headers to responses\nbased on the request path and method.\n'
from typing import Callable, Dict, Optional, Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.logging import get_logger
logger = get_logger('app.middleware.cache_control')
class CacheControlMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: Any, cache_rules: Optional[Dict[str, str]]=None, default_rule: str='no-store, no-cache, must-revalidate, max-age=0', cacheable_methods: Optional[list[str]]=None, exclude_paths: Optional[list[str]]=None) -> None:
        super().__init__(app)
        self.cache_rules = cache_rules or {'/static/': 'public, max-age=86400, stale-while-revalidate=3600', '/media/': 'public, max-age=86400, stale-while-revalidate=3600', '/api/v1/docs': 'public, max-age=3600', '/api/v1/redoc': 'public, max-age=3600', '/api/v1/openapi.json': 'public, max-age=3600', '/api/v1/health': 'public, max-age=60'}
        self.default_rule = default_rule
        self.cacheable_methods = cacheable_methods or ['GET', 'HEAD']
        self.exclude_paths = exclude_paths or []
        logger.info('CacheControlMiddleware initialized')
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        path = request.url.path
        method = request.method
        if any((path.startswith(exc) for exc in self.exclude_paths)):
            return await call_next(request)
        response = await call_next(request)
        if 'Cache-Control' in response.headers:
            return response
        if method not in self.cacheable_methods:
            response.headers['Cache-Control'] = 'no-store'
            return response
        cache_control = self.default_rule
        for path_prefix, rule in self.cache_rules.items():
            if path.startswith(path_prefix):
                cache_control = rule
                break
        response.headers['Cache-Control'] = cache_control
        response.headers['Vary'] = 'Accept-Encoding, Cookie, Authorization'
        return response