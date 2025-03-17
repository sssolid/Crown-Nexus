from __future__ import annotations
import logging
import sys
import traceback
from enum import Enum
from typing import Any, Dict, List, Optional, Type, Union, cast
from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from app.core.logging import get_logger
logger = get_logger('app.core.exceptions')
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
    NETWORK_ERROR = 'NETWORK_ERROR'
    TIMEOUT_ERROR = 'TIMEOUT_ERROR'
    CONNECTION_ERROR = 'CONNECTION_ERROR'
    EXTERNAL_SERVICE_ERROR = 'EXTERNAL_SERVICE_ERROR'
    RATE_LIMIT_EXCEEDED = 'RATE_LIMIT_EXCEEDED'
    SERVICE_UNAVAILABLE = 'SERVICE_UNAVAILABLE'
    EXTERNAL_DEPENDENCY_ERROR = 'EXTERNAL_DEPENDENCY_ERROR'
    BUSINESS_LOGIC_ERROR = 'BUSINESS_LOGIC_ERROR'
    INVALID_STATE_ERROR = 'INVALID_STATE_ERROR'
    OPERATION_NOT_ALLOWED = 'OPERATION_NOT_ALLOWED'
    SECURITY_ERROR = 'SECURITY_ERROR'
    ACCESS_DENIED = 'ACCESS_DENIED'
    CSRF_ERROR = 'CSRF_ERROR'
    DATA_ERROR = 'DATA_ERROR'
    SERIALIZATION_ERROR = 'SERIALIZATION_ERROR'
    DESERIALIZATION_ERROR = 'DESERIALIZATION_ERROR'
    SYSTEM_ERROR = 'SYSTEM_ERROR'
    CONFIGURATION_ERROR = 'CONFIGURATION_ERROR'
    DEPENDENCY_ERROR = 'DEPENDENCY_ERROR'
class ErrorSeverity(str, Enum):
    DEBUG = 'debug'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    CRITICAL = 'critical'
class ErrorCategory(str, Enum):
    VALIDATION = 'validation'
    AUTHENTICATION = 'authentication'
    AUTHORIZATION = 'authorization'
    RESOURCE = 'resource'
    DATABASE = 'database'
    NETWORK = 'network'
    EXTERNAL = 'external'
    BUSINESS = 'business'
    SECURITY = 'security'
    DATA = 'data'
    SYSTEM = 'system'
    UNKNOWN = 'unknown'
class ErrorDetail(BaseModel):
    loc: List[str] = Field(..., description='Error location (path to the error)')
    msg: str = Field(..., description='Error message')
    type: str = Field(..., description='Error type code')
class ErrorResponse(BaseModel):
    success: bool = Field(False, description='Success flag (always False for errors)')
    message: str = Field(..., description='Human-readable error message')
    code: str = Field(..., description='Error code')
    data: Optional[Any] = Field(None, description='Additional error data')
    details: List[ErrorDetail] = Field([], description='Detailed error information')
    meta: Dict[str, Any] = Field(default_factory=dict, description='Metadata')
    timestamp: Optional[str] = Field(None, description='Error timestamp')
    @validator('details', pre=True)
    def validate_details(cls, v: Any) -> List[ErrorDetail]:
        if isinstance(v, dict) and 'errors' in v:
            return v['errors']
        elif isinstance(v, list):
            return v
        elif v is None:
            return []
        return [{'loc': ['unknown'], 'msg': str(v), 'type': 'unknown'}]
class AppException(Exception):
    def __init__(self, message: str, code: Union[str, ErrorCode]=ErrorCode.UNKNOWN_ERROR, details: Optional[Dict[str, Any]]=None, status_code: int=status.HTTP_500_INTERNAL_SERVER_ERROR, severity: ErrorSeverity=ErrorSeverity.ERROR, category: ErrorCategory=ErrorCategory.UNKNOWN, original_exception: Optional[Exception]=None) -> None:
        self.message = message
        self.code = code
        self.details = details or {}
        self.status_code = status_code
        self.severity = severity
        self.category = category
        self.original_exception = original_exception
        if original_exception:
            self.details['original_error'] = str(original_exception)
            self.details['traceback'] = traceback.format_exception(type(original_exception), original_exception, original_exception.__traceback__)
        super().__init__(self.message)
    def to_response(self, request_id: Optional[str]=None) -> ErrorResponse:
        error_details = []
        if 'errors' in self.details:
            error_details = self.details['errors']
        elif self.details:
            for key, value in self.details.items():
                if key not in ['original_error', 'traceback']:
                    error_details.append({'loc': key.split('.'), 'msg': str(value), 'type': str(self.code).lower()})
        else:
            error_details = [{'loc': ['server'], 'msg': self.message, 'type': str(self.code).lower()}]
        meta = {'request_id': request_id} if request_id else {}
        meta['severity'] = self.severity
        meta['category'] = self.category
        return ErrorResponse(success=False, message=self.message, code=str(self.code), data=None, details=error_details, meta=meta, timestamp=None)
    def log(self, request_id: Optional[str]=None) -> None:
        log_method = getattr(logger, self.severity.value, logger.error)
        context = {'status_code': self.status_code, 'error_code': str(self.code), 'error_category': self.category.value}
        if request_id:
            context['request_id'] = request_id
        if self.original_exception:
            log_method(f'{self.message} (original error: {str(self.original_exception)})', exc_info=self.original_exception, **context)
        else:
            log_method(self.message, **context)
