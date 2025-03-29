from __future__ import annotations
"\nPagination-specific exceptions for the application.\n\nThis module defines exceptions related to pagination operations that integrate\nwith the application's exception system.\n"
from typing import Any, Dict, List, Optional, Union
from app.core.exceptions.base import AppException, ErrorCategory, ErrorCode, ErrorSeverity
class PaginationException(AppException):
    def __init__(self, message: str, code: ErrorCode=ErrorCode.BUSINESS_LOGIC_ERROR, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, status_code: int=400, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.WARNING, category=ErrorCategory.BUSINESS, original_exception=original_exception)
class InvalidPaginationParamsException(PaginationException):
    def __init__(self, message: str, params: Dict[str, Any], details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        error_details = details or {'params': params}
        super().__init__(message=message, code=ErrorCode.VALIDATION_ERROR, details=error_details, status_code=422, original_exception=original_exception)
class InvalidCursorException(PaginationException):
    def __init__(self, message: str='Invalid pagination cursor', cursor: Optional[str]=None, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        error_details = details or {}
        if cursor:
            error_details['cursor'] = cursor
        super().__init__(message=message, code=ErrorCode.VALIDATION_ERROR, details=error_details, status_code=422, original_exception=original_exception)
class InvalidSortFieldException(PaginationException):
    def __init__(self, field: str, model: str, message: Optional[str]=None, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        if message is None:
            message = f'Invalid sort field: {field} for model {model}'
        error_details = details or {'field': field, 'model': model}
        super().__init__(message=message, code=ErrorCode.VALIDATION_ERROR, details=error_details, status_code=422, original_exception=original_exception)