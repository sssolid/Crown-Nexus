from __future__ import annotations
import logging
import re
from typing import Callable, Optional, Pattern
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.core.logging import get_logger
logger = get_logger('app.middleware.security')
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, content_security_policy: Optional[str]=None, permissions_policy: Optional[str]=None, expect_ct: Optional[str]=None) -> None:
        super().__init__(app)
        self.content_security_policy: str = content_security_policy or settings.security.CONTENT_SECURITY_POLICY
        self.permissions_policy: str = permissions_policy or settings.security.PERMISSIONS_POLICY
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
            raise SecurityException(message='Forbidden - Suspicious request detected', code=ErrorCode.SECURITY_ERROR, details={'ip': request.client.host}, status_code=status.HTTP_403_FORBIDDEN)
        return await call_next(request)