class ValidationException(AppException):
    def __init__(self, message: str, code: Union[str, ErrorCode]=ErrorCode.VALIDATION_ERROR, details: Optional[Dict[str, Any]]=None, status_code: int=status.HTTP_400_BAD_REQUEST, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.WARNING, category=ErrorCategory.VALIDATION, original_exception=original_exception)
class ResourceNotFoundException(AppException):
    def __init__(self, message: str, code: Union[str, ErrorCode]=ErrorCode.RESOURCE_NOT_FOUND, details: Optional[Dict[str, Any]]=None, status_code: int=status.HTTP_404_NOT_FOUND, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.WARNING, category=ErrorCategory.RESOURCE, original_exception=original_exception)
class ResourceAlreadyExistsException(AppException):
    def __init__(self, message: str, code: Union[str, ErrorCode]=ErrorCode.RESOURCE_ALREADY_EXISTS, details: Optional[Dict[str, Any]]=None, status_code: int=status.HTTP_409_CONFLICT, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.WARNING, category=ErrorCategory.RESOURCE, original_exception=original_exception)
class BadRequestException(AppException):
    def __init__(self, message: str, code: Union[str, ErrorCode]=ErrorCode.BAD_REQUEST, details: Optional[Dict[str, Any]]=None, status_code: int=status.HTTP_400_BAD_REQUEST, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.WARNING, category=ErrorCategory.VALIDATION, original_exception=original_exception)
class AuthenticationException(AppException):
    def __init__(self, message: str, code: Union[str, ErrorCode]=ErrorCode.AUTHENTICATION_FAILED, details: Optional[Dict[str, Any]]=None, status_code: int=status.HTTP_401_UNAUTHORIZED, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.WARNING, category=ErrorCategory.AUTHENTICATION, original_exception=original_exception)
class PermissionDeniedException(AppException):
    def __init__(self, message: str, code: Union[str, ErrorCode]=ErrorCode.PERMISSION_DENIED, details: Optional[Dict[str, Any]]=None, status_code: int=status.HTTP_403_FORBIDDEN, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.WARNING, category=ErrorCategory.AUTHORIZATION, original_exception=original_exception)
class DatabaseException(AppException):
    def __init__(self, message: str, code: Union[str, ErrorCode]=ErrorCode.DATABASE_ERROR, details: Optional[Dict[str, Any]]=None, status_code: int=status.HTTP_500_INTERNAL_SERVER_ERROR, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.ERROR, category=ErrorCategory.DATABASE, original_exception=original_exception)
class DataIntegrityException(DatabaseException):
    def __init__(self, message: str, code: Union[str, ErrorCode]=ErrorCode.DATA_INTEGRITY_ERROR, details: Optional[Dict[str, Any]]=None, status_code: int=status.HTTP_409_CONFLICT, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.ERROR, category=ErrorCategory.DATABASE, original_exception=original_exception)
class TransactionException(DatabaseException):
    def __init__(self, message: str, code: Union[str, ErrorCode]=ErrorCode.TRANSACTION_FAILED, details: Optional[Dict[str, Any]]=None, status_code: int=status.HTTP_500_INTERNAL_SERVER_ERROR, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.ERROR, category=ErrorCategory.DATABASE, original_exception=original_exception)
class NetworkException(AppException):
    def __init__(self, message: str, code: Union[str, ErrorCode]=ErrorCode.NETWORK_ERROR, details: Optional[Dict[str, Any]]=None, status_code: int=status.HTTP_503_SERVICE_UNAVAILABLE, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.ERROR, category=ErrorCategory.NETWORK, original_exception=original_exception)
class TimeoutException(NetworkException):
    def __init__(self, message: str, code: Union[str, ErrorCode]=ErrorCode.TIMEOUT_ERROR, details: Optional[Dict[str, Any]]=None, status_code: int=status.HTTP_504_GATEWAY_TIMEOUT, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.ERROR, category=ErrorCategory.NETWORK, original_exception=original_exception)
