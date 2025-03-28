# app/core/pagination/exceptions.py
from __future__ import annotations

"""Pagination-specific exceptions for the application.

This module defines exceptions related to pagination operations that integrate
with the application's exception system.
"""

from typing import Any, Dict, List, Optional, Union

from app.core.exceptions.base import (
    AppException,
    ErrorCategory,
    ErrorCode,
    ErrorSeverity,
)


class PaginationException(AppException):
    """Base exception for pagination errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.BUSINESS_LOGIC_ERROR,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        status_code: int = 400,
        original_exception: Optional[Exception] = None,
    ) -> None:
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.BUSINESS,
            original_exception=original_exception,
        )


class InvalidPaginationParamsException(PaginationException):
    """Exception raised when pagination parameters are invalid."""

    def __init__(
        self,
        message: str,
        params: Dict[str, Any],
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        error_details = details or {"params": params}
        super().__init__(
            message=message,
            code=ErrorCode.VALIDATION_ERROR,
            details=error_details,
            status_code=422,
            original_exception=original_exception,
        )


class InvalidCursorException(PaginationException):
    """Exception raised when a pagination cursor is invalid."""

    def __init__(
        self,
        message: str = "Invalid pagination cursor",
        cursor: Optional[str] = None,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        error_details = details or {}
        if cursor:
            error_details["cursor"] = cursor
        super().__init__(
            message=message,
            code=ErrorCode.VALIDATION_ERROR,
            details=error_details,
            status_code=422,
            original_exception=original_exception,
        )


class InvalidSortFieldException(PaginationException):
    """Exception raised when a sort field is invalid."""

    def __init__(
        self,
        field: str,
        model: str,
        message: Optional[str] = None,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        if message is None:
            message = f"Invalid sort field: {field} for model {model}"
        error_details = details or {"field": field, "model": model}
        super().__init__(
            message=message,
            code=ErrorCode.VALIDATION_ERROR,
            details=error_details,
            status_code=422,
            original_exception=original_exception,
        )
