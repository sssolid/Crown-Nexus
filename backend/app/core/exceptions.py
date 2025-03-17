# /backend/app/core/exceptions.py
from __future__ import annotations

import logging
import sys
import traceback
from enum import Enum
from typing import Any, Dict, List, Optional, Type, Union, cast

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator

from app.core.logging import get_logger

logger = get_logger("app.core.exceptions")

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
    """Severity levels for errors.
    
    These levels help categorize errors by their impact and urgency.
    """
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class ErrorCategory(str, Enum):
    """Categories for errors.
    
    These categories help group errors by their source or nature.
    """
    VALIDATION = "validation"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    RESOURCE = "resource"
    DATABASE = "database"
    NETWORK = "network"
    EXTERNAL = "external"
    BUSINESS = "business"
    SECURITY = "security"
    DATA = "data"
    SYSTEM = "system"
    UNKNOWN = "unknown"

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

class ValidationException(AppException):
    """Exception raised for validation errors.
    
    This exception is used when input data fails validation checks.
    """
    def __init__(
        self,
        message: str,
        code: Union[str, ErrorCode] = ErrorCode.VALIDATION_ERROR,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the validation exception.
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
            status_code: HTTP status code
            original_exception: Original exception
        """
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.VALIDATION,
            original_exception=original_exception
        )

class ResourceNotFoundException(AppException):
    """Exception raised when a resource is not found.
    
    This exception is used when a requested resource doesn't exist.
    """
    def __init__(
        self,
        message: str,
        code: Union[str, ErrorCode] = ErrorCode.RESOURCE_NOT_FOUND,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = status.HTTP_404_NOT_FOUND,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the resource not found exception.
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
            status_code: HTTP status code
            original_exception: Original exception
        """
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.RESOURCE,
            original_exception=original_exception
        )

class ResourceAlreadyExistsException(AppException):
    """Exception raised when a resource already exists.
    
    This exception is used when attempting to create a resource that already exists.
    """
    def __init__(
        self,
        message: str,
        code: Union[str, ErrorCode] = ErrorCode.RESOURCE_ALREADY_EXISTS,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = status.HTTP_409_CONFLICT,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the resource already exists exception.
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
            status_code: HTTP status code
            original_exception: Original exception
        """
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.RESOURCE,
            original_exception=original_exception
        )

class BadRequestException(AppException):
    """Exception raised for bad requests.
    
    This exception is used when a request is malformed or invalid.
    """
    def __init__(
        self,
        message: str,
        code: Union[str, ErrorCode] = ErrorCode.BAD_REQUEST,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the bad request exception.
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
            status_code: HTTP status code
            original_exception: Original exception
        """
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.VALIDATION,
            original_exception=original_exception
        )

class AuthenticationException(AppException):
    """Exception raised for authentication errors.
    
    This exception is used when authentication fails.
    """
    def __init__(
        self,
        message: str,
        code: Union[str, ErrorCode] = ErrorCode.AUTHENTICATION_FAILED,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the authentication exception.
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
            status_code: HTTP status code
            original_exception: Original exception
        """
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.AUTHENTICATION,
            original_exception=original_exception
        )

class PermissionDeniedException(AppException):
    """Exception raised for permission errors.
    
    This exception is used when a user doesn't have permission to perform an action.
    """
    def __init__(
        self,
        message: str,
        code: Union[str, ErrorCode] = ErrorCode.PERMISSION_DENIED,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = status.HTTP_403_FORBIDDEN,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the permission denied exception.
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
            status_code: HTTP status code
            original_exception: Original exception
        """
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.AUTHORIZATION,
            original_exception=original_exception
        )

class DatabaseException(AppException):
    """Exception raised for database errors.
    
    This exception is used when a database operation fails.
    """
    def __init__(
        self,
        message: str,
        code: Union[str, ErrorCode] = ErrorCode.DATABASE_ERROR,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the database exception.
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
            status_code: HTTP status code
            original_exception: Original exception
        """
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.DATABASE,
            original_exception=original_exception
        )

class DataIntegrityException(DatabaseException):
    """Exception raised for data integrity errors.
    
    This exception is used when a database constraint is violated.
    """
    def __init__(
        self,
        message: str,
        code: Union[str, ErrorCode] = ErrorCode.DATA_INTEGRITY_ERROR,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = status.HTTP_409_CONFLICT,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the data integrity exception.
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
            status_code: HTTP status code
            original_exception: Original exception
        """
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.DATABASE,
            original_exception=original_exception
        )

