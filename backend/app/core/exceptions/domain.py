# /backend/app/core/exceptions/domain.py
from __future__ import annotations

"""Domain-specific exceptions for the application.

This module defines exceptions related to business logic, resources,
authentication, and validation that are specific to the application's domain.
"""

from typing import Any, Dict, List, Optional, Union

from app.core.exceptions.base import (
    AppException,
    ErrorCategory,
    ErrorCode,
    ErrorSeverity,
)


class ResourceException(AppException):
    """Base exception for resource-related errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.RESOURCE_NOT_FOUND,
        details: Any = None,
        status_code: int = 404,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize a resource exception.

        Args:
            message: Human-readable error message
            code: Error code
            details: Additional error details
            status_code: HTTP status code
            original_exception: Original exception
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
    """Exception raised when a resource is not found."""

    def __init__(
        self,
        resource_type: str,
        resource_id: str,
        message: Optional[str] = None,
        details: Any = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize a resource not found exception.

        Args:
            resource_type: Type of resource (e.g., "User", "Product")
            resource_id: ID of the resource
            message: Custom error message (optional)
            details: Additional error details
            original_exception: Original exception
        """
        if message is None:
            message = f"{resource_type} with ID {resource_id} not found"

        error_details = details or {
            "resource_type": resource_type,
            "resource_id": resource_id,
        }

        super().__init__(
            message=message,
            code=ErrorCode.RESOURCE_NOT_FOUND,
            details=error_details,
            status_code=404,
            original_exception=original_exception,
        )


class ResourceAlreadyExistsException(ResourceException):
    """Exception raised when a resource already exists."""

    def __init__(
        self,
        resource_type: str,
        identifier: str,
        field: str = "id",
        message: Optional[str] = None,
        details: Any = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize a resource already exists exception.

        Args:
            resource_type: Type of resource (e.g., "User", "Product")
            identifier: Value of the unique identifier
            field: Name of the field that must be unique
            message: Custom error message (optional)
            details: Additional error details
            original_exception: Original exception
        """
        if message is None:
            message = f"{resource_type} with {field} {identifier} already exists"

        error_details = details or {
            "resource_type": resource_type,
            "field": field,
            "identifier": identifier,
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
        details: Any = None,
        status_code: int = 401,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize an authentication/authorization exception.

        Args:
            message: Human-readable error message
            code: Error code
            details: Additional error details
            status_code: HTTP status code
            original_exception: Original exception
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
    """Exception raised for authentication errors."""

    def __init__(
        self,
        message: str = "Authentication failed",
        details: Any = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize an authentication exception.

        Args:
            message: Human-readable error message
            details: Additional error details
            original_exception: Original exception
        """
        super().__init__(
            message=message,
            code=ErrorCode.AUTHENTICATION_FAILED,
            details=details,
            status_code=401,
            original_exception=original_exception,
        )


class PermissionDeniedException(AuthException):
    """Exception raised for permission/authorization errors."""

    def __init__(
        self,
        message: str = "Permission denied",
        action: Optional[str] = None,
        resource_type: Optional[str] = None,
        permission: Optional[str] = None,
        details: Any = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize a permission denied exception.

        Args:
            message: Human-readable error message
            action: Attempted action (e.g., "create", "update")
            resource_type: Type of resource being accessed
            permission: Required permission
            details: Additional error details
            original_exception: Original exception
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
    """Exception raised for validation errors."""

    def __init__(
        self,
        message: str = "Validation error",
        errors: Optional[List[Dict[str, Any]]] = None,
        details: Any = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize a validation exception.

        Args:
            message: Human-readable error message
            errors: List of validation errors
            details: Additional error details
            original_exception: Original exception
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
    """Exception raised for business logic errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.BUSINESS_LOGIC_ERROR,
        details: Any = None,
        status_code: int = 400,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize a business logic exception.

        Args:
            message: Human-readable error message
            code: Error code
            details: Additional error details
            status_code: HTTP status code
            original_exception: Original exception
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
    """Exception raised when an operation is invalid for the current state."""

    def __init__(
        self,
        message: str,
        current_state: Optional[str] = None,
        expected_state: Optional[str] = None,
        details: Any = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize an invalid state exception.

        Args:
            message: Human-readable error message
            current_state: Current state of the entity
            expected_state: Expected state for the operation
            details: Additional error details
            original_exception: Original exception
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
    """Exception raised when an operation is not allowed."""

    def __init__(
        self,
        message: str,
        operation: Optional[str] = None,
        reason: Optional[str] = None,
        details: Any = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize an operation not allowed exception.

        Args:
            message: Human-readable error message
            operation: Attempted operation
            reason: Reason why the operation is not allowed
            details: Additional error details
            original_exception: Original exception
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