class ExternalServiceException(AppException):
    def __init__(self, message: str, code: Union[str, ErrorCode]=ErrorCode.EXTERNAL_SERVICE_ERROR, details: Optional[Dict[str, Any]]=None, status_code: int=status.HTTP_502_BAD_GATEWAY, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.ERROR, category=ErrorCategory.EXTERNAL, original_exception=original_exception)
class RateLimitException(ExternalServiceException):
    def __init__(self, message: str, code: Union[str, ErrorCode]=ErrorCode.RATE_LIMIT_EXCEEDED, details: Optional[Dict[str, Any]]=None, status_code: int=status.HTTP_429_TOO_MANY_REQUESTS, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.WARNING, category=ErrorCategory.EXTERNAL, original_exception=original_exception)
class ServiceUnavailableException(ExternalServiceException):
    def __init__(self, message: str, code: Union[str, ErrorCode]=ErrorCode.SERVICE_UNAVAILABLE, details: Optional[Dict[str, Any]]=None, status_code: int=status.HTTP_503_SERVICE_UNAVAILABLE, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.ERROR, category=ErrorCategory.EXTERNAL, original_exception=original_exception)
class BusinessLogicException(AppException):
    def __init__(self, message: str, code: Union[str, ErrorCode]=ErrorCode.BUSINESS_LOGIC_ERROR, details: Optional[Dict[str, Any]]=None, status_code: int=status.HTTP_400_BAD_REQUEST, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.WARNING, category=ErrorCategory.BUSINESS, original_exception=original_exception)
class InvalidStateException(BusinessLogicException):
    def __init__(self, message: str, code: Union[str, ErrorCode]=ErrorCode.INVALID_STATE_ERROR, details: Optional[Dict[str, Any]]=None, status_code: int=status.HTTP_409_CONFLICT, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.WARNING, category=ErrorCategory.BUSINESS, original_exception=original_exception)
class OperationNotAllowedException(BusinessLogicException):
    def __init__(self, message: str, code: Union[str, ErrorCode]=ErrorCode.OPERATION_NOT_ALLOWED, details: Optional[Dict[str, Any]]=None, status_code: int=status.HTTP_403_FORBIDDEN, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.WARNING, category=ErrorCategory.BUSINESS, original_exception=original_exception)
class ConfigurationException(AppException):
    def __init__(self, message: str, code: Union[str, ErrorCode]=ErrorCode.CONFIGURATION_ERROR, details: Optional[Dict[str, Any]]=None, status_code: int=status.HTTP_500_INTERNAL_SERVER_ERROR, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.ERROR, category=ErrorCategory.SYSTEM, original_exception=original_exception)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    exc.log(getattr(request.state, 'request_id', None))
    error_response = exc.to_response(getattr(request.state, 'request_id', None))
    return JSONResponse(status_code=exc.status_code, content=error_response.dict())
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.warning(f'Validation error: {str(exc)}', exc_info=exc, request_id=getattr(request.state, 'request_id', None))
    error_details = []
    for error in exc.errors():
        error_details.append({'loc': list(error['loc']), 'msg': error['msg'], 'type': error['type']})
    error_response = ErrorResponse(success=False, message='Validation error', code=ErrorCode.VALIDATION_ERROR, data=None, details=error_details, meta={'request_id': getattr(request.state, 'request_id', None)}, timestamp=None)
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=error_response.dict())
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    logger.warning(f'HTTP exception: {exc.detail}', exc_info=exc, request_id=getattr(request.state, 'request_id', None), status_code=exc.status_code)
    error_code = None
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        error_code = ErrorCode.RESOURCE_NOT_FOUND
    elif exc.status_code == status.HTTP_401_UNAUTHORIZED:
        error_code = ErrorCode.AUTHENTICATION_FAILED
    elif exc.status_code == status.HTTP_403_FORBIDDEN:
        error_code = ErrorCode.PERMISSION_DENIED
    elif exc.status_code == status.HTTP_409_CONFLICT:
        error_code = ErrorCode.RESOURCE_ALREADY_EXISTS
    else:
        error_code = ErrorCode.UNKNOWN_ERROR
    error_response = ErrorResponse(success=False, message=str(exc.detail), code=error_code, data=None, details=[{'loc': ['server'], 'msg': str(exc.detail), 'type': error_code.lower()}], meta={'request_id': getattr(request.state, 'request_id', None)}, timestamp=None)
    return JSONResponse(status_code=exc.status_code, content=error_response.dict(), headers=exc.headers)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f'Unhandled exception: {str(exc)}', exc_info=exc, request_id=getattr(request.state, 'request_id', None))
    error_response = ErrorResponse(success=False, message='An unexpected error occurred', code=ErrorCode.UNKNOWN_ERROR, data=None, details=[{'loc': ['server'], 'msg': str(exc), 'type': 'unknown_error'}], meta={'request_id': getattr(request.state, 'request_id', None)}, timestamp=None)
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error_response.dict())