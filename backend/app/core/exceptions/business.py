from __future__ import annotations
from typing import Any, Optional

from app.core.exceptions.base import AppException, ErrorCode, ErrorSeverity, ErrorCategory

class BusinessLogicException(AppException):
    """Exception raised for business logic errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.BUSINESS_LOGIC_ERROR,
        details: Any = None,
        status_code: int = 400,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the business logic exception."""
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.BUSINESS,
            original_exception=original_exception
        )

class ValidationException(AppException):
    """Exception raised for validation errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.VALIDATION_ERROR,
        details: Any = None,
        status_code: int = 422,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the validation exception."""
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.VALIDATION,
            original_exception=original_exception
        )

class InvalidStateException(BusinessLogicException):
    """Exception raised for invalid state errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.INVALID_STATE_ERROR,
        details: Any = None,
        status_code: int = 409,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the invalid state exception."""
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            original_exception=original_exception
        )

class OperationNotAllowedException(BusinessLogicException):
    """Exception raised when an operation is not allowed."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.OPERATION_NOT_ALLOWED,
        details: Any = None,
        status_code: int = 403,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the operation not allowed exception."""
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            original_exception=original_exception
        )
