from __future__ import annotations
import json
from typing import Callable, Optional, Dict, Any
from fastapi import FastAPI, Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.core.exceptions import SecurityException
from app.core.logging import get_logger
logger = get_logger('app.middleware.security')
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, content_security_policy: Optional[str]=None, permissions_policy: Optional[str]=None, expect_ct: Optional[str]=None) -> None:
        super().__init__(app)
        self.content_security_policy: str = content_security_policy or settings.CONTENT_SECURITY_POLICY
        self.permissions_policy: str = permissions_policy or settings.PERMISSIONS_POLICY
        self.expect_ct: Optional[str] = expect_ct
        logger.info('SecurityHeadersMiddleware initialized')
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        try:
            response: Response = await call_next(request)
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'DENY'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            response.headers['Content-Security-Policy'] = self.content_security_policy
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
            if self.permissions_policy:
                response.headers['Permissions-Policy'] = self.permissions_policy
            if self.expect_ct:
                response.headers['Expect-CT'] = self.expect_ct
            return response
        except Exception as e:
            raise
class SecureRequestMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, block_suspicious_requests: bool=True) -> None:
        super().__init__(app)
        self.block_suspicious_requests: bool = block_suspicious_requests
        self.suspicious_patterns: list[str] = ['../../', '<script', 'eval(', 'SELECT ']
        logger.info('SecureRequestMiddleware initialized')
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        if self.block_suspicious_requests and self._is_suspicious_request(request):
            logger.warning(f'Blocked suspicious request from {request.client.host}')
            raise SecurityException(message='Forbidden - Suspicious request detected', details={'ip': request.client.host}, status_code=status.HTTP_403_FORBIDDEN)
        return await call_next(request)
    def _is_suspicious_request(self, request: Request) -> bool:
        path = request.url.path
        for pattern in self.suspicious_patterns:
            if pattern.lower() in path.lower():
                logger.warning(f"Suspicious pattern '{pattern}' found in path: {path}")
                return True
        query_string = str(request.url.query)
        for pattern in self.suspicious_patterns:
            if pattern.lower() in query_string.lower():
                logger.warning(f"Suspicious pattern '{pattern}' found in query: {query_string}")
                return True
        for header_name, header_value in request.headers.items():
            for pattern in self.suspicious_patterns:
                if pattern.lower() in header_value.lower():
                    logger.warning(f"Suspicious pattern '{pattern}' found in header {header_name}")
                    return True
        async def check_body() -> bool:
            try:
                body = await request.body()
                if body:
                    body_str = body.decode('utf-8', errors='ignore')
                    for pattern in self.suspicious_patterns:
                        if pattern.lower() in body_str.lower():
                            logger.warning(f"Suspicious pattern '{pattern}' found in request body")
                            return True
            except Exception as e:
                logger.debug(f'Error checking request body: {str(e)}')
            return False
        return False