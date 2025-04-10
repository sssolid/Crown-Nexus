from __future__ import annotations
from app.core.metrics import MetricName
from app.utils.circuit_breaker_utils import safe_observe_histogram, safe_increment_counter
'\nSecurity middleware for the application.\n\nThis module provides middleware for adding security headers and\nblocking suspicious requests.\n'
import re
import time
from typing import Callable, Dict, List, Optional, Any, Pattern
from fastapi import FastAPI, Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.core.exceptions import SecurityException, ErrorCode
from app.logging.context import get_logger
from app.core.dependency_manager import get_service
logger = get_logger('app.middleware.security')
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, content_security_policy: Optional[str]=None, permissions_policy: Optional[str]=None, expect_ct: Optional[str]=None, hsts_max_age: int=31536000, include_subdomains: bool=True, preload: bool=False, exclude_paths: Optional[List[str]]=None) -> None:
        super().__init__(app)
        self.content_security_policy: str = content_security_policy or settings.CONTENT_SECURITY_POLICY
        self.permissions_policy: str = permissions_policy or settings.PERMISSIONS_POLICY
        self.expect_ct: Optional[str] = expect_ct
        self.exclude_paths = exclude_paths or []
        hsts_value = f'max-age={hsts_max_age}'
        if include_subdomains:
            hsts_value += '; includeSubDomains'
        if preload:
            hsts_value += '; preload'
        self.hsts_value = hsts_value
        logger.info('SecurityHeadersMiddleware initialized', hsts_max_age=hsts_max_age, include_subdomains=include_subdomains, preload=preload)
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        metrics_service: Optional[Any] = None
        try:
            metrics_service = get_service('metrics_service')
        except Exception:
            pass
        path = request.url.path
        if any((path.startswith(exc) for exc in self.exclude_paths)):
            return await call_next(request)
        start_time = time.time()
        try:
            response: Response = await call_next(request)
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'DENY'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            response.headers['Content-Security-Policy'] = self.content_security_policy
            response.headers['Strict-Transport-Security'] = self.hsts_value
            response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
            if self.permissions_policy:
                response.headers['Permissions-Policy'] = self.permissions_policy
            if self.expect_ct:
                response.headers['Expect-CT'] = self.expect_ct
            response.headers['X-Security-Headers-Added'] = str(int(time.time()))
            return response
        except Exception as e:
            logger.exception(f'Error in SecurityHeadersMiddleware: {str(e)}', exc_info=e)
            raise
        finally:
            if metrics_service:
                try:
                    duration = time.time() - start_time
                    safe_observe_histogram(MetricName.SECURITY_HEADERS_DURATION_SECONDS.value, duration, {'path': path})
                except Exception as e:
                    logger.debug(f'Failed to track security headers metrics: {e}')
class SecureRequestMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, block_suspicious_requests: bool=True, suspicious_patterns: Optional[List[str]]=None, suspicious_regex_patterns: Optional[List[str]]=None, exclude_paths: Optional[List[str]]=None) -> None:
        super().__init__(app)
        self.block_suspicious_requests: bool = block_suspicious_requests
        self.suspicious_patterns: List[str] = suspicious_patterns or ['../../', '<script', 'eval(', 'document.cookie', 'onload=', 'javascript:', 'onerror=', 'SELECT ', 'UNION ', 'DROP ', 'OR 1=1', 'alert(']
        regex_patterns = suspicious_regex_patterns or ['(?i)(union[\\s\\(\\+]+select)', '(?i)(select.+from)', '(?i)(/\\*!|\\*/(?!\\*))', '(?i)(script.*>)', '(?i)(alert\\s*\\(.*\\))']
        self.regex_patterns: List[Pattern[str]] = [re.compile(pattern) for pattern in regex_patterns]
        self.exclude_paths = exclude_paths or ['/', '/docs', '/redoc', '/openapi.json', '/static/', '/media/']
        logger.info('SecureRequestMiddleware initialized', block_suspicious=block_suspicious_requests, patterns_count=len(self.suspicious_patterns), regex_count=len(self.regex_patterns))
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        metrics_service: Optional[Any] = None
        try:
            metrics_service = get_service('metrics_service')
        except Exception:
            pass
        path = request.url.path
        if any((path.startswith(exc) for exc in self.exclude_paths)):
            return await call_next(request)
        start_time = time.time()
        suspicious = False
        suspicious_pattern = None
        try:
            if self.block_suspicious_requests:
                suspicious, suspicious_pattern = await self._is_suspicious_request(request)
                if suspicious:
                    client_ip = getattr(request.client, 'host', 'unknown') if request.client else 'unknown'
                    logger.warning(f'Blocked suspicious request', ip=client_ip, path=path, method=request.method, pattern=suspicious_pattern)
                    if metrics_service:
                        try:
                            safe_increment_counter('blocked_suspicious_requests_total', 1, {'endpoint': path, 'method': request.method, 'pattern_type': 'regex' if isinstance(suspicious_pattern, re.Pattern) else 'string'})
                        except Exception as e:
                            logger.debug(f'Failed to track security metrics: {e}')
                    raise SecurityException(message='Forbidden - Suspicious request detected', details={'ip': client_ip, 'path': path}, status_code=status.HTTP_403_FORBIDDEN)
            return await call_next(request)
        finally:
            if metrics_service:
                try:
                    duration = time.time() - start_time
                    safe_observe_histogram(MetricName.REQUEST_SECURITY_CHECK_DURATION_SECONDS.value, duration, {'suspicious': str(suspicious), 'path': path})
                except Exception as e:
                    logger.debug(f'Failed to track security check metrics: {e}')
    async def _is_suspicious_request(self, request: Request) -> tuple[bool, Optional[Any]]:
        path = request.url.path
        for pattern in self.suspicious_patterns:
            if pattern.lower() in path.lower():
                logger.warning(f'Suspicious pattern detected in path', pattern=pattern, path=path)
                return (True, pattern)
        query_string = str(request.url.query)
        for pattern in self.suspicious_patterns:
            if pattern.lower() in query_string.lower():
                logger.warning(f'Suspicious pattern detected in query', pattern=pattern, query=query_string)
                return (True, pattern)
        combined = f'{path}?{query_string}'
        for regex in self.regex_patterns:
            if regex.search(combined):
                logger.warning(f'Suspicious regex pattern detected', pattern=regex.pattern, path=path, query=query_string)
                return (True, regex)
        for header_name, header_value in request.headers.items():
            for pattern in self.suspicious_patterns:
                if pattern.lower() in header_value.lower():
                    logger.warning(f'Suspicious pattern detected in header', pattern=pattern, header_name=header_name)
                    return (True, pattern)
            for regex in self.regex_patterns:
                if regex.search(header_value):
                    logger.warning(f'Suspicious regex pattern detected in header', pattern=regex.pattern, header_name=header_name)
                    return (True, regex)
        return (False, None)