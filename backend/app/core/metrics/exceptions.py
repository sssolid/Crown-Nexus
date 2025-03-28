from __future__ import annotations

"""
Exceptions specific to the metrics system.

This module defines exceptions related to the metrics system,
aligned with the application's exception hierarchy.
"""

from typing import Any, Dict, List, Optional, Union

from app.core.exceptions.base import (
    AppException,
    ErrorCategory,
    ErrorCode,
    ErrorSeverity,
)


class MetricsException(AppException):
    """Base exception for metrics-related errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.UNKNOWN_ERROR,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        status_code: int = 500,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """
        Initialize the metrics exception.

        Args:
            message: Error message
            code: Error code
            details: Error details
            status_code: HTTP status code
            original_exception: Original causing exception
        """
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.SYSTEM,
            original_exception=original_exception,
        )


class MetricsConfigurationException(MetricsException):
    """Exception for metrics configuration errors."""

    def __init__(
        self,
        message: str,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """
        Initialize the metrics configuration exception.

        Args:
            message: Error message
            details: Error details
            original_exception: Original causing exception
        """
        super().__init__(
            message=message,
            code=ErrorCode.CONFIGURATION_ERROR,
            details=details,
            status_code=500,
            original_exception=original_exception,
        )


class MetricsOperationException(MetricsException):
    """Exception for metrics operation errors."""

    def __init__(
        self,
        message: str,
        operation: str,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """
        Initialize the metrics operation exception.

        Args:
            message: Error message
            operation: The operation that failed
            details: Error details
            original_exception: Original causing exception
        """
        error_details = details or {}
        if isinstance(error_details, dict):
            error_details["operation"] = operation

        super().__init__(
            message=message,
            code=ErrorCode.UNKNOWN_ERROR,
            details=error_details,
            status_code=500,
            original_exception=original_exception,
        )
