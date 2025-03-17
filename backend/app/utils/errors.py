# /backend/app/utils/errors.py
from __future__ import annotations

from typing import Any, Dict, List, Optional, Type, TypeVar, Union

from app.core.exceptions import (
    AppException,
    AuthenticationException,
    BadRequestException,
    BusinessLogicException,
    ConfigurationException,
    DataIntegrityException,
    DatabaseException,
    ErrorCategory,
    ErrorCode,
    ErrorSeverity,
    ExternalServiceException,
    InvalidStateException,
    NetworkException,
    OperationNotAllowedException,
    PermissionDeniedException,
    RateLimitException,
    ResourceAlreadyExistsException,
    ResourceNotFoundException,
    ServiceUnavailableException,
    TimeoutException,
    TransactionException,
    ValidationException,
)

T = TypeVar("T")

def ensure_not_none(
    value: Optional[T],
    resource_type: str,
    resource_id: Any,
    message: Optional[str] = None
) -> T:
    """Ensure a value is not None, raising ResourceNotFoundException if it is.

    Args:
        value: Value to check
        resource_type: Type of resource for error message
        resource_id: ID of the resource for error message
        message: Custom error message (optional)

    Returns:
        The value if it's not None

    Raises:
        ResourceNotFoundException: If the value is None
    """
    if value is None:
        error_message = message or f"{resource_type} with ID {resource_id} not found"
        raise ResourceNotFoundException(
            message=error_message,
            code=ErrorCode.RESOURCE_NOT_FOUND,
            details={
                "resource_type": resource_type,
                "resource_id": str(resource_id)
            },
            status_code=404
        )
    return value

def resource_not_found(
    resource_type: str,
    resource_id: Any,
    message: Optional[str] = None
) -> ResourceNotFoundException:
    """Create a ResourceNotFoundException with standard formatting.

    Args:
        resource_type: Type of resource (e.g., "User", "Product")
        resource_id: ID of the resource that wasn't found
        message: Custom error message (optional)

    Returns:
        ResourceNotFoundException with a standardized message
    """
    error_message = message or f"{resource_type} with ID {resource_id} not found"
    return ResourceNotFoundException(
        message=error_message,
        code=ErrorCode.RESOURCE_NOT_FOUND,
        details={
            "resource_type": resource_type,
            "resource_id": str(resource_id)
        },
        status_code=404
    )

def resource_already_exists(
    resource_type: str,
    identifier: Any,
    field: str = "id",
    message: Optional[str] = None
) -> ResourceAlreadyExistsException:
    """Create a ResourceAlreadyExistsException with standard formatting.

    Args:
        resource_type: Type of resource (e.g., "User", "Product")
        identifier: Identifier(s) that caused the conflict
        field: Field name that caused the conflict
        message: Custom error message (optional)

    Returns:
        ResourceAlreadyExistsException with a standardized message
    """
    error_message = message or f"{resource_type} with {field} {identifier} already exists"
    return ResourceAlreadyExistsException(
        message=error_message,
        code=ErrorCode.RESOURCE_ALREADY_EXISTS,
        details={
            "resource_type": resource_type,
            field: str(identifier)
        },
        status_code=409
    )

def validation_error(
    field: str,
    message: str,
    error_type: str = "validation_error"
) -> ValidationException:
    """Create a ValidationException for a specific field.

    Args:
        field: Field name or path
        message: Error message
        error_type: Error type

    Returns:
        ValidationException with details for the specified field
    """
    return ValidationException(
        message=f"Validation error: {message}",
        code=ErrorCode.VALIDATION_ERROR,
        details={
            "errors": [{
                "loc": field.split("."),
                "msg": message,
                "type": error_type
            }]
        },
        status_code=400
    )

def permission_denied(
    action: str,
    resource_type: str,
    permission: Optional[str] = None
) -> PermissionDeniedException:
    """Create a PermissionDeniedException with standard formatting.

    Args:
        action: Action attempted (e.g., "create", "update")
        resource_type: Type of resource (e.g., "User", "Product")
        permission: Permission that was required

    Returns:
        PermissionDeniedException with a standardized message
    """
    message = f"You don't have permission to {action} {resource_type}"
    details = {"action": action, "resource_type": resource_type}
    
    if permission:
        details["required_permission"] = permission
        
    return PermissionDeniedException(
        message=message,
        code=ErrorCode.PERMISSION_DENIED,
        details=details,
        status_code=403
    )

def bad_request(
    message: str,
    details: Optional[Dict[str, Any]] = None
) -> BadRequestException:
    """Create a BadRequestException with the provided message.

    Args:
        message: Error message
        details: Additional error details

    Returns:
        BadRequestException with the provided message
    """
    return BadRequestException(
        message=message,
        code=ErrorCode.BAD_REQUEST,
        details=details,
        status_code=400
    )

def business_logic_error(
    message: str,
    details: Optional[Dict[str, Any]] = None
) -> BusinessLogicException:
    """Create a BusinessLogicException with the provided message.

    Args:
        message: Error message
        details: Additional error details

    Returns:
        BusinessLogicException with the provided message
    """
    return BusinessLogicException(
        message=message,
        code=ErrorCode.BUSINESS_LOGIC_ERROR,
        details=details,
        status_code=400
    )

