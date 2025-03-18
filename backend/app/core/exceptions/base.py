from __future__ import annotations
import logging
import sys
import traceback
from enum import Enum
from typing import Any, Dict, List, Optional, Type, Union, cast
from pydantic import BaseModel, Field, validator
from fastapi import HTTPException, Request, status

from pydantic import BaseModel, Field

from app.core.logging import get_logger

logger = get_logger("app.core.exceptions")

class ErrorCategory(str, Enum):
    """Categories for errors."""
    VALIDATION = 'validation'
    AUTHENTICATION = 'authentication'
    AUTHORIZATION = 'authorization'
    RESOURCE = 'resource'
    DATABASE = 'database'
    NETWORK = 'network'
    EXTERNAL = 'external'
    BUSINESS = 'business'
    SECURITY = 'security'
    DATA = 'data'
    SYSTEM = 'system'
    UNKNOWN = 'unknown'

class ErrorCode(str, Enum):
    """Error codes for standardized error responses.

    These codes provide standardized identifiers for error types,
    allowing clients to handle errors consistently.
    """
    # General errors
    UNKNOWN_ERROR = "UNKNOWN_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    RESOURCE_ALREADY_EXISTS = "RESOURCE_ALREADY_EXISTS"
    BAD_REQUEST = "BAD_REQUEST"

    # Authentication errors
    AUTHENTICATION_FAILED = "AUTHENTICATION_FAILED"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    INVALID_TOKEN = "INVALID_TOKEN"
    USER_NOT_ACTIVE = "USER_NOT_ACTIVE"

    # Database errors
    DATABASE_ERROR = "DATABASE_ERROR"
    TRANSACTION_FAILED = "TRANSACTION_FAILED"
    DATA_INTEGRITY_ERROR = "DATA_INTEGRITY_ERROR"

    # Network errors
    NETWORK_ERROR = "NETWORK_ERROR"
    TIMEOUT_ERROR = "TIMEOUT_ERROR"
    CONNECTION_ERROR = "CONNECTION_ERROR"

    # External service errors
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    EXTERNAL_DEPENDENCY_ERROR = "EXTERNAL_DEPENDENCY_ERROR"

    # Business logic errors
    BUSINESS_LOGIC_ERROR = "BUSINESS_LOGIC_ERROR"
    INVALID_STATE_ERROR = "INVALID_STATE_ERROR"
    OPERATION_NOT_ALLOWED = "OPERATION_NOT_ALLOWED"

    # Security errors
    SECURITY_ERROR = "SECURITY_ERROR"
    ACCESS_DENIED = "ACCESS_DENIED"
    CSRF_ERROR = "CSRF_ERROR"

    # Data errors
    DATA_ERROR = "DATA_ERROR"
    SERIALIZATION_ERROR = "SERIALIZATION_ERROR"
    DESERIALIZATION_ERROR = "DESERIALIZATION_ERROR"

    # System errors
    SYSTEM_ERROR = "SYSTEM_ERROR"
    CONFIGURATION_ERROR = "CONFIGURATION_ERROR"
    DEPENDENCY_ERROR = "DEPENDENCY_ERROR"

class ErrorSeverity(str, Enum):
    """Severity levels for errors."""
    DEBUG = 'debug'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    CRITICAL = 'critical'

class ErrorDetail(BaseModel):
    """Detailed error information for API responses.

    This model provides structured error details, including location,
    message, and error type.
    """
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

    @validator("details", pre=True)
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

    This class provides the foundation for a structured exception hierarchy,
    with standardized error codes, messages, and HTTP status codes.
    """
    def __init__(
        self,
        message: str,
        code: Union[str, ErrorCode] = ErrorCode.UNKNOWN_ERROR,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        category: ErrorCategory = ErrorCategory.UNKNOWN,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the exception with customizable properties.

        Args:
            message: Human-readable error message
            code: Error code
            details: Detailed error information
            status_code: HTTP status code
            severity: Error severity level
            category: Error category
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
                original_exception.__traceback__
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

        if "errors" in self.details:
            # Use provided errors list
            error_details = self.details["errors"]
        elif self.details:
            # Convert details to error detail format
            for key, value in self.details.items():
                if key not in ["original_error", "traceback"]:
                    error_details.append({
                        "loc": key.split("."),
                        "msg": str(value),
                        "type": str(self.code).lower()
                    })
        else:
            # Create default error detail
            error_details = [{
                "loc": ["server"],
                "msg": self.message,
                "type": str(self.code).lower()
            }]

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
            timestamp=None  # Will be filled by middleware
        )

    def log(self, request_id: Optional[str] = None) -> None:
        """Log the exception with appropriate severity level.

        Args:
            request_id: Request ID for tracking
        """
        log_method = getattr(logger, self.severity.value, logger.error)

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
            log_method(
                f"{self.message} (original error: {str(self.original_exception)})",
                exc_info=self.original_exception,
                **context
            )
        else:
            log_method(self.message, **context)
