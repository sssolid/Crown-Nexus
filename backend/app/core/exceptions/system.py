from __future__ import annotations

"""System-level exceptions for the application.

This module defines exceptions related to system components such as
database, network, external services, configuration, and security.
"""

from typing import Any, Dict, List, Optional, Union

from app.core.exceptions.base import AppException, ErrorCategory, ErrorCode, ErrorSeverity


class SystemException(AppException):
    """Base exception for system-related errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.UNKNOWN_ERROR,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        status_code: int = 500,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize a SystemException.

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
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.SYSTEM,
            original_exception=original_exception,
        )


class DatabaseException(SystemException):
    """Exception raised when a database operation fails."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.DATABASE_ERROR,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        status_code: int = 500,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize a DatabaseException.

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
            original_exception=original_exception,
        )


class DataIntegrityException(DatabaseException):
    """Exception raised when a database operation would violate data integrity."""

    def __init__(
        self,
        message: str,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize a DataIntegrityException.

        Args:
            message: Human-readable error message
            details: Additional details about the error
            original_exception: Original exception if this is a wrapper
        """
        super().__init__(
            message=message,
            code=ErrorCode.DATABASE_ERROR,
            details=details,
            status_code=409,
            original_exception=original_exception,
        )


class TransactionException(DatabaseException):
    """Exception raised when a database transaction fails."""

    def __init__(
        self,
        message: str,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize a TransactionException.

        Args:
            message: Human-readable error message
            details: Additional details about the error
            original_exception: Original exception if this is a wrapper
        """
        super().__init__(
            message=message,
            code=ErrorCode.DATABASE_ERROR,
            details=details,
            status_code=500,
            original_exception=original_exception,
        )


class NetworkException(SystemException):
    """Exception raised when a network operation fails."""

    def __init__(
        self,
        message: str,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        status_code: int = 503,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize a NetworkException.

        Args:
            message: Human-readable error message
            details: Additional details about the error
            status_code: HTTP status code to return
            original_exception: Original exception if this is a wrapper
        """
        super().__init__(
            message=message,
            code=ErrorCode.NETWORK_ERROR,
            details=details,
            status_code=status_code,
            original_exception=original_exception,
        )


class ServiceException(SystemException):
    """Exception raised when an external service call fails."""

    def __init__(
        self,
        message: str,
        service_name: Optional[str] = None,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        status_code: int = 502,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize a ServiceException.

        Args:
            message: Human-readable error message
            service_name: Name of the external service that failed
            details: Additional details about the error
            status_code: HTTP status code to return
            original_exception: Original exception if this is a wrapper
        """
        error_details = details or {}

        if service_name:
            error_details["service_name"] = service_name

        super().__init__(
            message=message,
            code=ErrorCode.SERVICE_ERROR,
            details=error_details,
            status_code=status_code,
            original_exception=original_exception,
        )


class ConfigurationException(SystemException):
    """Exception raised when there is an issue with application configuration."""

    def __init__(
        self,
        message: str,
        component: Optional[str] = None,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize a ConfigurationException.

        Args:
            message: Human-readable error message
            component: The component with configuration issues
            details: Additional details about the error
            original_exception: Original exception if this is a wrapper
        """
        error_details = details or {}

        if component:
            error_details["component"] = component

        super().__init__(
            message=message,
            code=ErrorCode.CONFIGURATION_ERROR,
            details=error_details,
            status_code=500,
            original_exception=original_exception,
        )


class SecurityException(SystemException):
    """Exception raised when a security-related issue occurs."""

    def __init__(
        self,
        message: str,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        status_code: int = 403,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize a SecurityException.

        Args:
            message: Human-readable error message
            details: Additional details about the error
            status_code: HTTP status code to return
            original_exception: Original exception if this is a wrapper
        """
        super().__init__(
            message=message,
            code=ErrorCode.SECURITY_ERROR,
            details=details,
            status_code=status_code,
            original_exception=original_exception,
        )


class RateLimitException(SecurityException):
    """Exception raised when a rate limit is exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        headers: Optional[Dict[str, str]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize a RateLimitException.

        Args:
            message: Human-readable error message
            details: Additional details about the error
            headers: HTTP headers to include in the response
            original_exception: Original exception if this is a wrapper
        """
        error_details = details or {}
        error_details["headers"] = headers or {}

        super().__init__(
            message=message,
            details=error_details,
            status_code=429,
            original_exception=original_exception,
        )
