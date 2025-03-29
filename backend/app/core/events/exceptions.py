from __future__ import annotations

"""
Event system exceptions.

This module defines exceptions specific to the event system,
aligned with the application's exception hierarchy.
"""

from typing import Any, Dict, List, Optional, Union

from app.core.exceptions.base import (
    AppException,
    ErrorCategory,
    ErrorCode,
    ErrorSeverity,
)


class EventException(AppException):
    """Base exception for all event-related exceptions."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.SERVICE_ERROR,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        status_code: int = 500,
        original_exception: Optional[Exception] = None,
    ) -> None:
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.SYSTEM,
            original_exception=original_exception,
        )


class EventPublishException(EventException):
    """Exception raised when publishing an event fails."""

    def __init__(
        self,
        message: str,
        event_name: str,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        error_details = details or {}
        if isinstance(error_details, dict):
            error_details["event_name"] = event_name

        super().__init__(
            message=message,
            code=ErrorCode.SERVICE_ERROR,
            details=error_details,
            status_code=500,
            original_exception=original_exception,
        )


class EventHandlerException(EventException):
    """Exception raised when an event handler fails."""

    def __init__(
        self,
        message: str,
        event_name: str,
        handler_name: str,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        error_details = details or {}
        if isinstance(error_details, dict):
            error_details["event_name"] = event_name
            error_details["handler_name"] = handler_name

        super().__init__(
            message=message,
            code=ErrorCode.SERVICE_ERROR,
            details=error_details,
            status_code=500,
            original_exception=original_exception,
        )


class EventConfigurationException(EventException):
    """Exception raised when there's an error with event system configuration."""

    def __init__(
        self,
        message: str,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        super().__init__(
            message=message,
            code=ErrorCode.CONFIGURATION_ERROR,
            details=details,
            status_code=500,
            original_exception=original_exception,
        )


class EventBackendException(EventException):
    """Exception raised when there's an error with the event backend."""

    def __init__(
        self,
        message: str,
        backend_type: str,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        error_details = details or {}
        if isinstance(error_details, dict):
            error_details["backend_type"] = backend_type

        super().__init__(
            message=message,
            code=ErrorCode.SERVICE_ERROR,
            details=error_details,
            status_code=500,
            original_exception=original_exception,
        )


class EventServiceException(EventException):
    """Exception raised when there's an error with the event service."""

    def __init__(
        self,
        message: str,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        super().__init__(
            message=message,
            code=ErrorCode.SERVICE_ERROR,
            details=details,
            status_code=500,
            original_exception=original_exception,
        )
