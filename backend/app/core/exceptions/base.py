# app/core/exceptions/base.py
from __future__ import annotations

"""
Base exception system for the application.

This module defines the core exception types, error codes, and response models
used throughout the application. It provides a consistent foundation for error
handling and reporting.
"""

from app.logging import get_logger
import traceback
import logging
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator

from app.logging.context import get_logger

logger = get_logger("app.core.exceptions")


class ErrorCategory(str, Enum):
    """Categories of errors in the application."""

    VALIDATION = "validation"
    AUTH = "auth"
    RESOURCE = "resource"
    SYSTEM = "system"
    BUSINESS = "business"


class ErrorCode(str, Enum):
    """Specific error codes for different error scenarios."""

    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    RESOURCE_ALREADY_EXISTS = "RESOURCE_ALREADY_EXISTS"
    AUTHENTICATION_FAILED = "AUTHENTICATION_FAILED"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    BAD_REQUEST = "BAD_REQUEST"
    BUSINESS_LOGIC_ERROR = "BUSINESS_LOGIC_ERROR"
    INVALID_STATE = "INVALID_STATE"
    OPERATION_NOT_ALLOWED = "OPERATION_NOT_ALLOWED"
    DATABASE_ERROR = "DATABASE_ERROR"
    NETWORK_ERROR = "NETWORK_ERROR"
    SERVICE_ERROR = "SERVICE_ERROR"
    SERVER_ERROR = "SERVER_ERROR"
    CONFIGURATION_ERROR = "CONFIGURATION_ERROR"
    SECURITY_ERROR = "SECURITY_ERROR"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


class ErrorSeverity(str, Enum):
    """Severity levels for errors."""

    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ErrorDetail(BaseModel):
    """Detailed information about a specific error."""

    loc: List[str] = Field(..., description="Error location (path to the error)")
    msg: str = Field(..., description="Error message")
    type: str = Field(..., description="Error type code")


class ErrorResponse(BaseModel):
    """Standardized error response model."""

    success: bool = Field(False, description="Success flag (always False for errors)")
    message: str = Field(..., description="Human-readable error message")
    code: str = Field(..., description="Error code")
    data: Optional[Any] = Field(None, description="Additional error data")
    details: List[ErrorDetail] = Field([], description="Detailed error information")
    meta: Dict[str, Any] = Field(default_factory=dict, description="Metadata")
    timestamp: Optional[str] = Field(None, description="Error timestamp")

    @field_validator("details", mode="before")
    @classmethod
    def validate_details(cls, v: Any) -> List[ErrorDetail]:
        """
        Validate and transform error details.

        Args:
            v: The input value to validate

        Returns:
            Processed list of error details
        """
        if isinstance(v, dict) and "errors" in v:
            return v["errors"]
        elif isinstance(v, list):
            return v
        elif v is None:
            return []
        return [{"loc": ["unknown"], "msg": str(v), "type": "unknown"}]


class AppException(Exception):
    """
    Base exception class for application exceptions.

    Provides consistent error handling, formatting, and logging for all
    application exceptions.
    """

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.UNKNOWN_ERROR,
        details: Any = None,
        status_code: int = 500,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        category: ErrorCategory = ErrorCategory.SYSTEM,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """
        Initialize the exception.

        Args:
            message: Human-readable error message
            code: Error code identifier
            details: Additional details about the error
            status_code: HTTP status code for the error
            severity: Severity level of the error
            category: Category of the error
            original_exception: Original exception that caused this one
        """
        self.message = message
        self.code = code
        self.details = details or {}
        self.status_code = status_code
        self.severity = severity
        self.category = category
        self.original_exception = original_exception

        # Add original exception info if available
        if original_exception:
            if isinstance(self.details, dict):
                self.details["original_error"] = str(original_exception)
                self.details["traceback"] = traceback.format_exception(
                    type(original_exception),
                    original_exception,
                    original_exception.__traceback__,
                )

        super().__init__(self.message)

    def to_response(self, request_id: Optional[str] = None) -> ErrorResponse:
        """
        Convert the exception to a standardized error response.

        Args:
            request_id: Optional request ID to include in the response

        Returns:
            Formatted error response object
        """
        error_details = []

        if isinstance(self.details, list):
            error_details = self.details
        elif isinstance(self.details, dict):
            if "errors" in self.details:
                error_details = self.details["errors"]
            else:
                for key, value in self.details.items():
                    if key not in ["original_error", "traceback"]:
                        error_details.append(
                            {
                                "loc": key.split("."),
                                "msg": str(value),
                                "type": str(self.code).lower(),
                            }
                        )
        else:
            error_details = [
                {"loc": ["server"], "msg": self.message, "type": str(self.code).lower()}
            ]

        # Add metadata
        meta = {"request_id": request_id} if request_id else {}
        meta["severity"] = self.severity
        meta["category"] = self.category

        return ErrorResponse(
            success=False,
            message=self.message,
            code=str(self.code),
            data=None,
            details=error_details,
            meta=meta,
            timestamp=None,
        )

    def log(self, request_id: Optional[str] = None) -> None:
        """
        Log the exception with appropriate severity and context.

        Args:
            request_id: Optional request ID for correlation
        """
        log_level = (
            logging.WARNING if self.severity == ErrorSeverity.WARNING else logging.ERROR
        )

        context = {
            "status_code": self.status_code,
            "error_code": str(self.code),
            "error_category": self.category.value,
        }

        if request_id:
            context["request_id"] = request_id

        if self.original_exception:
            logger.log(
                log_level,
                f"{self.message} (original error: {str(self.original_exception)})",
                exc_info=self.original_exception,
                **context,
            )
        else:
            logger.log(log_level, self.message, **context)
