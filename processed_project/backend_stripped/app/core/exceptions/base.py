from __future__ import annotations
'\nBase exception system for the application.\n\nThis module defines the core exception types, error codes, and response models\nused throughout the application. It provides a consistent foundation for error\nhandling and reporting.\n'
from app.logging import get_logger
import traceback
import logging
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator
from app.logging.context import get_logger
logger = get_logger('app.core.exceptions')
class ErrorCategory(str, Enum):
    VALIDATION = 'validation'
    AUTH = 'auth'
    RESOURCE = 'resource'
    SYSTEM = 'system'
    BUSINESS = 'business'
class ErrorCode(str, Enum):
    RESOURCE_NOT_FOUND = 'RESOURCE_NOT_FOUND'
    RESOURCE_ALREADY_EXISTS = 'RESOURCE_ALREADY_EXISTS'
    AUTHENTICATION_FAILED = 'AUTHENTICATION_FAILED'
    PERMISSION_DENIED = 'PERMISSION_DENIED'
    VALIDATION_ERROR = 'VALIDATION_ERROR'
    BAD_REQUEST = 'BAD_REQUEST'
    BUSINESS_LOGIC_ERROR = 'BUSINESS_LOGIC_ERROR'
    INVALID_STATE = 'INVALID_STATE'
    OPERATION_NOT_ALLOWED = 'OPERATION_NOT_ALLOWED'
    DATABASE_ERROR = 'DATABASE_ERROR'
    NETWORK_ERROR = 'NETWORK_ERROR'
    SERVICE_ERROR = 'SERVICE_ERROR'
    SERVER_ERROR = 'SERVER_ERROR'
    CONFIGURATION_ERROR = 'CONFIGURATION_ERROR'
    SECURITY_ERROR = 'SECURITY_ERROR'
    UNKNOWN_ERROR = 'UNKNOWN_ERROR'
class ErrorSeverity(str, Enum):
    WARNING = 'warning'
    ERROR = 'error'
    CRITICAL = 'critical'
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
    @field_validator('details', mode='before')
    @classmethod
    def validate_details(cls, v: Any) -> List[ErrorDetail]:
        if isinstance(v, dict) and 'errors' in v:
            return v['errors']
        elif isinstance(v, list):
            return v
        elif v is None:
            return []
        return [{'loc': ['unknown'], 'msg': str(v), 'type': 'unknown'}]
class AppException(Exception):
    def __init__(self, message: str, code: ErrorCode=ErrorCode.UNKNOWN_ERROR, details: Any=None, status_code: int=500, severity: ErrorSeverity=ErrorSeverity.ERROR, category: ErrorCategory=ErrorCategory.SYSTEM, original_exception: Optional[Exception]=None) -> None:
        self.message = message
        self.code = code
        self.details = details or {}
        self.status_code = status_code
        self.severity = severity
        self.category = category
        self.original_exception = original_exception
        if original_exception:
            if isinstance(self.details, dict):
                self.details['original_error'] = str(original_exception)
                self.details['traceback'] = traceback.format_exception(type(original_exception), original_exception, original_exception.__traceback__)
        super().__init__(self.message)
    def to_response(self, request_id: Optional[str]=None) -> ErrorResponse:
        error_details = []
        if isinstance(self.details, list):
            error_details = self.details
        elif isinstance(self.details, dict):
            if 'errors' in self.details:
                error_details = self.details['errors']
            else:
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
        log_level = logging.WARNING if self.severity == ErrorSeverity.WARNING else logging.ERROR
        context = {'status_code': self.status_code, 'error_code': str(self.code), 'error_category': self.category.value}
        if request_id:
            context['request_id'] = request_id
        if self.original_exception:
            logger.log(log_level, f'{self.message} (original error: {str(self.original_exception)})', exc_info=self.original_exception, **context)
        else:
            logger.log(log_level, self.message, **context)