# app/core/exceptions.py
from __future__ import annotations

import traceback
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class ErrorCode(str, Enum):
    """Error codes for standardized error responses."""

    # Generic errors
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
    
    # External service errors
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    
    # Business logic errors
    BUSINESS_LOGIC_ERROR = "BUSINESS_LOGIC_ERROR"


class ErrorDetail(BaseModel):
    """Detailed error information for API responses."""

    loc: List[str] = Field(default_factory=list, description="Location of the error")
    msg: str = Field(description="Error message")
    type: str = Field(description="Error type")


class ErrorResponse(BaseModel):
    """Standardized error response model."""

    code: ErrorCode = Field(description="Error code")
    message: str = Field(description="Human-readable error message")
    details: Optional[List[ErrorDetail]] = Field(default=None, description="Detailed error information")
    request_id: Optional[str] = Field(default=None, description="Request ID for tracking")


class AppException(Exception):
    """Base exception for all application-specific exceptions."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    code: ErrorCode = ErrorCode.UNKNOWN_ERROR
    message: str = "An unexpected error occurred"
    details: Optional[List[ErrorDetail]] = None

    def __init__(
        self,
        message: Optional[str] = None,
        code: Optional[ErrorCode] = None,
        details: Optional[List[ErrorDetail]] = None,
        status_code: Optional[int] = None,
    ) -> None:
        """Initialize the exception with customizable properties.
        
        Args:
            message: Human-readable error message
            code: Error code
            details: Detailed error information
            status_code: HTTP status code
        """
        self.message = message or self.message
        self.code = code or self.code
        self.details = details or self.details
        if status_code is not None:
            self.status_code = status_code
        super().__init__(self.message)

    def to_response(self, request_id: Optional[str] = None) -> ErrorResponse:
        """Convert exception to a standardized error response.
        
        Args:
            request_id: Request ID for tracking
            
        Returns:
            Standardized error response
        """
        return ErrorResponse(
            code=self.code,
            message=self.message,
            details=self.details,
            request_id=request_id,
        )


class ValidationException(AppException):
    """Exception raised for validation errors."""

    status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY
    code: ErrorCode = ErrorCode.VALIDATION_ERROR
    message: str = "Validation error"


class PermissionDeniedException(AppException):
    """Exception raised for permission errors."""

    status_code: int = status.HTTP_403_FORBIDDEN
    code: ErrorCode = ErrorCode.PERMISSION_DENIED
    message: str = "Permission denied"


class AuthenticationException(AppException):
    """Exception raised for authentication errors."""

    status_code: int = status.HTTP_401_UNAUTHORIZED
    code: ErrorCode = ErrorCode.AUTHENTICATION_FAILED
    message: str = "Authentication failed"


class ResourceNotFoundException(AppException):
    """Exception raised when a resource is not found."""

    status_code: int = status.HTTP_404_NOT_FOUND
    code: ErrorCode = ErrorCode.RESOURCE_NOT_FOUND
    message: str = "Resource not found"


class ResourceAlreadyExistsException(AppException):
    """Exception raised when a resource already exists."""

    status_code: int = status.HTTP_409_CONFLICT
    code: ErrorCode = ErrorCode.RESOURCE_ALREADY_EXISTS
    message: str = "Resource already exists"


class BadRequestException(AppException):
    """Exception raised for bad requests."""

    status_code: int = status.HTTP_400_BAD_REQUEST
    code: ErrorCode = ErrorCode.BAD_REQUEST
    message: str = "Bad request"


class DatabaseException(AppException):
    """Exception raised for database errors."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    code: ErrorCode = ErrorCode.DATABASE_ERROR
    message: str = "Database error"


class ExternalServiceException(AppException):
    """Exception raised for external service errors."""

    status_code: int = status.HTTP_502_BAD_GATEWAY
    code: ErrorCode = ErrorCode.EXTERNAL_SERVICE_ERROR
    message: str = "External service error"


class BusinessLogicException(AppException):
    """Exception raised for business logic errors."""

    status_code: int = status.HTTP_400_BAD_REQUEST
    code: ErrorCode = ErrorCode.BUSINESS_LOGIC_ERROR
    message: str = "Business logic error"


