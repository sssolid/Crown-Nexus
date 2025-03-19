# /backend/app/core/exceptions/base.py
from __future__ import annotations

import logging

"""Base exception system for the application.

This module defines the core exception types, error codes, and response models
used throughout the application. It provides a consistent foundation for error
handling and reporting.
"""

import traceback
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator

from app.core.logging import get_logger

logger = get_logger("app.core.exceptions")


class ErrorCategory(str, Enum):
    """Categories for different types of errors."""

    VALIDATION = "validation"  # Input validation errors
    AUTH = "auth"  # Authentication and authorization errors
    RESOURCE = "resource"  # Resource access and management errors
    SYSTEM = "system"  # System-level errors (DB, network, services)
    BUSINESS = "business"  # Business logic and domain rule errors


class ErrorCode(str, Enum):
    """Standardized error codes for application errors.

    These codes provide a consistent way to identify error types across
    the application, allowing clients to handle errors in a structured way.
    """

    # Resource errors
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    RESOURCE_ALREADY_EXISTS = "RESOURCE_ALREADY_EXISTS"

    # Auth errors
    AUTHENTICATION_FAILED = "AUTHENTICATION_FAILED"
    PERMISSION_DENIED = "PERMISSION_DENIED"

    # Validation errors
    VALIDATION_ERROR = "VALIDATION_ERROR"
    BAD_REQUEST = "BAD_REQUEST"

    # Business logic errors
    BUSINESS_LOGIC_ERROR = "BUSINESS_LOGIC_ERROR"
    INVALID_STATE = "INVALID_STATE"
    OPERATION_NOT_ALLOWED = "OPERATION_NOT_ALLOWED"

    # System errors
    DATABASE_ERROR = "DATABASE_ERROR"
    NETWORK_ERROR = "NETWORK_ERROR"
    SERVICE_ERROR = "SERVICE_ERROR"
    CONFIGURATION_ERROR = "CONFIGURATION_ERROR"
    SECURITY_ERROR = "SECURITY_ERROR"

    # Generic errors
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


class ErrorSeverity(str, Enum):
    """Severity levels for errors."""

    WARNING = "warning"  # Issues that need attention but aren't critical
    ERROR = "error"  # Serious errors that impact functionality
    CRITICAL = "critical"  # Critical failures requiring immediate attention


class ErrorDetail(BaseModel):
    """Detailed error information for API responses."""

    loc: List[str] = Field(..., description="Error location (path to the error)")
    msg: str = Field(..., description="Error message")
    type: str = Field(..., description="Error type code")


class ErrorResponse(BaseModel):
    """Standardized error response model.

    This model defines the structure of error responses returned by the API,
    providing consistent error information to clients.
    """

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
        """Validate and convert error details to proper format."""
        if isinstance(v, dict) and "errors" in v:
            return v["errors"]
        elif isinstance(v, list):
            return v
        elif v is None:
            return []
        return [{"loc": ["unknown"], "msg": str(v), "type": "unknown"}]


class AppException(Exception):
    """Base exception for all application-specific exceptions.

    This class provides the foundation for the application's exception hierarchy,
    with standardized error codes, messages, and HTTP status codes.
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
        """Initialize the exception with customizable properties.

        Args:
            message: Human-readable error message
            code: Error code from ErrorCode enum
            details: Additional error details or context
            status_code: HTTP status code to return
            severity: Error severity level
            category: Error category for classification
            original_exception: Original exception that caused this error
        """
        self.message = message
        self.code = code
        self.details = details or {}
        self.status_code = status_code
        self.severity = severity
        self.category = category
        self.original_exception = original_exception

        # Add traceback information if original exception is provided
        if original_exception:
            self.details["original_error"] = str(original_exception)
            self.details["traceback"] = traceback.format_exception(
                type(original_exception),
                original_exception,
                original_exception.__traceback__,
            )

        super().__init__(self.message)

    def to_response(self, request_id: Optional[str] = None) -> ErrorResponse:
        """Convert exception to a standardized error response.

        Args:
            request_id: Request ID for tracking

        Returns:
            ErrorResponse: Standardized error response
        """
        # Prepare error details
        error_details = []

        if isinstance(self.details, list):
            # Already formatted as error details
            error_details = self.details
        elif isinstance(self.details, dict):
            if "errors" in self.details:
                # Use provided errors list
                error_details = self.details["errors"]
            else:
                # Convert details to error detail format
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
            # Create default error detail
            error_details = [
                {"loc": ["server"], "msg": self.message, "type": str(self.code).lower()}
            ]

        # Create metadata
        meta = {"request_id": request_id} if request_id else {}
        meta["severity"] = self.severity
        meta["category"] = self.category

        # Return error response
        return ErrorResponse(
            success=False,
            message=self.message,
            code=str(self.code),
            data=None,
            details=error_details,
            meta=meta,
            timestamp=None,  # Will be filled by middleware
        )

    def log(self, request_id: Optional[str] = None) -> None:
        """Log the exception with appropriate severity level.

        Args:
            request_id: Request ID for tracking
        """
        log_level = (
            logging.WARNING if self.severity == ErrorSeverity.WARNING else logging.ERROR
        )

        # Prepare log context
        context = {
            "status_code": self.status_code,
            "error_code": str(self.code),
            "error_category": self.category.value,
        }

        if request_id:
            context["request_id"] = request_id

        # Log the error
        if self.original_exception:
            logger.log(
                log_level,
                f"{self.message} (original error: {str(self.original_exception)})",
                exc_info=self.original_exception,
                extra=context,
            )
        else:
            logger.log(log_level, self.message, extra=context)
