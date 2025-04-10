from __future__ import annotations
'\nTimeout middleware for the application.\n\nThis middleware sets a maximum execution time for requests to prevent\nlong-running requests from consuming resources.\n'
import asyncio
import time
from typing import Callable, Optional, Any, Dict
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette import status
from app.core.exceptions import AppException, ErrorCode
from app.logging import get_logger
from app.core.dependency_manager import get_service
from app.utils.circuit_breaker_utils import safe_observe_histogram, safe_increment_counter
logger = get_logger('app.middleware.timeout')
class TimeoutException(AppException):
    def __init__(self, message: str, details: Optional[dict[str, Any]]=None, status_code: int=status.HTTP_504_GATEWAY_TIMEOUT, code: ErrorCode=ErrorCode.SERVER_ERROR) -> None:
        super().__init__(message, details, status_code, code)
class TimeoutMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: Any, timeout_seconds: float=30.0, exclude_paths: Optional[list[str]]=None) -> None:
        super().__init__(app)
        self.timeout_seconds = timeout_seconds
        self.exclude_paths = exclude_paths or ['/docs', '/redoc', '/openapi.json']
        logger.info('TimeoutMiddleware initialized', timeout_seconds=timeout_seconds)
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        path = request.url.path
        if any((path.startswith(exc) for exc in self.exclude_paths)):
            return await call_next(request)
        metrics_service = None
        try:
            metrics_service = get_service('metrics_service')
        except Exception:
            pass
        start_time = time.monotonic()
        timed_out = False
        try:
            return await asyncio.wait_for(call_next(request), timeout=self.timeout_seconds)
        except asyncio.TimeoutError:
            timed_out = True
            client_ip = getattr(request.client, 'host', 'unknown') if request.client else 'unknown'
            logger.warning('Request timed out', path=path, method=request.method, client=client_ip, timeout_seconds=self.timeout_seconds)
            if metrics_service:
                try:
                    safe_increment_counter('request_timeouts_total', 1, {'endpoint': path, 'method': request.method})
                except Exception as e:
                    logger.debug(f'Failed to track timeout metrics: {str(e)}')
            error_message = f'Request timed out after {self.timeout_seconds} seconds'
            error_details = {'endpoint': path, 'method': request.method, 'timeout_seconds': self.timeout_seconds}
            return JSONResponse(status_code=status.HTTP_504_GATEWAY_TIMEOUT, content={'success': False, 'message': error_message, 'error': {'code': ErrorCode.SERVER_ERROR.value, 'details': error_details}, 'timestamp': time.time()})
        finally:
            if metrics_service and (not timed_out):
                try:
                    duration = time.monotonic() - start_time
                    safe_observe_histogram('request_duration_seconds', duration, {'endpoint': path, 'method': request.method})
                except Exception as e:
                    logger.debug(f'Failed to track duration metrics: {str(e)}')