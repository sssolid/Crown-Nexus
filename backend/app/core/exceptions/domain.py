from __future__ import annotations

"""Domain-specific exceptions for the application.

This module defines exceptions related to business logic, resources,
authentication, and validation that are specific to the application's domain.
"""

from typing import Any, Dict, List, Optional, Union

from app.core.exceptions.base import AppException, ErrorCategory, ErrorCode, ErrorSeverity


class ResourceException(AppException):
    """Base exception for resource-related errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.RESOURCE_NOT_FOUND,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        status_code: int = 404,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize a ResourceException.

        Args:
            message: Human-readable error message
            code: Error code from ErrorCode enum
            details: Additional details about the error
            status_code: HTTP status code to return
            original_exception: Original exception if this is a wrapper
        """
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.RESOURCE,
            original_exception=original_exception,
        )


class ResourceNotFoundException(ResourceException):
    """Exception raised when a requested resource is not found."""

    def __init__(
        self,
        resource_type: str,
        resource_id: str,
        message: Optional[str] = None,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize a ResourceNotFoundException.

        Args:
            resource_type: Type of resource that was not found
            resource_id: ID of the resource that was not found
            message: Optional custom message (defaults to standard not found message)
            details: Additional details about the error
            original_exception: Original exception if this is a wrapper
        """
        if message is None:
            message = f"{resource_type} with ID {resource_id} not found"

        error_details = details or {"resource_type": resource_type, "resource_id": resource_id}

        super().__init__(
            message=message,
            code=ErrorCode.RESOURCE_NOT_FOUND,
            details=error_details,
            status_code=404,
            original_exception=original_exception,
        )


class ResourceAlreadyExistsException(ResourceException):
    """Exception raised when attempting to create a resource that already exists."""

    def __init__(
        self,
        resource_type: str,
        identifier: str,
        field: str = "id",
        message: Optional[str] = None,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize a ResourceAlreadyExistsException.

        Args:
            resource_type: Type of resource that already exists
            identifier: Identifier value of the resource
            field: Field name that contains the identifier (defaults to "id")
            message: Optional custom message
            details: Additional details about the error
            original_exception: Original exception if this is a wrapper
        """
        if message is None:
            message = f"{resource_type} with {field} {identifier} already exists"

        error_details = details or {
            "resource_type": resource_type,
            "field": field,
            "identifier": identifier
        }

        super().__init__(
            message=message,
            code=ErrorCode.RESOURCE_ALREADY_EXISTS,
            details=error_details,
            status_code=409,
            original_exception=original_exception,
        )


class AuthException(AppException):
    """Base exception for authentication and authorization errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        status_code: int = 401,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize an AuthException.

        Args:
            message: Human-readable error message
            code: Error code from ErrorCode enum
            details: Additional details about the error
            status_code: HTTP status code to return
            original_exception: Original exception if this is a wrapper
        """
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.AUTH,
            original_exception=original_exception,
        )


class AuthenticationException(AuthException):
    """Exception raised when authentication fails."""

    def __init__(
        self,
        message: str = "Authentication failed",
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize an AuthenticationException.

        Args:
            message: Human-readable error message
            details: Additional details about the error
            original_exception: Original exception if this is a wrapper
        """
        super().__init__(
            message=message,
            code=ErrorCode.AUTHENTICATION_FAILED,
            details=details,
            status_code=401,
            original_exception=original_exception,
        )


class PermissionDeniedException(AuthException):
    """Exception raised when a user doesn't have permission for an action."""

    def __init__(
        self,
        message: str = "Permission denied",
        action: Optional[str] = None,
        resource_type: Optional[str] = None,
        permission: Optional[str] = None,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize a PermissionDeniedException.

        Args:
            message: Human-readable error message
            action: The action that was attempted (e.g., "create", "read")
            resource_type: The type of resource being accessed
            permission: The permission that was required
            details: Additional details about the error
            original_exception: Original exception if this is a wrapper
        """
        error_details = details or {}

        if action and resource_type:
            if not message or message == "Permission denied":
                message = f"Permission denied to {action} {resource_type}"

            if "action" not in error_details:
                error_details["action"] = action

            if "resource_type" not in error_details:
                error_details["resource_type"] = resource_type

            if permission and "permission" not in error_details:
                error_details["permission"] = permission

        super().__init__(
            message=message,
            code=ErrorCode.PERMISSION_DENIED,
            details=error_details,
            status_code=403,
            original_exception=original_exception,
        )


class ValidationException(AppException):
    """Exception raised when input validation fails."""

    def __init__(
        self,
        message: str = "Validation error",
        errors: Optional[List[Dict[str, Any]]] = None,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize a ValidationException.

        Args:
            message: Human-readable error message
            errors: List of validation errors
            details: Additional details about the error
            original_exception: Original exception if this is a wrapper
        """
        error_details = errors or details or []

        super().__init__(
            message=message,
            code=ErrorCode.VALIDATION_ERROR,
            details=error_details,
            status_code=422,
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.VALIDATION,
            original_exception=original_exception,
        )


class BusinessException(AppException):
    """Exception raised when a business rule is violated."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.BUSINESS_LOGIC_ERROR,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        status_code: int = 400,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize a BusinessException.

        Args:
            message: Human-readable error message
            code: Error code from ErrorCode enum
            details: Additional details about the error
            status_code: HTTP status code to return
            original_exception: Original exception if this is a wrapper
        """
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.BUSINESS,
            original_exception=original_exception,
        )


class InvalidStateException(BusinessException):
    """Exception raised when an operation is attempted on an entity in an invalid state."""

    def __init__(
        self,
        message: str,
        current_state: Optional[str] = None,
        expected_state: Optional[str] = None,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize an InvalidStateException.

        Args:
            message: Human-readable error message
            current_state: The current state of the entity
            expected_state: The expected state for the operation
            details: Additional details about the error
            original_exception: Original exception if this is a wrapper
        """
        error_details = details or {}

        if current_state:
            error_details["current_state"] = current_state

        if expected_state:
            error_details["expected_state"] = expected_state

        super().__init__(
            message=message,
            code=ErrorCode.INVALID_STATE,
            details=error_details,
            status_code=409,
            original_exception=original_exception,
        )


class OperationNotAllowedException(BusinessException):
    """Exception raised when an operation is not allowed due to business rules."""

    def __init__(
        self,
        message: str,
        operation: Optional[str] = None,
        reason: Optional[str] = None,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize an OperationNotAllowedException.

        Args:
            message: Human-readable error message
            operation: The operation that was attempted
            reason: The reason the operation is not allowed
            details: Additional details about the error
            original_exception: Original exception if this is a wrapper
        """
        error_details = details or {}

        if operation:
            error_details["operation"] = operation

        if reason:
            error_details["reason"] = reason

        super().__init__(
            message=message,
            code=ErrorCode.OPERATION_NOT_ALLOWED,
            details=error_details,
            status_code=403,
            original_exception=original_exception,
        )
