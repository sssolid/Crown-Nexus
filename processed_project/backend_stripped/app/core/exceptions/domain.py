from __future__ import annotations
"Domain-specific exceptions for the application.\n\nThis module defines exceptions related to business logic, resources,\nauthentication, and validation that are specific to the application's domain.\n"
from typing import Any, Dict, List, Optional, Union
from app.core.exceptions.base import AppException, ErrorCategory, ErrorCode, ErrorSeverity
class ResourceException(AppException):
    def __init__(self, message: str, code: ErrorCode=ErrorCode.RESOURCE_NOT_FOUND, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, status_code: int=404, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.WARNING, category=ErrorCategory.RESOURCE, original_exception=original_exception)
class ResourceNotFoundException(ResourceException):
    def __init__(self, resource_type: str, resource_id: str, message: Optional[str]=None, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        if message is None:
            message = f'{resource_type} with ID {resource_id} not found'
        error_details = details or {'resource_type': resource_type, 'resource_id': resource_id}
        super().__init__(message=message, code=ErrorCode.RESOURCE_NOT_FOUND, details=error_details, status_code=404, original_exception=original_exception)
class ResourceAlreadyExistsException(ResourceException):
    def __init__(self, resource_type: str, identifier: str, field: str='id', message: Optional[str]=None, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        if message is None:
            message = f'{resource_type} with {field} {identifier} already exists'
        error_details = details or {'resource_type': resource_type, 'field': field, 'identifier': identifier}
        super().__init__(message=message, code=ErrorCode.RESOURCE_ALREADY_EXISTS, details=error_details, status_code=409, original_exception=original_exception)
class AuthException(AppException):
    def __init__(self, message: str, code: ErrorCode, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, status_code: int=401, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.WARNING, category=ErrorCategory.AUTH, original_exception=original_exception)
class AuthenticationException(AuthException):
    def __init__(self, message: str='Authentication failed', details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=ErrorCode.AUTHENTICATION_FAILED, details=details, status_code=401, original_exception=original_exception)
class PermissionDeniedException(AuthException):
    def __init__(self, message: str='Permission denied', action: Optional[str]=None, resource_type: Optional[str]=None, permission: Optional[str]=None, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        error_details = details or {}
        if action and resource_type:
            if not message or message == 'Permission denied':
                message = f'Permission denied to {action} {resource_type}'
            if 'action' not in error_details:
                error_details['action'] = action
            if 'resource_type' not in error_details:
                error_details['resource_type'] = resource_type
            if permission and 'permission' not in error_details:
                error_details['permission'] = permission
        super().__init__(message=message, code=ErrorCode.PERMISSION_DENIED, details=error_details, status_code=403, original_exception=original_exception)
class ValidationException(AppException):
    def __init__(self, message: str='Validation error', errors: Optional[List[Dict[str, Any]]]=None, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        error_details = errors or details or []
        super().__init__(message=message, code=ErrorCode.VALIDATION_ERROR, details=error_details, status_code=422, severity=ErrorSeverity.WARNING, category=ErrorCategory.VALIDATION, original_exception=original_exception)
class BusinessException(AppException):
    def __init__(self, message: str, code: ErrorCode=ErrorCode.BUSINESS_LOGIC_ERROR, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, status_code: int=400, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, severity=ErrorSeverity.WARNING, category=ErrorCategory.BUSINESS, original_exception=original_exception)
class InvalidStateException(BusinessException):
    def __init__(self, message: str, current_state: Optional[str]=None, expected_state: Optional[str]=None, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        error_details = details or {}
        if current_state:
            error_details['current_state'] = current_state
        if expected_state:
            error_details['expected_state'] = expected_state
        super().__init__(message=message, code=ErrorCode.INVALID_STATE, details=error_details, status_code=409, original_exception=original_exception)
class OperationNotAllowedException(BusinessException):
    def __init__(self, message: str, operation: Optional[str]=None, reason: Optional[str]=None, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        error_details = details or {}
        if operation:
            error_details['operation'] = operation
        if reason:
            error_details['reason'] = reason
        super().__init__(message=message, code=ErrorCode.OPERATION_NOT_ALLOWED, details=error_details, status_code=403, original_exception=original_exception)