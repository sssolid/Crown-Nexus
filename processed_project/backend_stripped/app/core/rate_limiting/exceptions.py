from __future__ import annotations
"\nRate limiting system exceptions.\n\nThis module defines exceptions specific to the rate limiting system,\naligned with the application's exception hierarchy.\n"
from typing import Any, Dict, List, Optional, Union
from app.core.exceptions.base import AppException, ErrorCategory, ErrorCode, ErrorSeverity
class RateLimitingException(AppException):
    def __init__(self, message: str, code: ErrorCode=ErrorCode.SECURITY_ERROR, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, status_code: int=429, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.WARNING, category=ErrorCategory.SYSTEM, original_exception=original_exception)
class RateLimitExceededException(RateLimitingException):
    def __init__(self, message: str='Rate limit exceeded', details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, headers: Optional[Dict[str, str]]=None, reset_seconds: Optional[int]=None, original_exception: Optional[Exception]=None) -> None:
        error_details = details or {}
        if isinstance(error_details, dict):
            error_details['headers'] = headers or {}
            if reset_seconds:
                error_details['reset_seconds'] = reset_seconds
        super().__init__(message=message, details=error_details, status_code=429, original_exception=original_exception)
class RateLimitingServiceException(RateLimitingException):
    def __init__(self, message: str, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=ErrorCode.SERVICE_ERROR, details=details, status_code=500, original_exception=original_exception)
class RateLimitingConfigurationException(RateLimitingException):
    def __init__(self, message: str, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=ErrorCode.CONFIGURATION_ERROR, details=details, status_code=500, original_exception=original_exception)