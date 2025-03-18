from __future__ import annotations
from typing import Any, Dict, Optional

from app.core.exceptions.base import AppException, ErrorCode, ErrorSeverity, ErrorCategory

class BadRequestException(AppException):
    """Exception raised for bad requests."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.BAD_REQUEST,
        details: Any = None,
        status_code: int = 400,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the bad request exception."""
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.VALIDATION,
            original_exception=original_exception
        )

class PermissionDeniedException(AppException):
    """Exception raised for permission errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.PERMISSION_DENIED,
        details: Any = None,
        status_code: int = 403,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the permission denied exception."""
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.AUTHORIZATION,
            original_exception=original_exception
        )

class AuthenticationException(AppException):
    """Exception raised for authentication errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.AUTHENTICATION_FAILED,
        details: Any = None,
        status_code: int = 401,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the authentication exception."""
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.AUTHENTICATION,
            original_exception=original_exception
        )

class ResourceNotFoundException(AppException):
    """Exception raised when a resource is not found."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.RESOURCE_NOT_FOUND,
        details: Any = None,
        status_code: int = 404,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the resource not found exception."""
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.RESOURCE,
            original_exception=original_exception
        )

class ResourceAlreadyExistsException(AppException):
    """Exception raised when a resource already exists."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.RESOURCE_ALREADY_EXISTS,
        details: Any = None,
        status_code: int = 409,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the resource already exists exception."""
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.RESOURCE,
            original_exception=original_exception
        )
