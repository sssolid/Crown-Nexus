from __future__ import annotations
'\nSecurity middleware for the application.\n\nThis module provides middleware for adding security headers and\nblocking suspicious requests.\n'
from typing import Callable, Optional
from fastapi import FastAPI, Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.core.exceptions import SecurityException
from app.logging.context import get_logger
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
            logger.exception(f'Error in SecurityHeadersMiddleware: {str(e)}', exc_info=e)
            raise
class SecureRequestMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, block_suspicious_requests: bool=True) -> None:
        super().__init__(app)
        self.block_suspicious_requests: bool = block_suspicious_requests
        self.suspicious_patterns: list[str] = ['../../', '<script', 'eval(', 'SELECT ']
        logger.info('SecureRequestMiddleware initialized')
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        if self.block_suspicious_requests and self._is_suspicious_request(request):
            client_ip = request.client.host if request.client else 'unknown'
            logger.warning(f'Blocked suspicious request', ip=client_ip, path=request.url.path, method=request.method)
            raise SecurityException(message='Forbidden - Suspicious request detected', details={'ip': client_ip}, status_code=status.HTTP_403_FORBIDDEN)
        return await call_next(request)
    def _is_suspicious_request(self, request: Request) -> bool:
        path = request.url.path
        for pattern in self.suspicious_patterns:
            if pattern.lower() in path.lower():
                logger.warning(f'Suspicious pattern detected in path', pattern=pattern, path=path)
                return True
        query_string = str(request.url.query)
        for pattern in self.suspicious_patterns:
            if pattern.lower() in query_string.lower():
                logger.warning(f'Suspicious pattern detected in query', pattern=pattern, query=query_string)
                return True
        for header_name, header_value in request.headers.items():
            for pattern in self.suspicious_patterns:
                if pattern.lower() in header_value.lower():
                    logger.warning(f'Suspicious pattern detected in header', pattern=pattern, header_name=header_name)
                    return True
        return False