class TransactionException(DatabaseException):
    """Exception raised for transaction errors.
    
    This exception is used when a database transaction fails.
    """
    def __init__(
        self,
        message: str,
        code: Union[str, ErrorCode] = ErrorCode.TRANSACTION_FAILED,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the transaction exception.
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
            status_code: HTTP status code
            original_exception: Original exception
        """
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.DATABASE,
            original_exception=original_exception
        )

class NetworkException(AppException):
    """Exception raised for network errors.
    
    This exception is used when a network operation fails.
    """
    def __init__(
        self,
        message: str,
        code: Union[str, ErrorCode] = ErrorCode.NETWORK_ERROR,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = status.HTTP_503_SERVICE_UNAVAILABLE,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the network exception.
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
            status_code: HTTP status code
            original_exception: Original exception
        """
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.NETWORK,
            original_exception=original_exception
        )

class TimeoutException(NetworkException):
    """Exception raised for timeout errors.
    
    This exception is used when a network operation times out.
    """
    def __init__(
        self,
        message: str,
        code: Union[str, ErrorCode] = ErrorCode.TIMEOUT_ERROR,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = status.HTTP_504_GATEWAY_TIMEOUT,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the timeout exception.
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
            status_code: HTTP status code
            original_exception: Original exception
        """
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.NETWORK,
            original_exception=original_exception
        )

class ExternalServiceException(AppException):
    """Exception raised for external service errors.
    
    This exception is used when an external service call fails.
    """
    def __init__(
        self,
        message: str,
        code: Union[str, ErrorCode] = ErrorCode.EXTERNAL_SERVICE_ERROR,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = status.HTTP_502_BAD_GATEWAY,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the external service exception.
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
            status_code: HTTP status code
            original_exception: Original exception
        """
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.EXTERNAL,
            original_exception=original_exception
        )

class RateLimitException(ExternalServiceException):
    """Exception raised for rate limit errors.
    
    This exception is used when an external service rate limit is exceeded.
    """
    def __init__(
        self,
        message: str,
        code: Union[str, ErrorCode] = ErrorCode.RATE_LIMIT_EXCEEDED,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = status.HTTP_429_TOO_MANY_REQUESTS,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the rate limit exception.
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
            status_code: HTTP status code
            original_exception: Original exception
        """
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.EXTERNAL,
            original_exception=original_exception
        )

class ServiceUnavailableException(ExternalServiceException):
    """Exception raised when an external service is unavailable.
    
    This exception is used when an external service is temporarily unavailable.
    """
    def __init__(
        self,
        message: str,
        code: Union[str, ErrorCode] = ErrorCode.SERVICE_UNAVAILABLE,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = status.HTTP_503_SERVICE_UNAVAILABLE,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the service unavailable exception.
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
            status_code: HTTP status code
            original_exception: Original exception
        """
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.EXTERNAL,
            original_exception=original_exception
        )

class BusinessLogicException(AppException):
    """Exception raised for business logic errors.
    
    This exception is used when a business rule is violated.
    """
    def __init__(
        self,
        message: str,
        code: Union[str, ErrorCode] = ErrorCode.BUSINESS_LOGIC_ERROR,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the business logic exception.
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
            status_code: HTTP status code
            original_exception: Original exception
        """
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.BUSINESS,
            original_exception=original_exception
        )

class InvalidStateException(BusinessLogicException):
    """Exception raised for invalid state errors.
    
    This exception is used when an operation is attempted in an invalid state.
    """
    def __init__(
        self,
        message: str,
        code: Union[str, ErrorCode] = ErrorCode.INVALID_STATE_ERROR,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = status.HTTP_409_CONFLICT,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the invalid state exception.
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
            status_code: HTTP status code
            original_exception: Original exception
        """
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.BUSINESS,
            original_exception=original_exception
        )

