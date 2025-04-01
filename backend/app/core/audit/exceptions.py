from __future__ import annotations

"""
Audit-specific exceptions for the application.

This module defines exceptions related to audit operations that integrate
with the application's exception system.
"""

from typing import Any, Dict, List, Optional, Union

from app.core.exceptions.base import ErrorCode
from app.core.exceptions.service import BackendError, CoreServiceException, ManagerError


class AuditException(CoreServiceException):
    """Base exception for all audit-related errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.SERVICE_ERROR,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        status_code: int = 500,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message.
            code: Error code from ErrorCode enum.
            details: Additional error details.
            status_code: HTTP status code.
            original_exception: Original exception if this is a wrapper.
        """
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            original_exception=original_exception,
        )


class AuditBackendException(BackendError):
    """Exception raised when an audit backend operation fails."""

    def __init__(
        self,
        backend_name: str,
        operation: str = "log_event",
        message: str = "Audit backend operation failed",
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
        super().__init__(
            backend_name=backend_name,
            operation=operation,
            message=message,
            details=details,
            original_exception=original_exception,
        )


class AuditManagerException(ManagerError):
    """Exception raised when an audit manager operation fails."""

    def __init__(
        self,
        operation: str,
        message: str = "Audit manager operation failed",
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            operation: Name of the operation that failed.
            message: Human-readable error message.
            details: Additional error details.
            original_exception: Original exception if this is a wrapper.
        """
        super().__init__(
            manager_name="audit",
            operation=operation,
            message=message,
            details=details,
            original_exception=original_exception,
        )


class AuditConfigurationException(AuditException):
    """Exception raised when audit configuration is invalid."""

    def __init__(
        self,
        message: str = "Invalid audit configuration",
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message.
            details: Additional error details.
            original_exception: Original exception if this is a wrapper.
        """
        super().__init__(
            message=message,
            code=ErrorCode.CONFIGURATION_ERROR,
            details=details,
            original_exception=original_exception,
        )