def database_error(
    message: str,
    original_error: Optional[Exception] = None,
    details: Optional[Dict[str, Any]] = None
) -> DatabaseException:
    """Create a DatabaseException with the provided message.

    Args:
        message: Error message
        original_error: Original exception that was caught
        details: Additional error details

    Returns:
        DatabaseException with the provided message
    """
    error_details = details or {}
    
    return DatabaseException(
        message=message,
        code=ErrorCode.DATABASE_ERROR,
        details=error_details,
        status_code=500,
        original_exception=original_error
    )

def configuration_error(
    message: str,
    details: Optional[Dict[str, Any]] = None
) -> ConfigurationException:
    """Create a ConfigurationException with the provided message.

    Args:
        message: Error message
        details: Additional error details

    Returns:
        ConfigurationException with the provided message
    """
    return ConfigurationException(
        message=message,
        code=ErrorCode.CONFIGURATION_ERROR,
        details=details,
        status_code=500
    )

def external_service_error(
    service_name: str,
    message: str,
    original_error: Optional[Exception] = None,
    details: Optional[Dict[str, Any]] = None
) -> ExternalServiceException:
    """Create an ExternalServiceException for a specific service.

    Args:
        service_name: Name of the external service
        message: Error message
        original_error: Original exception that was caught
        details: Additional error details

    Returns:
        ExternalServiceException with details for the specified service
    """
    error_details = details or {}
    error_details["service_name"] = service_name
    
    return ExternalServiceException(
        message=f"External service error ({service_name}): {message}",
        code=ErrorCode.EXTERNAL_SERVICE_ERROR,
        details=error_details,
        status_code=502,
        original_exception=original_error
    )

def service_unavailable(
    service_name: str,
    message: Optional[str] = None
) -> ServiceUnavailableException:
    """Create a ServiceUnavailableException for a specific service.

    Args:
        service_name: Name of the service
        message: Custom error message (optional)

    Returns:
        ServiceUnavailableException with details for the specified service
    """
    error_message = message or f"Service {service_name} is currently unavailable"
    return ServiceUnavailableException(
        message=error_message,
        code=ErrorCode.SERVICE_UNAVAILABLE,
        details={"service_name": service_name},
        status_code=503
    )

def rate_limit_exceeded(
    service_name: str,
    limit: Optional[int] = None,
    reset_after: Optional[int] = None
) -> RateLimitException:
    """Create a RateLimitException for a specific service.

    Args:
        service_name: Name of the service
        limit: Rate limit that was exceeded
        reset_after: Seconds until rate limit resets

    Returns:
        RateLimitException with details for the specified service
    """
    message = f"Rate limit exceeded for service {service_name}"
    details = {"service_name": service_name}
    
    if limit is not None:
        details["limit"] = limit
        
    if reset_after is not None:
        details["reset_after"] = reset_after
        
    return RateLimitException(
        message=message,
        code=ErrorCode.RATE_LIMIT_EXCEEDED,
        details=details,
        status_code=429
    )

def invalid_state(
    entity_type: str,
    entity_id: Any,
    current_state: str,
    expected_state: Optional[str] = None,
    allowed_states: Optional[List[str]] = None
) -> InvalidStateException:
    """Create an InvalidStateException for a specific entity.

    Args:
        entity_type: Type of entity (e.g., "Order", "Payment")
        entity_id: ID of the entity
        current_state: Current state of the entity
        expected_state: Expected state (if one specific state was expected)
        allowed_states: List of allowed states (if multiple states were allowed)

    Returns:
        InvalidStateException with details for the specified entity
    """
    details = {
        "entity_type": entity_type,
        "entity_id": str(entity_id),
        "current_state": current_state
    }
    
    if expected_state:
        message = f"{entity_type} {entity_id} is in invalid state: {current_state} (expected: {expected_state})"
        details["expected_state"] = expected_state
    elif allowed_states:
        message = f"{entity_type} {entity_id} is in invalid state: {current_state} (allowed: {', '.join(allowed_states)})"
        details["allowed_states"] = allowed_states
    else:
        message = f"{entity_type} {entity_id} is in invalid state: {current_state}"
        
    return InvalidStateException(
        message=message,
        code=ErrorCode.INVALID_STATE_ERROR,
        details=details,
        status_code=409
    )

def operation_not_allowed(
    operation: str,
    entity_type: str,
    entity_id: Optional[Any] = None,
    reason: Optional[str] = None
) -> OperationNotAllowedException:
    """Create an OperationNotAllowedException for a specific operation.

    Args:
        operation: Operation that was attempted (e.g., "cancel", "refund")
        entity_type: Type of entity (e.g., "Order", "Payment")
        entity_id: ID of the entity (optional)
        reason: Reason why the operation is not allowed (optional)

    Returns:
        OperationNotAllowedException with details for the specified operation
    """
    details = {
        "operation": operation,
        "entity_type": entity_type
    }
    
    if entity_id is not None:
        details["entity_id"] = str(entity_id)
        
    if entity_id is not None:
        message = f"Operation {operation} is not allowed for {entity_type} {entity_id}"
    else:
        message = f"Operation {operation} is not allowed for {entity_type}"
        
    if reason:
        message += f": {reason}"
        details["reason"] = reason
        
    return OperationNotAllowedException(
        message=message,
        code=ErrorCode.OPERATION_NOT_ALLOWED,
        details=details,
        status_code=403
    )