class OperationNotAllowedException(BusinessLogicException):
    """Exception raised when an operation is not allowed.
    
    This exception is used when an operation is not allowed due to business rules.
    """
    def __init__(
        self,
        message: str,
        code: Union[str, ErrorCode] = ErrorCode.OPERATION_NOT_ALLOWED,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = status.HTTP_403_FORBIDDEN,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the operation not allowed exception.
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
            status_code: HTTP status code
            original_exception: Original exception
        """
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.WARNING,
            category=ErrorCategory.BUSINESS,
            original_exception=original_exception
        )

class ConfigurationException(AppException):
    """Exception raised for configuration errors.
    
    This exception is used when there's an issue with application configuration.
    """
    def __init__(
        self,
        message: str,
        code: Union[str, ErrorCode] = ErrorCode.CONFIGURATION_ERROR,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the configuration exception.
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
            status_code: HTTP status code
            original_exception: Original exception
        """
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.SYSTEM,
            original_exception=original_exception
        )

# Exception handler functions

async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle AppException instances.

    Args:
        request: FastAPI request
        exc: AppException instance

    Returns:
        JSONResponse: JSON response with error details
    """
    # Log the exception
    exc.log(getattr(request.state, "request_id", None))
    
    # Generate error response
    error_response = exc.to_response(getattr(request.state, "request_id", None))
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict(),
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle FastAPI's RequestValidationError.

    Args:
        request: FastAPI request
        exc: RequestValidationError instance

    Returns:
        JSONResponse: JSON response with validation error details
    """
    # Log the exception
    logger.warning(
        f"Validation error: {str(exc)}",
        exc_info=exc,
        request_id=getattr(request.state, "request_id", None),
    )
    
    # Format error details
    error_details = []
    for error in exc.errors():
        error_details.append({
            "loc": list(error["loc"]),
            "msg": error["msg"],
            "type": error["type"],
        })
    
    # Create error response
    error_response = ErrorResponse(
        success=False,
        message="Validation error",
        code=ErrorCode.VALIDATION_ERROR,
        data=None,
        details=error_details,
        meta={
            "request_id": getattr(request.state, "request_id", None)
        },
        timestamp=None,
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.dict(),
    )

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle FastAPI's HTTPException.

    Args:
        request: FastAPI request
        exc: HTTPException instance

    Returns:
        JSONResponse: JSON response with error details
    """
    # Log the exception
    logger.warning(
        f"HTTP exception: {exc.detail}",
        exc_info=exc,
        request_id=getattr(request.state, "request_id", None),
        status_code=exc.status_code,
    )
    
    # Map HTTP status code to error code
    error_code = None
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        error_code = ErrorCode.RESOURCE_NOT_FOUND
    elif exc.status_code == status.HTTP_401_UNAUTHORIZED:
        error_code = ErrorCode.AUTHENTICATION_FAILED
    elif exc.status_code == status.HTTP_403_FORBIDDEN:
        error_code = ErrorCode.PERMISSION_DENIED
    elif exc.status_code == status.HTTP_409_CONFLICT:
        error_code = ErrorCode.RESOURCE_ALREADY_EXISTS
    else:
        error_code = ErrorCode.UNKNOWN_ERROR
    
    # Create error response
    error_response = ErrorResponse(
        success=False,
        message=str(exc.detail),
        code=error_code,
        data=None,
        details=[{
            "loc": ["server"],
            "msg": str(exc.detail),
            "type": error_code.lower(),
        }],
        meta={
            "request_id": getattr(request.state, "request_id", None)
        },
        timestamp=None,
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict(),
        headers=exc.headers,
    )

async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unhandled exceptions.

    Args:
        request: FastAPI request
        exc: Unhandled exception

    Returns:
        JSONResponse: JSON response with error details
    """
    # Log the exception
    logger.error(
        f"Unhandled exception: {str(exc)}",
        exc_info=exc,
        request_id=getattr(request.state, "request_id", None),
    )
    
    # Create error response
    error_response = ErrorResponse(
        success=False,
        message="An unexpected error occurred",
        code=ErrorCode.UNKNOWN_ERROR,
        data=None,
        details=[{
            "loc": ["server"],
            "msg": str(exc),
            "type": "unknown_error",
        }],
        meta={
            "request_id": getattr(request.state, "request_id", None)
        },
        timestamp=None,
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.dict(),
    )