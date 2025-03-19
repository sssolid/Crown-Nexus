# /backend/app/core/exceptions/system.py
from __future__ import annotations

"""System-level exceptions for the application.

This module defines exceptions related to system components such as
database, network, external services, configuration, and security.
"""

from typing import Any, Dict, Optional

from app.core.exceptions.base import (
    AppException,
    ErrorCategory,
    ErrorCode,
    ErrorSeverity,
)


class SystemException(AppException):
    """Base exception for system-level errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.UNKNOWN_ERROR,
        details: Any = None,
        status_code: int = 500,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize a system exception.

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
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.SYSTEM,
            original_exception=original_exception
        )


class DatabaseException(SystemException):
    """Exception raised for database errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.DATABASE_ERROR,
        details: Any = None,
        status_code: int = 500,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize a database exception.

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
            original_exception=original_exception
        )


class DataIntegrityException(DatabaseException):
    """Exception raised for data integrity errors."""

    def __init__(
        self,
        message: str,
        details: Any = None,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize a data integrity exception.

        Args:
            message: Human-readable error message
            details: Additional error details
            original_exception: Original exception
        """
        super().__init__(
            message=message,
            code=ErrorCode.DATABASE_ERROR,
            details=details,
            status_code=409,
            original_exception=original_exception
        )


class TransactionException(DatabaseException):
    """Exception raised for transaction errors."""

    def __init__(
        self,
        message: str,
        details: Any = None,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize a transaction exception.

        Args:
            message: Human-readable error message
            details: Additional error details
            original_exception: Original exception
        """
        super().__init__(
            message=message,
            code=ErrorCode.DATABASE_ERROR,
            details=details,
            status_code=500,
            original_exception=original_exception
        )


class NetworkException(SystemException):
    """Exception raised for network errors."""

    def __init__(
        self,
        message: str,
        details: Any = None,
        status_code: int = 503,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize a network exception.

        Args:
            message: Human-readable error message
            details: Additional error details
            status_code: HTTP status code
            original_exception: Original exception
        """
        super().__init__(
            message=message,
            code=ErrorCode.NETWORK_ERROR,
            details=details,
            status_code=status_code,
            original_exception=original_exception
        )


class ServiceException(SystemException):
    """Exception raised for external service errors."""

    def __init__(
        self,
        message: str,
        service_name: Optional[str] = None,
        details: Any = None,
        status_code: int = 502,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize a service exception.

        Args:
            message: Human-readable error message
            service_name: Name of the external service
            details: Additional error details
            status_code: HTTP status code
            original_exception: Original exception
        """
        error_details = details or {}
        if service_name:
            error_details["service_name"] = service_name

        super().__init__(
            message=message,
            code=ErrorCode.SERVICE_ERROR,
            details=error_details,
            status_code=status_code,
            original_exception=original_exception
        )


class ConfigurationException(SystemException):
    """Exception raised for configuration errors."""

    def __init__(
        self,
        message: str,
        component: Optional[str] = None,
        details: Any = None,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize a configuration exception.

        Args:
            message: Human-readable error message
            component: Component with configuration error
            details: Additional error details
            original_exception: Original exception
        """
        error_details = details or {}
        if component:
            error_details["component"] = component

        super().__init__(
            message=message,
            code=ErrorCode.CONFIGURATION_ERROR,
            details=error_details,
            status_code=500,
            original_exception=original_exception
        )


class SecurityException(SystemException):
    """Exception raised for security issues."""

    def __init__(
        self,
        message: str,
        details: Any = None,
        status_code: int = 403,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize a security exception.

        Args:
            message: Human-readable error message
            details: Additional error details
            status_code: HTTP status code
            original_exception: Original exception
        """
        super().__init__(
            message=message,
            code=ErrorCode.SECURITY_ERROR,
            details=details,
            status_code=status_code,
            original_exception=original_exception
        )


class RateLimitException(SecurityException):
    """Exception raised for rate limit errors."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        details: Any = None,
        headers: Optional[Dict[str, str]] = None,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize a rate limit exception.

        Args:
            message: Human-readable error message
            details: Additional error details
            headers: HTTP headers to include in the response
            original_exception: Original exception
        """
        error_details = details or {}
        error_details["headers"] = headers or {}

        super().__init__(
            message=message,
            details=error_details,
            status_code=429,
            original_exception=original_exception
        )
