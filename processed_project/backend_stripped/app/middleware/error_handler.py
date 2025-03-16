from __future__ import annotations
import traceback
from typing import Callable, Optional
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.exceptions import AppException, ErrorCode, ErrorResponse
from app.core.logging import get_logger
class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)
        self.logger = get_logger('app.middleware.error_handler')
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        try:
            return await call_next(request)
        except Exception as exc:
            if isinstance(exc, AppException):
                raise
            request_id = getattr(request.state, 'request_id', None)
            self.logger.error(f'Unhandled exception in request: {str(exc)}', extra={'request_id': request_id, 'path': request.url.path, 'method': request.method, 'exception_type': exc.__class__.__name__, 'exception_message': str(exc)})
            self.logger.debug(f'Traceback: {traceback.format_exc()}')
            error_response = ErrorResponse(code=ErrorCode.UNKNOWN_ERROR, message='An unexpected error occurred', request_id=request_id)
            return JSONResponse(status_code=500, content=error_response.dict())