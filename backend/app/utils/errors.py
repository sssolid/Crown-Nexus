# app/utils/errors.py
from __future__ import annotations

from typing import Any, Dict, List, Optional, Type, TypeVar, Union

from app.core.exceptions import (
    AppException,
    BadRequestException,
    BusinessLogicException,
    DatabaseException,
    ErrorCode,
    ErrorDetail,
    PermissionDeniedException,
    ResourceAlreadyExistsException,
    ResourceNotFoundException,
    ValidationException,
)

T = TypeVar("T")


def create_error_details(
    loc: List[str], msg: str, type_str: str = "value_error"
) -> ErrorDetail:
    """Create an error detail object.
    
    Args:
        loc: Location of the error (e.g., ["body", "username"])
        msg: Error message
        type_str: Error type string
        
    Returns:
        ErrorDetail object
    """
    return ErrorDetail(loc=loc, msg=msg, type=type_str)


def resource_not_found(
    resource_type: str, resource_id: Optional[Any] = None
) -> ResourceNotFoundException:
    """Create a ResourceNotFoundException with standard formatting.
    
    Args:
        resource_type: Type of resource (e.g., "User", "Product")
        resource_id: ID of the resource that wasn't found
        
    Returns:
        ResourceNotFoundException with a standardized message
    """
    msg = f"{resource_type} not found"
    if resource_id is not None:
        msg = f"{resource_type} with ID {resource_id} not found"
    return ResourceNotFoundException(message=msg)


def resource_already_exists(
    resource_type: str, identifier: Optional[Dict[str, Any]] = None
) -> ResourceAlreadyExistsException:
    """Create a ResourceAlreadyExistsException with standard formatting.
    
    Args:
        resource_type: Type of resource (e.g., "User", "Product")
        identifier: Identifier(s) that caused the conflict
        
    Returns:
        ResourceAlreadyExistsException with a standardized message
    """
    msg = f"{resource_type} already exists"
    if identifier:
        identifiers_str = ", ".join(f"{k}={v}" for k, v in identifier.items())
        msg = f"{resource_type} with {identifiers_str} already exists"
    return ResourceAlreadyExistsException(message=msg)


def permission_denied(action: str, resource_type: str) -> PermissionDeniedException:
    """Create a PermissionDeniedException with standard formatting.
    
    Args:
        action: Action attempted (e.g., "create", "update")
        resource_type: Type of resource (e.g., "User", "Product")
        
    Returns:
        PermissionDeniedException with a standardized message
    """
    return PermissionDeniedException(
        message=f"You don't have permission to {action} {resource_type}"
    )


def bad_request(message: str) -> BadRequestException:
    """Create a BadRequestException with the provided message.
    
    Args:
        message: Error message
        
    Returns:
        BadRequestException with the provided message
    """
    return BadRequestException(message=message)


def validation_error(
    field: Union[str, List[str]], message: str
) -> ValidationException:
    """Create a ValidationException for a specific field.
    
    Args:
        field: Field name or path
        message: Error message
        
    Returns:
        ValidationException with details for the specified field
    """
    loc = field if isinstance(field, list) else ["body", field]
    details = [create_error_details(loc=loc, msg=message)]
    return ValidationException(message=f"Validation error: {message}", details=details)


def database_error(message: str, original_error: Optional[Exception] = None) -> DatabaseException:
    """Create a DatabaseException with the provided message.
    
    Args:
        message: Error message
        original_error: Original exception that was caught
        
    Returns:
        DatabaseException with the provided message
    """
    full_message = message
    if original_error:
        full_message = f"{message}: {str(original_error)}"
    return DatabaseException(message=full_message)


def business_logic_error(message: str) -> BusinessLogicException:
    """Create a BusinessLogicException with the provided message.
    
    Args:
        message: Error message
        
    Returns:
        BusinessLogicException with the provided message
    """
    return BusinessLogicException(message=message)


def ensure_not_none(
    value: Optional[T], 
    resource_type: str, 
    resource_id: Optional[Any] = None
) -> T:
    """Ensure a value is not None, raising ResourceNotFoundException if it is.
    
    Args:
        value: Value to check
        resource_type: Type of resource for error message
        resource_id: ID of the resource for error message
        
    Returns:
        The value if it's not None
        
    Raises:
        ResourceNotFoundException: If the value is None
    """
    if value is None:
        raise resource_not_found(resource_type, resource_id)
    return value
