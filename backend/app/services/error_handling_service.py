# /backend/app/services/error_handling_service.py
from __future__ import annotations

import traceback
from typing import Any, Dict, Optional, Type, cast

from app.core.exceptions import (
    AppException,
    BusinessLogicException,
    DatabaseException,
    ErrorCode,
    ErrorResponse,
    ValidationException
)
from app.core.logging import get_logger
from app.services.interfaces import ServiceInterface

logger = get_logger("app.services.error_handling_service")

class ErrorHandlingService:
    """Service for centralized error handling.
    
    This service provides standardized error handling across the application,
    with consistent error responses and logging.
    """
    
    def __init__(self) -> None:
        """Initialize the error handling service."""
        self.logger = logger
        
    async def initialize(self) -> None:
        """Initialize service resources."""
        self.logger.debug("Initializing error handling service")
        
    async def shutdown(self) -> None:
        """Release service resources."""
        self.logger.debug("Shutting down error handling service")
        
    def handle_exception(
        self, 
        exception: Exception, 
        request_id: Optional[str] = None
    ) -> ErrorResponse:
        """Handle an exception and return a standardized error response.
        
        Args:
            exception: The exception to handle
            request_id: Request ID for logging and tracking
            
        Returns:
            ErrorResponse: Standardized error response
        """
        if isinstance(exception, AppException):
            # Handle application exceptions
            self.logger.warning(
                f"Application exception: {str(exception)}",
                exc_info=exception,
                request_id=request_id,
                error_code=getattr(exception, "code", ErrorCode.UNKNOWN_ERROR),
            )
            return exception.to_response(request_id)
        else:
            # Handle unexpected exceptions
            self.logger.error(
                f"Unexpected exception: {str(exception)}",
                exc_info=exception,
                request_id=request_id,
            )
            return ErrorResponse(
                success=False,
                message="An unexpected error occurred",
                code=ErrorCode.UNKNOWN_ERROR,
                data=None,
                details=[{
                    "loc": ["server"],
                    "msg": str(exception),
                    "type": exception.__class__.__name__,
                }],
                meta={
                    "request_id": request_id
                },
                timestamp=None,
            )
            
    def create_validation_error(
        self, 
        field: str, 
        message: str, 
        error_type: str = "validation_error"
    ) -> ValidationException:
        """Create a validation error exception.
        
        Args:
            field: Field with the error
            message: Error message
            error_type: Type of error
            
        Returns:
            ValidationException: Validation error exception
        """
        return ValidationException(
            f"Validation error: {message}",
            code=ErrorCode.VALIDATION_ERROR,
            details={
                "errors": [{
                    "loc": field.split("."),
                    "msg": message,
                    "type": error_type,
                }]
            },
            status_code=400,
        )
        
    def create_business_logic_error(
        self, 
        message: str, 
        details: Optional[Dict[str, Any]] = None
    ) -> BusinessLogicException:
        """Create a business logic error exception.
        
        Args:
            message: Error message
            details: Additional error details
            
        Returns:
            BusinessLogicException: Business logic error exception
        """
        return BusinessLogicException(
            message,
            code=ErrorCode.BUSINESS_LOGIC_ERROR,
            details=details or {},
            status_code=400,
        )
        
    def create_database_error(
        self, 
        message: str, 
        original_error: Optional[Exception] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> DatabaseException:
        """Create a database error exception.
        
        Args:
            message: Error message
            original_error: Original exception
            details: Additional error details
            
        Returns:
            DatabaseException: Database error exception
        """
        error_details = details or {}
        if original_error:
            error_details["original_error"] = str(original_error)
            error_details["traceback"] = traceback.format_exc()
            
        return DatabaseException(
            message,
            code=ErrorCode.DATABASE_ERROR,
            details=error_details,
            status_code=500,
        )
