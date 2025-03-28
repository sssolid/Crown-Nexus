# app/core/rate_limiting/exceptions.py
from __future__ import annotations

"""
Rate limiting system exceptions.

This module defines exceptions specific to the rate limiting system,
aligned with the application's exception hierarchy.
"""

from typing import Any, Dict, List, Optional, Union

from app.core.exceptions.base import (
    AppException,
    ErrorCategory,
    ErrorCode,
    ErrorSeverity,
)


class RateLimitingException(AppException):
    """Base exception for rate limiting errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.SECURITY_ERROR,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        status_code: int = 429,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize a rate limiting exception.

        Args:
            message: Human-readable error message.
            code: Error code from ErrorCode enum.
            details: Additional details about the error.
            status_code: HTTP status code for the error.
            original_exception: The original exception that caused this one.
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


class RateLimitExceededException(RateLimitingException):
    """Exception raised when a rate limit is exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        headers: Optional[Dict[str, str]] = None,
        reset_seconds: Optional[int] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize a rate limit exceeded exception.

        Args:
            message: Human-readable error message.
            details: Additional details about the error.
            headers: HTTP headers to include in the response.
            reset_seconds: Seconds until the rate limit resets.
            original_exception: The original exception that caused this one.
        """
        error_details = details or {}
        if isinstance(error_details, dict):
            error_details["headers"] = headers or {}
            if reset_seconds:
                error_details["reset_seconds"] = reset_seconds

        super().__init__(
            message=message,
            details=error_details,
            status_code=429,
            original_exception=original_exception,
        )


class RateLimitingServiceException(RateLimitingException):
    """Exception raised when the rate limiting service encounters an error."""

    def __init__(
        self,
        message: str,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize a rate limiting service exception.

        Args:
            message: Human-readable error message.
            details: Additional details about the error.
            original_exception: The original exception that caused this one.
        """
        super().__init__(
            message=message,
            code=ErrorCode.SERVICE_ERROR,
            details=details,
            status_code=500,
            original_exception=original_exception,
        )


class RateLimitingConfigurationException(RateLimitingException):
    """Exception raised when the rate limiting configuration is invalid."""

    def __init__(
        self,
        message: str,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize a rate limiting configuration exception.

        Args:
            message: Human-readable error message.
            details: Additional details about the error.
            original_exception: The original exception that caused this one.
        """
        super().__init__(
            message=message,
            code=ErrorCode.CONFIGURATION_ERROR,
            details=details,
            status_code=500,
            original_exception=original_exception,
        )
