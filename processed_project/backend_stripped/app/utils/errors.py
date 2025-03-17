from __future__ import annotations
from typing import Any, Dict, List, Optional, Type, TypeVar, Union
from app.core.exceptions import AppException, AuthenticationException, BadRequestException, BusinessLogicException, ConfigurationException, DataIntegrityException, DatabaseException, ErrorCategory, ErrorCode, ErrorSeverity, ExternalServiceException, InvalidStateException, NetworkException, OperationNotAllowedException, PermissionDeniedException, RateLimitException, ResourceAlreadyExistsException, ResourceNotFoundException, ServiceUnavailableException, TimeoutException, TransactionException, ValidationException
T = TypeVar('T')
def ensure_not_none(value: Optional[T], resource_type: str, resource_id: Any, message: Optional[str]=None) -> T:
    if value is None:
        error_message = message or f'{resource_type} with ID {resource_id} not found'
        raise ResourceNotFoundException(message=error_message, code=ErrorCode.RESOURCE_NOT_FOUND, details={'resource_type': resource_type, 'resource_id': str(resource_id)}, status_code=404)
    return value
def resource_not_found(resource_type: str, resource_id: Any, message: Optional[str]=None) -> ResourceNotFoundException:
    error_message = message or f'{resource_type} with ID {resource_id} not found'
    return ResourceNotFoundException(message=error_message, code=ErrorCode.RESOURCE_NOT_FOUND, details={'resource_type': resource_type, 'resource_id': str(resource_id)}, status_code=404)
def resource_already_exists(resource_type: str, identifier: Any, field: str='id', message: Optional[str]=None) -> ResourceAlreadyExistsException:
    error_message = message or f'{resource_type} with {field} {identifier} already exists'
    return ResourceAlreadyExistsException(message=error_message, code=ErrorCode.RESOURCE_ALREADY_EXISTS, details={'resource_type': resource_type, field: str(identifier)}, status_code=409)
def validation_error(field: str, message: str, error_type: str='validation_error') -> ValidationException:
    return ValidationException(message=f'Validation error: {message}', code=ErrorCode.VALIDATION_ERROR, details={'errors': [{'loc': field.split('.'), 'msg': message, 'type': error_type}]}, status_code=400)
def permission_denied(action: str, resource_type: str, permission: Optional[str]=None) -> PermissionDeniedException:
    message = f"You don't have permission to {action} {resource_type}"
    details = {'action': action, 'resource_type': resource_type}
    if permission:
        details['required_permission'] = permission
    return PermissionDeniedException(message=message, code=ErrorCode.PERMISSION_DENIED, details=details, status_code=403)
def bad_request(message: str, details: Optional[Dict[str, Any]]=None) -> BadRequestException:
    return BadRequestException(message=message, code=ErrorCode.BAD_REQUEST, details=details, status_code=400)
def business_logic_error(message: str, details: Optional[Dict[str, Any]]=None) -> BusinessLogicException:
    return BusinessLogicException(message=message, code=ErrorCode.BUSINESS_LOGIC_ERROR, details=details, status_code=400)
def database_error(message: str, original_error: Optional[Exception]=None, details: Optional[Dict[str, Any]]=None) -> DatabaseException:
    error_details = details or {}
    return DatabaseException(message=message, code=ErrorCode.DATABASE_ERROR, details=error_details, status_code=500, original_exception=original_error)
def configuration_error(message: str, details: Optional[Dict[str, Any]]=None) -> ConfigurationException:
    return ConfigurationException(message=message, code=ErrorCode.CONFIGURATION_ERROR, details=details, status_code=500)
def external_service_error(service_name: str, message: str, original_error: Optional[Exception]=None, details: Optional[Dict[str, Any]]=None) -> ExternalServiceException:
    error_details = details or {}
    error_details['service_name'] = service_name
    return ExternalServiceException(message=f'External service error ({service_name}): {message}', code=ErrorCode.EXTERNAL_SERVICE_ERROR, details=error_details, status_code=502, original_exception=original_error)
def service_unavailable(service_name: str, message: Optional[str]=None) -> ServiceUnavailableException:
    error_message = message or f'Service {service_name} is currently unavailable'
    return ServiceUnavailableException(message=error_message, code=ErrorCode.SERVICE_UNAVAILABLE, details={'service_name': service_name}, status_code=503)
def rate_limit_exceeded(service_name: str, limit: Optional[int]=None, reset_after: Optional[int]=None) -> RateLimitException:
    message = f'Rate limit exceeded for service {service_name}'
    details = {'service_name': service_name}
    if limit is not None:
        details['limit'] = limit
    if reset_after is not None:
        details['reset_after'] = reset_after
    return RateLimitException(message=message, code=ErrorCode.RATE_LIMIT_EXCEEDED, details=details, status_code=429)
def invalid_state(entity_type: str, entity_id: Any, current_state: str, expected_state: Optional[str]=None, allowed_states: Optional[List[str]]=None) -> InvalidStateException:
    details = {'entity_type': entity_type, 'entity_id': str(entity_id), 'current_state': current_state}
    if expected_state:
        message = f'{entity_type} {entity_id} is in invalid state: {current_state} (expected: {expected_state})'
        details['expected_state'] = expected_state
    elif allowed_states:
        message = f"{entity_type} {entity_id} is in invalid state: {current_state} (allowed: {', '.join(allowed_states)})"
        details['allowed_states'] = allowed_states
    else:
        message = f'{entity_type} {entity_id} is in invalid state: {current_state}'
    return InvalidStateException(message=message, code=ErrorCode.INVALID_STATE_ERROR, details=details, status_code=409)
def operation_not_allowed(operation: str, entity_type: str, entity_id: Optional[Any]=None, reason: Optional[str]=None) -> OperationNotAllowedException:
    details = {'operation': operation, 'entity_type': entity_type}
    if entity_id is not None:
        details['entity_id'] = str(entity_id)
    if entity_id is not None:
        message = f'Operation {operation} is not allowed for {entity_type} {entity_id}'
    else:
        message = f'Operation {operation} is not allowed for {entity_type}'
    if reason:
        message += f': {reason}'
        details['reason'] = reason
    return OperationNotAllowedException(message=message, code=ErrorCode.OPERATION_NOT_ALLOWED, details=details, status_code=403)