# Exception handlers for FastAPI
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle AppException instances.
    
    Args:
        request: FastAPI request
        exc: AppException instance
        
    Returns:
        JSON response with error details
    """
    from app.core.logging import get_logger
    
    logger = get_logger("app.exception")
    
    # Get request ID from context if available
    request_id = getattr(request.state, "request_id", None)
    
    # Log the exception
    log_data = {
        "request_id": request_id,
        "error_code": exc.code,
        "status_code": exc.status_code,
        "message": exc.message,
        "path": request.url.path,
        "method": request.method,
    }
    
    if exc.status_code >= 500:
        logger.error(f"Application error: {exc.message}", extra=log_data)
        # Log traceback for server errors
        logger.debug(f"Traceback: {traceback.format_exc()}")
    else:
        logger.info(f"Client error: {exc.message}", extra=log_data)
    
    # Return standardized error response
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_response(request_id=request_id).dict(),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle FastAPI's RequestValidationError.
    
    Args:
        request: FastAPI request
        exc: RequestValidationError instance
        
    Returns:
        JSON response with validation error details
    """
    from app.core.logging import get_logger
    
    logger = get_logger("app.exception")
    
    # Get request ID from context if available
    request_id = getattr(request.state, "request_id", None)
    
    # Transform validation errors to our format
    details = []
    for error in exc.errors():
        details.append(
            ErrorDetail(
                loc=[str(loc) for loc in error["loc"]],
                msg=error["msg"],
                type=error["type"],
            )
        )
    
    # Create validation exception
    validation_exc = ValidationException(
        message="Validation error",
        details=details,
    )
    
    # Log the validation error
    log_data = {
        "request_id": request_id,
        "error_code": validation_exc.code,
        "status_code": validation_exc.status_code,
        "path": request.url.path,
        "method": request.method,
        "details": [detail.dict() for detail in details],
    }
    
    logger.info(f"Validation error", extra=log_data)
    
    # Return standardized error response
    return JSONResponse(
        status_code=validation_exc.status_code,
        content=validation_exc.to_response(request_id=request_id).dict(),
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle FastAPI's HTTPException.
    
    Args:
        request: FastAPI request
        exc: HTTPException instance
        
    Returns:
        JSON response with error details
    """
    from app.core.logging import get_logger
    
    logger = get_logger("app.exception")
    
    # Get request ID from context if available
    request_id = getattr(request.state, "request_id", None)
    
    # Map status code to error code
    code = ErrorCode.UNKNOWN_ERROR
    if exc.status_code == 401:
        code = ErrorCode.AUTHENTICATION_FAILED
    elif exc.status_code == 403:
        code = ErrorCode.PERMISSION_DENIED
    elif exc.status_code == 404:
        code = ErrorCode.RESOURCE_NOT_FOUND
    elif exc.status_code == 409:
        code = ErrorCode.RESOURCE_ALREADY_EXISTS
    elif exc.status_code == 422:
        code = ErrorCode.VALIDATION_ERROR
    elif 400 <= exc.status_code < 500:
        code = ErrorCode.BAD_REQUEST
    
    # Create app exception from HTTP exception
    app_exc = AppException(
        message=str(exc.detail),
        code=code,
        status_code=exc.status_code,
    )
    
    # Log the exception
    log_data = {
        "request_id": request_id,
        "error_code": app_exc.code,
        "status_code": app_exc.status_code,
        "path": request.url.path,
        "method": request.method,
    }
    
    if exc.status_code >= 500:
        logger.error(f"Application error: {app_exc.message}", extra=log_data)
    else:
        logger.info(f"Client error: {app_exc.message}", extra=log_data)
    
    # Return standardized error response
    return JSONResponse(
        status_code=app_exc.status_code,
        content=app_exc.to_response(request_id=request_id).dict(),
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unhandled exceptions.
    
    Args:
        request: FastAPI request
        exc: Unhandled exception
        
    Returns:
        JSON response with error details
    """
    from app.core.logging import get_logger
    
    logger = get_logger("app.exception")
    
    # Get request ID from context if available
    request_id = getattr(request.state, "request_id", None)
    
    # Create generic app exception
    app_exc = AppException(
        message="An unexpected error occurred",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
    
    # Log the exception with traceback
    log_data = {
        "request_id": request_id,
        "error_code": app_exc.code,
        "status_code": app_exc.status_code,
        "path": request.url.path,
        "method": request.method,
        "exception_type": exc.__class__.__name__,
        "exception_message": str(exc),
    }
    
    logger.error(f"Unhandled exception: {str(exc)}", extra=log_data)
    logger.debug(f"Traceback: {traceback.format_exc()}")
    
    # Return standardized error response
    return JSONResponse(
        status_code=app_exc.status_code,
        content=app_exc.to_response(request_id=request_id).dict(),
      )
