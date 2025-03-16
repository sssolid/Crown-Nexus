from __future__ import annotations
from typing import Any, Dict, List, Optional, Type, TypeVar, Union
from app.core.exceptions import AppException, BadRequestException, BusinessLogicException, DatabaseException, ErrorCode, ErrorDetail, PermissionDeniedException, ResourceAlreadyExistsException, ResourceNotFoundException, ValidationException
T = TypeVar('T')
def create_error_details(loc: List[str], msg: str, type_str: str='value_error') -> ErrorDetail:
    return ErrorDetail(loc=loc, msg=msg, type=type_str)
def resource_not_found(resource_type: str, resource_id: Optional[Any]=None) -> ResourceNotFoundException:
    msg = f'{resource_type} not found'
    if resource_id is not None:
        msg = f'{resource_type} with ID {resource_id} not found'
    return ResourceNotFoundException(message=msg)
def resource_already_exists(resource_type: str, identifier: Optional[Dict[str, Any]]=None) -> ResourceAlreadyExistsException:
    msg = f'{resource_type} already exists'
    if identifier:
        identifiers_str = ', '.join((f'{k}={v}' for k, v in identifier.items()))
        msg = f'{resource_type} with {identifiers_str} already exists'
    return ResourceAlreadyExistsException(message=msg)
def permission_denied(action: str, resource_type: str) -> PermissionDeniedException:
    return PermissionDeniedException(message=f"You don't have permission to {action} {resource_type}")
def bad_request(message: str) -> BadRequestException:
    return BadRequestException(message=message)
def validation_error(field: Union[str, List[str]], message: str) -> ValidationException:
    loc = field if isinstance(field, list) else ['body', field]
    details = [create_error_details(loc=loc, msg=message)]
    return ValidationException(message=f'Validation error: {message}', details=details)
def database_error(message: str, original_error: Optional[Exception]=None) -> DatabaseException:
    full_message = message
    if original_error:
        full_message = f'{message}: {str(original_error)}'
    return DatabaseException(message=full_message)
def business_logic_error(message: str) -> BusinessLogicException:
    return BusinessLogicException(message=message)
def ensure_not_none(value: Optional[T], resource_type: str, resource_id: Optional[Any]=None) -> T:
    if value is None:
        raise resource_not_found(resource_type, resource_id)
    return value