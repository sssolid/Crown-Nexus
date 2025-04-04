from __future__ import annotations
from app.utils.circuit_breaker_utils import safe_increment_counter
'\nError handler middleware for the application.\n\nThis middleware catches exceptions and routes them to the appropriate handlers,\nensuring consistent error responses across the application.\n'
import time
from typing import Callable, Any, Optional, Dict, Type
from fastapi import Request, Response, status
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.core.error import handle_exception
from app.core.exceptions import AppException, ErrorCode, app_exception_handler, validation_exception_handler, generic_exception_handler
from app.logging.context import get_logger
from app.core.dependency_manager import get_service
logger = get_logger('app.middleware.error_handler')
ERROR_TYPE_MAPPING: Dict[Type[Exception], ErrorCode] = {RequestValidationError: ErrorCode.VALIDATION_ERROR, ValueError: ErrorCode.VALIDATION_ERROR, TypeError: ErrorCode.VALIDATION_ERROR}
class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: Any) -> None:
        super().__init__(app)
        logger.info('ErrorHandlerMiddleware initialized')
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        metrics_service: Optional[Any] = None
        try:
            metrics_service = get_service('metrics_service')
        except Exception:
            pass
        start_time = time.time()
        error_type = None
        status_code = None
        try:
            return await call_next(request)
        except AppException as exc:
            execution_time = time.time() - start_time
            request_id = getattr(request.state, 'request_id', None)
            user_id = getattr(request.state, 'user_id', None)
            path = request.url.path
            method = request.method
            error_type = type(exc).__name__
            status_code = exc.status_code
            logger.warning(f'Application exception: {str(exc)}', exc_info=exc, request_id=request_id, path=path, method=method, error_code=exc.code.value if hasattr(exc, 'code') else None, status_code=exc.status_code, details=exc.details, execution_time=f'{execution_time:.4f}s')
            handle_exception(exc, request_id=request_id, user_id=user_id, function_name=method)
            self._track_error_metrics(metrics_service, error_type, status_code, request.method, request.url.path)
            return await app_exception_handler(request, exc)
        except RequestValidationError as exc:
            execution_time = time.time() - start_time
            request_id = getattr(request.state, 'request_id', None)
            user_id = getattr(request.state, 'user_id', None)
            path = request.url.path
            method = request.method
            error_type = type(exc).__name__
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            logger.warning(f'Validation error: {str(exc)}', exc_info=exc, request_id=request_id, path=path, method=method, error_code=ErrorCode.VALIDATION_ERROR.value, status_code=status_code, errors=str(exc.errors()) if hasattr(exc, 'errors') else None, execution_time=f'{execution_time:.4f}s')
            handle_exception(exc, request_id=request_id, user_id=user_id, function_name=method)
            self._track_error_metrics(metrics_service, error_type, status_code, request.method, request.url.path)
            return await validation_exception_handler(request, exc)
        except Exception as exc:
            execution_time = time.time() - start_time
            request_id = getattr(request.state, 'request_id', None)
            user_id = getattr(request.state, 'user_id', None)
            path = request.url.path
            method = request.method
            error_type = type(exc).__name__
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            error_code = ERROR_TYPE_MAPPING.get(type(exc), ErrorCode.SERVER_ERROR)
            logger.exception(f'Unhandled exception: {str(exc)}', exc_info=exc, request_id=request_id, path=path, method=method, error_code=error_code.value, status_code=status_code, execution_time=f'{execution_time:.4f}s')
            handle_exception(exc, request_id=request_id, user_id=user_id, function_name=method)
            self._track_error_metrics(metrics_service, error_type, status_code, request.method, request.url.path)
            return await generic_exception_handler(request, exc)
    def _track_error_metrics(self, metrics_service: Optional[Any], error_type: str, status_code: int, method: str, path: str) -> None:
        if not metrics_service:
            return
        try:
            safe_increment_counter('http_errors_total', 1, {'error_type': error_type, 'status_code': str(status_code), 'method': method, 'endpoint': path})
        except Exception as e:
            logger.debug(f'Failed to track error metrics: {e}')