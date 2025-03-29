from __future__ import annotations
'\nError handler middleware for the application.\n\nThis middleware catches exceptions and routes them to the appropriate handlers,\nensuring consistent error responses across the application.\n'
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.error import handle_exception
from app.core.exceptions import AppException, app_exception_handler, generic_exception_handler
from app.logging.context import get_logger
logger = get_logger('app.middleware.error_handler')
class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            return await call_next(request)
        except AppException as exc:
            request_id = getattr(request.state, 'request_id', None)
            handle_exception(exc, request_id)
            return await app_exception_handler(request, exc)
        except Exception as exc:
            request_id = getattr(request.state, 'request_id', None)
            logger.exception(f'Unhandled exception: {str(exc)}', exc_info=exc, request_id=request_id, path=request.url.path)
            handle_exception(exc, request_id)
            return await generic_exception_handler(request, exc)