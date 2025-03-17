# app/utils/errors.py
from __future__ import annotations

from typing import Any, Dict, List, Optional, Type, TypeVar, Union

from app.core.dependency_manager import get_dependency
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
from app.services.error_handling_service import ErrorHandlingService

T = TypeVar("T")


def get_error_service() -> ErrorHandlingService:
    """Get the error handling service.

    Returns:
        ErrorHandlingService instance
    """
    try:
        return get_dependency("error_handling_service")
    except Exception:
        # Fallback to creating a new instance if dependency manager is not available
        return ErrorHandlingService()


def ensure_not_none(value: Optional[T], resource_type: str, resource_id: Any, message: Optional[str] = None) -> T:
    """Ensure a value is not None or raise a ResourceNotFoundException.

    Args:
        value: Value to check
        resource_type: Type of resource
        resource_id: Resource ID
        message: Optional custom error message

    Returns:
        The value if not None

    Raises:
        ResourceNotFoundException: If value is None
    """
    if value is None:
        service = get_error_service()
        raise service.create_resource_not_found_error(resource_type, resource_id)
    return value


def validation_error(field: str, message: str, error_type: str = "validation_error") -> ValidationException:
    """Create a validation error exception.

    Args:
        field: Field with validation error
        message: Error message
        error_type: Error type

    Returns:
        ValidationException
    """
    service = get_error_service()
    return service.create_validation_error(field, message, error_type)


def permission_denied(action: str, resource_type: str, permission: Optional[str] = None) -> PermissionDeniedException:
    """Create a permission denied exception.

    Args:
        action: Action being performed
        resource_type: Type of resource
        permission: Optional required permission

    Returns:
        PermissionDeniedException
    """
    service = get_error_service()
    return service.create_permission_denied_error(action, resource_type, permission)


def bad_request(message: str, details: Optional[Dict[str, Any]] = None) -> BadRequestException:
    """Create a bad request exception.

    Args:
        message: Error message
        details: Optional error details

    Returns:
        BadRequestException
    """
    return BadRequestException(
        message=message,
        code=ErrorCode.BAD_REQUEST,
        details=details or {},
        status_code=400
    )


def business_logic_error(message: str, details: Optional[Dict[str, Any]] = None) -> BusinessLogicException:
    """Create a business logic error exception.

    Args:
        message: Error message
        details: Optional error details

    Returns:
        BusinessLogicException
    """
    service = get_error_service()
    return service.create_business_logic_error(message, details)


def database_error(message: str, original_error: Optional[Exception] = None, details: Optional[Dict[str, Any]] = None) -> DatabaseException:
    """Create a database error exception.

    Args:
        message: Error message
        original_error: Optional original exception
        details: Optional error details

    Returns:
        DatabaseException
    """
    service = get_error_service()
    return service.create_database_error(message, original_error, details)


def resource_not_found(resource_type: str, resource_id: Any, message: Optional[str] = None) -> ResourceNotFoundException:
    """Create a resource not found exception.

    Args:
        resource_type: Type of resource
        resource_id: Resource ID
        message: Optional custom error message

    Returns:
        ResourceNotFoundException
    """
    error_message = message or f"{resource_type} with ID {resource_id} not found"
    return ResourceNotFoundException(
        message=error_message,
        code=ErrorCode.RESOURCE_NOT_FOUND,
        details={"resource_type": resource_type, "resource_id": str(resource_id)},
        status_code=404
    )


def resource_already_exists(resource_type: str, identifier: Any, field: str = "id", message: Optional[str] = None) -> ResourceAlreadyExistsException:
    """Create a resource already exists exception.

    Args:
        resource_type: Type of resource
        identifier: Resource identifier
        field: Field name
        message: Optional custom error message

    Returns:
        ResourceAlreadyExistsException
    """
    error_message = message or f"{resource_type} with {field} {identifier} already exists"
    return ResourceAlreadyExistsException(
        message=error_message,
        code=ErrorCode.RESOURCE_ALREADY_EXISTS,
        details={"resource_type": resource_type, field: str(identifier)},
        status_code=409
    )


def invalid_state(entity_type: str, entity_id: Any, current_state: str, expected_state: Optional[str] = None, allowed_states: Optional[List[str]] = None) -> InvalidStateException:
    """Create an invalid state exception.

    Args:
        entity_type: Type of entity
        entity_id: Entity ID
        current_state: Current state
        expected_state: Optional expected state
        allowed_states: Optional list of allowed states

    Returns:
        InvalidStateException
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


def operation_not_allowed(operation: str, entity_type: str, entity_id: Optional[Any] = None, reason: Optional[str] = None) -> OperationNotAllowedException:
    """Create an operation not allowed exception.

    Args:
        operation: Operation being performed
        entity_type: Type of entity
        entity_id: Optional entity ID
        reason: Optional reason

    Returns:
        OperationNotAllowedException
    """
    details = {"operation": operation, "entity_type": entity_type}

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


def external_service_error(service_name: str, message: str, original_error: Optional[Exception] = None, details: Optional[Dict[str, Any]] = None) -> ExternalServiceException:
    """Create an external service error exception.

    Args:
        service_name: Name of the external service
        message: Error message
        original_error: Optional original exception
        details: Optional error details

    Returns:
        ExternalServiceException
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
