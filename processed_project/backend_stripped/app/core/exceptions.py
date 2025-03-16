from __future__ import annotations
import traceback
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
class ErrorCode(str, Enum):
    UNKNOWN_ERROR = 'UNKNOWN_ERROR'
    VALIDATION_ERROR = 'VALIDATION_ERROR'
    PERMISSION_DENIED = 'PERMISSION_DENIED'
    RESOURCE_NOT_FOUND = 'RESOURCE_NOT_FOUND'
    RESOURCE_ALREADY_EXISTS = 'RESOURCE_ALREADY_EXISTS'
    BAD_REQUEST = 'BAD_REQUEST'
    AUTHENTICATION_FAILED = 'AUTHENTICATION_FAILED'
    TOKEN_EXPIRED = 'TOKEN_EXPIRED'
    INVALID_TOKEN = 'INVALID_TOKEN'
    USER_NOT_ACTIVE = 'USER_NOT_ACTIVE'
    DATABASE_ERROR = 'DATABASE_ERROR'
    TRANSACTION_FAILED = 'TRANSACTION_FAILED'
    DATA_INTEGRITY_ERROR = 'DATA_INTEGRITY_ERROR'
    EXTERNAL_SERVICE_ERROR = 'EXTERNAL_SERVICE_ERROR'
    RATE_LIMIT_EXCEEDED = 'RATE_LIMIT_EXCEEDED'
    SERVICE_UNAVAILABLE = 'SERVICE_UNAVAILABLE'
    BUSINESS_LOGIC_ERROR = 'BUSINESS_LOGIC_ERROR'
class ErrorDetail(BaseModel):
    loc: List[str] = Field(default_factory=list, description='Location of the error')
    msg: str = Field(description='Error message')
    type: str = Field(description='Error type')
class ErrorResponse(BaseModel):
    code: ErrorCode = Field(description='Error code')
    message: str = Field(description='Human-readable error message')
    details: Optional[List[ErrorDetail]] = Field(default=None, description='Detailed error information')
    request_id: Optional[str] = Field(default=None, description='Request ID for tracking')
