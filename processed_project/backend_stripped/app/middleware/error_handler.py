from __future__ import annotations
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.error import handle_exception
from app.core.exceptions import AppException, app_exception_handler, generic_exception_handler
from app.core.logging import get_logger
logger = get_logger('app.middleware.error_handler')
class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            return await call_next(request)
        except AppException as exc:
            handle_exception(exc, request.headers.get('X-Request-ID'))
            return await app_exception_handler(request, exc)
        except Exception as exc:
            handle_exception(exc, request.headers.get('X-Request-ID'))
            return await generic_exception_handler(request, exc)