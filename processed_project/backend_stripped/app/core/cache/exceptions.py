from __future__ import annotations
"\nCache-specific exceptions for the application.\n\nThis module defines exceptions related to cache operations that integrate\nwith the application's exception system.\n"
from typing import Any, Dict, List, Optional, Union
from app.core.exceptions.base import AppException, ErrorCategory, ErrorCode, ErrorSeverity
class CacheException(AppException):
    def __init__(self, message: str, code: ErrorCode=ErrorCode.UNKNOWN_ERROR, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, status_code: int=500, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.WARNING, category=ErrorCategory.SYSTEM, original_exception=original_exception)
class CacheConnectionException(CacheException):
    def __init__(self, message: str, backend: str, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        error_details = details or {}
        if isinstance(error_details, dict):
            error_details['backend'] = backend
        super().__init__(message=message, code=ErrorCode.SERVICE_ERROR, details=error_details, status_code=500, original_exception=original_exception)
class CacheOperationException(CacheException):
    def __init__(self, message: str, operation: str, key: Optional[str]=None, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        error_details = details or {}
        if isinstance(error_details, dict):
            error_details['operation'] = operation
            if key:
                error_details['key'] = key
        super().__init__(message=message, code=ErrorCode.SERVICE_ERROR, details=error_details, status_code=500, original_exception=original_exception)
class CacheConfigurationException(CacheException):
    def __init__(self, message: str, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=ErrorCode.CONFIGURATION_ERROR, details=details, status_code=500, original_exception=original_exception)