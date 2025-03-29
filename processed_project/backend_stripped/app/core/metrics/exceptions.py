from __future__ import annotations
"\nExceptions specific to the metrics system.\n\nThis module defines exceptions related to the metrics system,\naligned with the application's exception hierarchy.\n"
from typing import Any, Dict, List, Optional, Union
from app.core.exceptions.base import AppException, ErrorCategory, ErrorCode, ErrorSeverity
class MetricsException(AppException):
    def __init__(self, message: str, code: ErrorCode=ErrorCode.UNKNOWN_ERROR, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, status_code: int=500, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.WARNING, category=ErrorCategory.SYSTEM, original_exception=original_exception)
class MetricsConfigurationException(MetricsException):
    def __init__(self, message: str, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=ErrorCode.CONFIGURATION_ERROR, details=details, status_code=500, original_exception=original_exception)
class MetricsOperationException(MetricsException):
    def __init__(self, message: str, operation: str, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        error_details = details or {}
        if isinstance(error_details, dict):
            error_details['operation'] = operation
        super().__init__(message=message, code=ErrorCode.UNKNOWN_ERROR, details=error_details, status_code=500, original_exception=original_exception)