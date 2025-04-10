from __future__ import annotations
'\nEnhanced error handler middleware for the application.\n\nThis middleware catches exceptions and routes them to the appropriate handlers,\nensuring consistent error responses across the application and preventing\ninfinite middleware loops.\n'
import time
import sys
import traceback
from typing import Callable, Any, Optional, Dict, Type
from fastapi import Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.error import handle_exception
from app.core.exceptions import AppException, ErrorCode, app_exception_handler, validation_exception_handler, generic_exception_handler
from app.logging.context import get_logger
from app.core.dependency_manager import get_service
from app.utils.circuit_breaker_utils import safe_increment_counter
logger = get_logger('app.middleware.error_handler')
ERROR_TYPE_MAPPING: Dict[Type[Exception], ErrorCode] = {RequestValidationError: ErrorCode.VALIDATION_ERROR, ValueError: ErrorCode.VALIDATION_ERROR, TypeError: ErrorCode.VALIDATION_ERROR}
class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: Any) -> None:
        super().__init__(app)
        logger.info('ErrorHandlerMiddleware initialized')
    def _get_metrics_service(self) -> Optional[Any]:
        try:
            return get_service('metrics_service')
        except Exception:
            return None
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        start_time = time.time()
        error_type = None
        status_code = None
        if hasattr(request.state, '_error_handler_active'):
            logger.error('Detected recursive error handling - bypassing error handler')
            try:
                return JSONResponse(status_code=500, content={'success': False, 'message': 'Internal Server Error', 'error': {'code': 'RECURSIVE_ERROR', 'details': 'Error occurred during error handling'}})
            except Exception:
                return Response(content='Internal Server Error', status_code=500, media_type='text/plain')
        setattr(request.state, '_error_handler_active', True)
        try:
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
                self._track_error_metrics(error_type, status_code, request.method, request.url.path)
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
                self._track_error_metrics(error_type, status_code, request.method, request.url.path)
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
                exc_info = sys.exc_info()
                tb_str = ''.join(traceback.format_exception(*exc_info))
                logger.exception(f'Unhandled exception: {str(exc)}', exc_info=exc, traceback=tb_str, request_id=request_id, path=path, method=method, error_code=error_code.value, status_code=status_code, execution_time=f'{execution_time:.4f}s')
                handle_exception(exc, request_id=request_id, user_id=user_id, function_name=method)
                self._track_error_metrics(error_type, status_code, request.method, request.url.path)
                return await generic_exception_handler(request, exc)
        except Exception as nested_exc:
            logger.critical(f'Exception occurred during error handling: {str(nested_exc)}', exc_info=nested_exc)
            return JSONResponse(status_code=500, content={'success': False, 'message': 'Internal Server Error', 'error': {'code': 'ERROR_HANDLER_FAILURE', 'details': 'An error occurred during error handling'}})
        finally:
            if hasattr(request.state, '_error_handler_active'):
                delattr(request.state, '_error_handler_active')
    def _track_error_metrics(self, error_type: str, status_code: int, method: str, path: str) -> None:
        metrics_service = self._get_metrics_service()
        if not metrics_service:
            return
        try:
            safe_increment_counter('http_errors_total', 1, {'error_type': error_type, 'status_code': str(status_code), 'method': method, 'endpoint': path})
        except Exception as e:
            logger.debug(f'Failed to track error metrics: {e}')