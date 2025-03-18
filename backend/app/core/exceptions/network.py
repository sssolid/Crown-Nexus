from __future__ import annotations
from typing import Any, Dict, Optional

from app.core.exceptions.base import AppException, ErrorCode, ErrorSeverity, ErrorCategory

class NetworkException(AppException):
    """Exception raised for network errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.NETWORK_ERROR,
        details: Any = None,
        status_code: int = 503,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the network exception."""
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.NETWORK,
            original_exception=original_exception
        )

class TimeoutException(NetworkException):
    """Exception raised for timeout errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.TIMEOUT_ERROR,
        details: Any = None,
        status_code: int = 504,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the timeout exception."""
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            original_exception=original_exception
        )

class ExternalServiceException(AppException):
    """Exception raised for external service errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.EXTERNAL_SERVICE_ERROR,
        details: Any = None,
        status_code: int = 502,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the external service exception."""
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.EXTERNAL,
            original_exception=original_exception
        )

class ServiceUnavailableException(ExternalServiceException):
    """Exception raised when an external service is unavailable."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.SERVICE_UNAVAILABLE,
        details: Any = None,
        status_code: int = 503,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the service unavailable exception."""
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            original_exception=original_exception
        )

class RateLimitException(ExternalServiceException):
    """Exception raised for rate limit errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.RATE_LIMIT_EXCEEDED,
        details: Any = None,
        status_code: int = 429,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the rate limit exception."""
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            original_exception=original_exception
        )