class AppException(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    code: ErrorCode = ErrorCode.UNKNOWN_ERROR
    message: str = 'An unexpected error occurred'
    details: Optional[List[ErrorDetail]] = None
    def __init__(self, message: Optional[str]=None, code: Optional[ErrorCode]=None, details: Optional[List[ErrorDetail]]=None, status_code: Optional[int]=None) -> None:
        self.message = message or self.message
        self.code = code or self.code
        self.details = details or self.details
        if status_code is not None:
            self.status_code = status_code
        super().__init__(self.message)
    def to_response(self, request_id: Optional[str]=None) -> ErrorResponse:
        return ErrorResponse(code=self.code, message=self.message, details=self.details, request_id=request_id)
class ValidationException(AppException):
    status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY
    code: ErrorCode = ErrorCode.VALIDATION_ERROR
    message: str = 'Validation error'
class PermissionDeniedException(AppException):
    status_code: int = status.HTTP_403_FORBIDDEN
    code: ErrorCode = ErrorCode.PERMISSION_DENIED
    message: str = 'Permission denied'
class AuthenticationException(AppException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    code: ErrorCode = ErrorCode.AUTHENTICATION_FAILED
    message: str = 'Authentication failed'
class ResourceNotFoundException(AppException):
    status_code: int = status.HTTP_404_NOT_FOUND
    code: ErrorCode = ErrorCode.RESOURCE_NOT_FOUND
    message: str = 'Resource not found'
class ResourceAlreadyExistsException(AppException):
    status_code: int = status.HTTP_409_CONFLICT
    code: ErrorCode = ErrorCode.RESOURCE_ALREADY_EXISTS
    message: str = 'Resource already exists'
class BadRequestException(AppException):
    status_code: int = status.HTTP_400_BAD_REQUEST
    code: ErrorCode = ErrorCode.BAD_REQUEST
    message: str = 'Bad request'
class DatabaseException(AppException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    code: ErrorCode = ErrorCode.DATABASE_ERROR
    message: str = 'Database error'
class ExternalServiceException(AppException):
    status_code: int = status.HTTP_502_BAD_GATEWAY
    code: ErrorCode = ErrorCode.EXTERNAL_SERVICE_ERROR
    message: str = 'External service error'
class BusinessLogicException(AppException):
    status_code: int = status.HTTP_400_BAD_REQUEST
    code: ErrorCode = ErrorCode.BUSINESS_LOGIC_ERROR
    message: str = 'Business logic error'
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    from app.core.logging import get_logger
    logger = get_logger('app.exception')
    request_id = getattr(request.state, 'request_id', None)
    log_data = {'request_id': request_id, 'error_code': exc.code, 'status_code': exc.status_code, 'message': exc.message, 'path': request.url.path, 'method': request.method}
    if exc.status_code >= 500:
        logger.error(f'Application error: {exc.message}', extra=log_data)
        logger.debug(f'Traceback: {traceback.format_exc()}')
    else:
        logger.info(f'Client error: {exc.message}', extra=log_data)
    return JSONResponse(status_code=exc.status_code, content=exc.to_response(request_id=request_id).dict())
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    from app.core.logging import get_logger
    logger = get_logger('app.exception')
    request_id = getattr(request.state, 'request_id', None)
    details = []
    for error in exc.errors():
        details.append(ErrorDetail(loc=[str(loc) for loc in error['loc']], msg=error['msg'], type=error['type']))
    validation_exc = ValidationException(message='Validation error', details=details)
    log_data = {'request_id': request_id, 'error_code': validation_exc.code, 'status_code': validation_exc.status_code, 'path': request.url.path, 'method': request.method, 'details': [detail.dict() for detail in details]}
    logger.info(f'Validation error', extra=log_data)
    return JSONResponse(status_code=validation_exc.status_code, content=validation_exc.to_response(request_id=request_id).dict())
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    from app.core.logging import get_logger
    logger = get_logger('app.exception')
    request_id = getattr(request.state, 'request_id', None)
    code = ErrorCode.UNKNOWN_ERROR
    if exc.status_code == 401:
        code = ErrorCode.AUTHENTICATION_FAILED
    elif exc.status_code == 403:
        code = ErrorCode.PERMISSION_DENIED
    elif exc.status_code == 404:
        code = ErrorCode.RESOURCE_NOT_FOUND
    elif exc.status_code == 409:
        code = ErrorCode.RESOURCE_ALREADY_EXISTS
    elif exc.status_code == 422:
        code = ErrorCode.VALIDATION_ERROR
    elif 400 <= exc.status_code < 500:
        code = ErrorCode.BAD_REQUEST
    app_exc = AppException(message=str(exc.detail), code=code, status_code=exc.status_code)
    log_data = {'request_id': request_id, 'error_code': app_exc.code, 'status_code': app_exc.status_code, 'path': request.url.path, 'method': request.method}
    if exc.status_code >= 500:
        logger.error(f'Application error: {app_exc.message}', extra=log_data)
    else:
        logger.info(f'Client error: {app_exc.message}', extra=log_data)
    return JSONResponse(status_code=app_exc.status_code, content=app_exc.to_response(request_id=request_id).dict())
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    from app.core.logging import get_logger
    logger = get_logger('app.exception')
    request_id = getattr(request.state, 'request_id', None)
    app_exc = AppException(message='An unexpected error occurred', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    log_data = {'request_id': request_id, 'error_code': app_exc.code, 'status_code': app_exc.status_code, 'path': request.url.path, 'method': request.method, 'exception_type': exc.__class__.__name__, 'exception_message': str(exc)}
    logger.error(f'Unhandled exception: {str(exc)}', extra=log_data)
    logger.debug(f'Traceback: {traceback.format_exc()}')
    return JSONResponse(status_code=app_exc.status_code, content=app_exc.to_response(request_id=request_id).dict())