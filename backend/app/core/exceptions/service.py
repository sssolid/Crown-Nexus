from __future__ import annotations

"""
Core service exceptions.

This module defines exceptions specific to core services that can be extended
by each core package for specific error cases.
"""

from typing import Any, Dict, List, Optional, Union

from app.core.exceptions.base import AppException, ErrorCategory, ErrorCode, ErrorSeverity


class CoreServiceException(AppException):
    """Base exception for all core service errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.SERVICE_ERROR,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        status_code: int = 500,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message.
            code: Error code from ErrorCode enum.
            details: Additional error details.
            status_code: HTTP status code.
            severity: Error severity level.
            original_exception: Original exception if this is a wrapper.
        """
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=severity,
            category=ErrorCategory.SYSTEM,
            original_exception=original_exception,
        )


class ServiceInitializationError(CoreServiceException):
    """Exception raised when a service fails to initialize."""

    def __init__(
        self,
        service_name: str,
        message: str = "Service initialization failed",
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            service_name: Name of the service that failed to initialize.
            message: Human-readable error message.
            details: Additional error details.
            original_exception: Original exception if this is a wrapper.
        """
        error_details = details or {}
        if isinstance(error_details, dict):
            error_details["service_name"] = service_name

        super().__init__(
            message=f"{message}: {service_name}",
            code=ErrorCode.INITIALIZATION_ERROR,
            details=error_details,
            severity=ErrorSeverity.CRITICAL,
            original_exception=original_exception,
        )


class ServiceShutdownError(CoreServiceException):
    """Exception raised when a service fails to shut down."""

    def __init__(
        self,
        service_name: str,
        message: str = "Service shutdown failed",
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            service_name: Name of the service that failed to shut down.
            message: Human-readable error message.
            details: Additional error details.
            original_exception: Original exception if this is a wrapper.
        """
        error_details = details or {}
        if isinstance(error_details, dict):
            error_details["service_name"] = service_name

        super().__init__(
            message=f"{message}: {service_name}",
            code=ErrorCode.SERVICE_ERROR,
            details=error_details,
            severity=ErrorSeverity.ERROR,
            original_exception=original_exception,
        )


class ServiceNotInitializedError(CoreServiceException):
    """Exception raised when a service is used before being initialized."""

    def __init__(
        self,
        service_name: str,
        message: str = "Service not initialized",
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            service_name: Name of the service that is not initialized.
            message: Human-readable error message.
            details: Additional error details.
            original_exception: Original exception if this is a wrapper.
        """
        error_details = details or {}
        if isinstance(error_details, dict):
            error_details["service_name"] = service_name

        super().__init__(
            message=f"{message}: {service_name}",
            code=ErrorCode.SERVICE_ERROR,
            details=error_details,
            severity=ErrorSeverity.ERROR,
            original_exception=original_exception,
        )


class BackendError(CoreServiceException):
    """Exception raised when a backend operation fails."""

    def __init__(
        self,
        backend_name: str,
        operation: str,
        message: str = "Backend operation failed",
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            backend_name: Name of the backend that failed.
            operation: Name of the operation that failed.
            message: Human-readable error message.
            details: Additional error details.
            original_exception: Original exception if this is a wrapper.
        """
        error_details = details or {}
        if isinstance(error_details, dict):
            error_details["backend_name"] = backend_name
            error_details["operation"] = operation

        super().__init__(
            message=f"{message}: {operation} on {backend_name}",
            code=ErrorCode.SERVICE_ERROR,
            details=error_details,
            severity=ErrorSeverity.ERROR,
            original_exception=original_exception,
        )


class ConfigurationError(CoreServiceException):
    """Exception raised when service configuration is invalid."""

    def __init__(
        self,
        service_name: str,
        message: str = "Invalid service configuration",
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            service_name: Name of the service with invalid configuration.
            message: Human-readable error message.
            details: Additional error details.
            original_exception: Original exception if this is a wrapper.
        """
        error_details = details or {}
        if isinstance(error_details, dict):
            error_details["service_name"] = service_name

        super().__init__(
            message=f"{message}: {service_name}",
            code=ErrorCode.CONFIGURATION_ERROR,
            details=error_details,
            severity=ErrorSeverity.ERROR,
            original_exception=original_exception,
        )


class ManagerError(CoreServiceException):
    """Exception raised when a manager operation fails."""

    def __init__(
        self,
        manager_name: str,
        operation: str,
        message: str = "Manager operation failed",
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            manager_name: Name of the manager that failed.
            operation: Name of the operation that failed.
            message: Human-readable error message.
            details: Additional error details.
            original_exception: Original exception if this is a wrapper.
        """
        error_details = details or {}
        if isinstance(error_details, dict):
            error_details["manager_name"] = manager_name
            error_details["operation"] = operation

        super().__init__(
            message=f"{message}: {operation} on {manager_name}",
            code=ErrorCode.SERVICE_ERROR,
            details=error_details,
            severity=ErrorSeverity.ERROR,
            original_exception=original_exception,
        )
