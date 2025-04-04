from __future__ import annotations
'\nCore service exceptions.\n\nThis module defines exceptions specific to core services that can be extended\nby each core package for specific error cases.\n'
from typing import Any, Dict, List, Optional, Union
from app.core.exceptions.base import AppException, ErrorCategory, ErrorCode, ErrorSeverity
class CoreServiceException(AppException):
    def __init__(self, message: str, code: ErrorCode=ErrorCode.SERVICE_ERROR, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, status_code: int=500, severity: ErrorSeverity=ErrorSeverity.ERROR, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=severity, category=ErrorCategory.SYSTEM, original_exception=original_exception)
class ServiceInitializationError(CoreServiceException):
    def __init__(self, service_name: str, message: str='Service initialization failed', details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        error_details = details or {}
        if isinstance(error_details, dict):
            error_details['service_name'] = service_name
        super().__init__(message=f'{message}: {service_name}', code=ErrorCode.INITIALIZATION_ERROR, details=error_details, severity=ErrorSeverity.CRITICAL, original_exception=original_exception)
class ServiceShutdownError(CoreServiceException):
    def __init__(self, service_name: str, message: str='Service shutdown failed', details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        error_details = details or {}
        if isinstance(error_details, dict):
            error_details['service_name'] = service_name
        super().__init__(message=f'{message}: {service_name}', code=ErrorCode.SERVICE_ERROR, details=error_details, severity=ErrorSeverity.ERROR, original_exception=original_exception)
class ServiceNotInitializedError(CoreServiceException):
    def __init__(self, service_name: str, message: str='Service not initialized', details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        error_details = details or {}
        if isinstance(error_details, dict):
            error_details['service_name'] = service_name
        super().__init__(message=f'{message}: {service_name}', code=ErrorCode.SERVICE_ERROR, details=error_details, severity=ErrorSeverity.ERROR, original_exception=original_exception)
class BackendError(CoreServiceException):
    def __init__(self, backend_name: str, operation: str, message: str='Backend operation failed', details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        error_details = details or {}
        if isinstance(error_details, dict):
            error_details['backend_name'] = backend_name
            error_details['operation'] = operation
        super().__init__(message=f'{message}: {operation} on {backend_name}', code=ErrorCode.SERVICE_ERROR, details=error_details, severity=ErrorSeverity.ERROR, original_exception=original_exception)
class ConfigurationError(CoreServiceException):
    def __init__(self, service_name: str, message: str='Invalid service configuration', details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        error_details = details or {}
        if isinstance(error_details, dict):
            error_details['service_name'] = service_name
        super().__init__(message=f'{message}: {service_name}', code=ErrorCode.CONFIGURATION_ERROR, details=error_details, severity=ErrorSeverity.ERROR, original_exception=original_exception)
class ManagerError(CoreServiceException):
    def __init__(self, manager_name: str, operation: str, message: str='Manager operation failed', details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        error_details = details or {}
        if isinstance(error_details, dict):
            error_details['manager_name'] = manager_name
            error_details['operation'] = operation
        super().__init__(message=f'{message}: {operation} on {manager_name}', code=ErrorCode.SERVICE_ERROR, details=error_details, severity=ErrorSeverity.ERROR, original_exception=original_exception)