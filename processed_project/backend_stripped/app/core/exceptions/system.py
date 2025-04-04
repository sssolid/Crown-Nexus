from __future__ import annotations
'System-level exceptions for the application.\n\nThis module defines exceptions related to system components such as\ndatabase, network, external services, configuration, and security.\n'
from typing import Any, Dict, List, Optional, Union
from app.core.exceptions.base import AppException, ErrorCategory, ErrorCode, ErrorSeverity
class SystemException(AppException):
    def __init__(self, message: str, code: ErrorCode=ErrorCode.UNKNOWN_ERROR, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, status_code: int=500, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.ERROR, category=ErrorCategory.SYSTEM, original_exception=original_exception)
class DatabaseException(SystemException):
    def __init__(self, message: str, code: ErrorCode=ErrorCode.DATABASE_ERROR, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, status_code: int=500, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, original_exception=original_exception)
class DataIntegrityException(DatabaseException):
    def __init__(self, message: str, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=ErrorCode.DATABASE_ERROR, details=details, status_code=409, original_exception=original_exception)
class TransactionException(DatabaseException):
    def __init__(self, message: str, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=ErrorCode.DATABASE_ERROR, details=details, status_code=500, original_exception=original_exception)
class NetworkException(SystemException):
    def __init__(self, message: str, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, status_code: int=503, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=ErrorCode.NETWORK_ERROR, details=details, status_code=status_code, original_exception=original_exception)
class ServiceException(SystemException):
    def __init__(self, message: str, service_name: Optional[str]=None, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, status_code: int=502, original_exception: Optional[Exception]=None) -> None:
        error_details = details or {}
        if service_name:
            error_details['service_name'] = service_name
        super().__init__(message=message, code=ErrorCode.SERVICE_ERROR, details=error_details, status_code=status_code, original_exception=original_exception)
class ConfigurationException(SystemException):
    def __init__(self, message: str, component: Optional[str]=None, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        error_details = details or {}
        if component:
            error_details['component'] = component
        super().__init__(message=message, code=ErrorCode.CONFIGURATION_ERROR, details=error_details, status_code=500, original_exception=original_exception)
class SecurityException(SystemException):
    def __init__(self, message: str, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, status_code: int=403, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=ErrorCode.SECURITY_ERROR, details=details, status_code=status_code, original_exception=original_exception)
class RateLimitException(SecurityException):
    def __init__(self, message: str='Rate limit exceeded', details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, headers: Optional[Dict[str, str]]=None, original_exception: Optional[Exception]=None) -> None:
        error_details = details or {}
        error_details['headers'] = headers or {}
        super().__init__(message=message, details=error_details, status_code=429, original_exception=original_exception)