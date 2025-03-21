from __future__ import annotations
'Exception handlers for the application.\n\nThis module defines handlers for different types of exceptions that can occur\nin the application, mapping them to appropriate HTTP responses.\n'
import traceback
import datetime
from typing import Any, Dict, Optional
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from app.core.exceptions.base import AppException, ErrorCode, ErrorDetail, ErrorResponse, ErrorSeverity
from app.core.logging import get_logger
logger = get_logger('app.core.exceptions.handlers')
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    request_id = getattr(request.state, 'request_id', None)
    exc.log(request_id=request_id)
    error_response = exc.to_response(request_id=request_id)
    error_response.timestamp = datetime.datetime.now(datetime.UTC).isoformat()
    return JSONResponse(status_code=exc.status_code, content=jsonable_encoder(error_response), headers=exc.details.get('headers', {}) if isinstance(exc.details, dict) else {})
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    request_id = getattr(request.state, 'request_id', None)
    errors = []
    for error in exc.errors():
        errors.append(ErrorDetail(loc=list(map(str, error['loc'])), msg=error['msg'], type=error['type']))
    error_response = ErrorResponse(success=False, message='Validation error', code=ErrorCode.VALIDATION_ERROR, details=errors, meta={'request_id': request_id, 'severity': ErrorSeverity.WARNING}, timestamp=datetime.datetime.now(datetime.UTC).isoformat())
    logger.warning(f'Validation error: {len(errors)} validation errors', extra={'request_id': request_id, 'path': request.url.path, 'validation_errors': [{'loc': e.loc, 'msg': e.msg, 'type': e.type} for e in errors]})
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=jsonable_encoder(error_response))
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = getattr(request.state, 'request_id', None)
    logger.error(f'Unhandled exception: {str(exc)}', exc_info=exc, extra={'request_id': request_id, 'path': request.url.path})
    from app.core.config import settings, Environment
    error_message = 'An unexpected error occurred'
    error_details = None
    if settings.ENVIRONMENT != Environment.PRODUCTION:
        error_message = f'Unhandled error: {str(exc)}'
        error_details = [{'loc': ['server'], 'msg': str(exc), 'type': 'unhandled_error'}]
        if settings.ENVIRONMENT == Environment.DEVELOPMENT:
            trace = traceback.format_exception(type(exc), exc, exc.__traceback__)
            error_details[0]['traceback'] = trace
    error_response = ErrorResponse(success=False, message=error_message, code=ErrorCode.UNKNOWN_ERROR, details=error_details or [], meta={'request_id': request_id, 'severity': ErrorSeverity.ERROR}, timestamp=datetime.datetime.now(datetime.UTC).isoformat())
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(error_response))