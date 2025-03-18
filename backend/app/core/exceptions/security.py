from __future__ import annotations
from typing import Any, Dict, Optional

from app.core.exceptions.base import AppException, ErrorCode, ErrorSeverity, ErrorCategory

class SecurityException(AppException):
    """Exception raised for security issues."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.SECURITY_ERROR,
        details: Any = None,
        status_code: int = 403,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the security exception."""
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.SECURITY,
            original_exception=original_exception
        )

class ConfigurationException(AppException):
    """Exception raised for configuration errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.CONFIGURATION_ERROR,
        details: Any = None,
        status_code: int = 500,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the configuration exception."""
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.SYSTEM,
            original_exception=original_exception
        )
