# app/services/error_handling_service.py
from __future__ import annotations

import inspect
import json
import sys
import traceback
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union, cast

from fastapi import HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app.core.exceptions import (
    AppException,
    BadRequestException,
    BusinessLogicException,
    DatabaseException,
    ErrorCategory,
    ErrorCode,
    ErrorDetail,
    ErrorResponse,
    ErrorSeverity,
    NetworkException,
    PermissionDeniedException,
    ResourceNotFoundException,
    SecurityException,
    ValidationException,
)
from app.core.logging import get_logger
from app.services.interfaces import ServiceInterface

logger = get_logger("app.services.error_handling_service")
F = TypeVar("F", bound=Callable[..., Any])


class ErrorContext(BaseModel):
    """Model for error context information."""

    request_id: Optional[str] = None
    user_id: Optional[str] = None
    path: Optional[str] = None
    method: Optional[str] = None
    component: Optional[str] = None
    operation: Optional[str] = None
    additional_data: Dict[str, Any] = Field(default_factory=dict)


class ErrorReporter:
    """Interface for error reporting implementations."""

    async def report_error(
        self,
        exception: Exception,
        context: Optional[ErrorContext] = None
    ) -> None:
        """Report an error to external monitoring system.

        Args:
            exception: The exception to report
            context: Optional error context
        """
        pass


class DefaultErrorReporter(ErrorReporter):
    """Default implementation of error reporter."""

    async def report_error(
        self,
        exception: Exception,
        context: Optional[ErrorContext] = None
    ) -> None:
        """Report an error using the default logger.

        Args:
            exception: The exception to report
            context: Optional error context
        """
        # Extract context information
        ctx = context or ErrorContext()

        # Determine log level based on exception type
        level = "error"
        if isinstance(exception, AppException):
            if exception.severity == ErrorSeverity.WARNING:
                level = "warning"
            elif exception.severity == ErrorSeverity.INFO:
                level = "info"
            elif exception.severity == ErrorSeverity.CRITICAL:
                level = "critical"
        elif isinstance(exception, (ValidationException, ResourceNotFoundException)):
            level = "warning"
        elif isinstance(exception, (DatabaseException, NetworkException)):
            level = "error"
        elif isinstance(exception, HTTPException) and exception.status_code < 500:
            level = "warning"

        # Build log context
        log_data = {
            "error_type": exception.__class__.__name__,
            "request_id": ctx.request_id,
            "user_id": ctx.user_id,
            "path": ctx.path,
            "method": ctx.method,
            "component": ctx.component,
            "operation": ctx.operation,
        }

        # Add additional data
        if ctx.additional_data:
            log_data.update(ctx.additional_data)

        # Get stack trace for non-AppExceptions
        if not isinstance(exception, AppException):
            log_data["traceback"] = traceback.format_exc()

        # Get error code if available
        if hasattr(exception, "code"):
            log_data["error_code"] = getattr(exception, "code")

        # Log with appropriate level
        log_func = getattr(logger, level)
        log_func(f"Error: {str(exception)}", **log_data)


class ErrorHandlingService:
    """Service for centralized error handling.

    Handles error reporting, formatting, and returning appropriate responses
    for different types of exceptions.
    """

    def __init__(self) -> None:
        """Initialize the error handling service."""
        self.logger = logger
        self.reporters: List[ErrorReporter] = [DefaultErrorReporter()]
        self.known_exceptions: Dict[str, Dict[str, Any]] = {}
        self._register_known_exceptions()

    async def initialize(self) -> None:
        """Initialize the error handling service."""
        self.logger.debug("Initializing error handling service")

    async def shutdown(self) -> None:
        """Shutdown the error handling service."""
        self.logger.debug("Shutting down error handling service")

    def _register_known_exceptions(self) -> None:
        """Register known exception types with their default settings."""
        # Map exception types to their default settings
        self.known_exceptions = {
            "ValidationException": {
                "code": ErrorCode.VALIDATION_ERROR,
                "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "severity": ErrorSeverity.WARNING,
                "category": ErrorCategory.VALIDATION,
            },
            "ResourceNotFoundException": {
                "code": ErrorCode.RESOURCE_NOT_FOUND,
                "status_code": status.HTTP_404_NOT_FOUND,
                "severity": ErrorSeverity.WARNING,
                "category": ErrorCategory.RESOURCE,
            },
            "PermissionDeniedException": {
                "code": ErrorCode.PERMISSION_DENIED,
                "status_code": status.HTTP_403_FORBIDDEN,
                "severity": ErrorSeverity.WARNING,
                "category": ErrorCategory.AUTHORIZATION,
            },
            "BadRequestException": {
                "code": ErrorCode.BAD_REQUEST,
                "status_code": status.HTTP_400_BAD_REQUEST,
                "severity": ErrorSeverity.WARNING,
                "category": ErrorCategory.VALIDATION,
            },
            "BusinessLogicException": {
                "code": ErrorCode.BUSINESS_LOGIC_ERROR,
                "status_code": status.HTTP_400_BAD_REQUEST,
                "severity": ErrorSeverity.WARNING,
                "category": ErrorCategory.BUSINESS,
            },
            "DatabaseException": {
                "code": ErrorCode.DATABASE_ERROR,
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "severity": ErrorSeverity.ERROR,
                "category": ErrorCategory.DATABASE,
            },
            "NetworkException": {
                "code": ErrorCode.NETWORK_ERROR,
                "status_code": status.HTTP_503_SERVICE_UNAVAILABLE,
                "severity": ErrorSeverity.ERROR,
                "category": ErrorCategory.NETWORK,
            },
            "SecurityException": {
                "code": ErrorCode.SECURITY_ERROR,
                "status_code": status.HTTP_403_FORBIDDEN,
                "severity": ErrorSeverity.WARNING,
                "category": ErrorCategory.SECURITY,
            },
        }

    def register_reporter(self, reporter: ErrorReporter) -> None:
        """Register an error reporter.

        Args:
            reporter: Error reporter to register
        """
        self.reporters.append(reporter)

    async def report_error(
        self,
        exception: Exception,
        context: Optional[ErrorContext] = None
    ) -> None:
        """Report an error to all registered reporters.

        Args:
            exception: The exception to report
            context: Optional error context
        """
        for reporter in self.reporters:
            try:
                await reporter.report_error(exception, context)
            except Exception as e:
                self.logger.error(f"Error reporter failed: {str(e)}", exc_info=True)

    def handle_exception(
        self,
        exception: Exception,
        request_id: Optional[str] = None,
        context: Optional[ErrorContext] = None
    ) -> ErrorResponse:
        """Handle and format an exception.

        Args:
            exception: The exception to handle
            request_id: Optional request ID
            context: Optional error context

        Returns:
            Formatted error response
        """
        # For AppExceptions, just use the built-in to_response method
        if isinstance(exception, AppException):
            return exception.to_response(request_id)

        # For HTTPExceptions, convert to an appropriate AppException
        if isinstance(exception, HTTPException):
            return self._convert_http_exception(exception, request_id)

        # For all other exceptions, create a generic error response
        error_type = exception.__class__.__name__
        error_details = []

        # Create a generic error detail
        error_details.append(
            ErrorDetail(
                loc=["server"],
                msg=str(exception),
                type="server_error"
            )
        )

        # Get stack trace
        tb = traceback.format_exc()

        # Create metadata
        meta = {"request_id": request_id} if request_id else {}
        meta["error_type"] = error_type
        meta["severity"] = ErrorSeverity.ERROR
        meta["category"] = ErrorCategory.UNKNOWN

        # Create response
        response = ErrorResponse(
            success=False,
            message=f"An unexpected error occurred: {str(exception)}",
            code=ErrorCode.UNKNOWN_ERROR,
            data=None,
            details=error_details,
            meta=meta,
            timestamp=datetime.utcnow().isoformat()
        )

        return response

    def _convert_http_exception(
        self,
        exception: HTTPException,
        request_id: Optional[str] = None
    ) -> ErrorResponse:
        """Convert a FastAPI HTTPException to an ErrorResponse.

        Args:
            exception: The HTTP exception to convert
            request_id: Optional request ID

        Returns:
            Converted error response
        """
        error_code = None
        category = ErrorCategory.UNKNOWN
        severity = ErrorSeverity.WARNING

        # Determine error code and category based on status code
        if exception.status_code == status.HTTP_404_NOT_FOUND:
            error_code = ErrorCode.RESOURCE_NOT_FOUND
            category = ErrorCategory.RESOURCE
        elif exception.status_code == status.HTTP_401_UNAUTHORIZED:
            error_code = ErrorCode.AUTHENTICATION_FAILED
            category = ErrorCategory.AUTHENTICATION
        elif exception.status_code == status.HTTP_403_FORBIDDEN:
            error_code = ErrorCode.PERMISSION_DENIED
            category = ErrorCategory.AUTHORIZATION
        elif exception.status_code == status.HTTP_409_CONFLICT:
            error_code = ErrorCode.RESOURCE_ALREADY_EXISTS
            category = ErrorCategory.RESOURCE
        elif exception.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            error_code = ErrorCode.VALIDATION_ERROR
            category = ErrorCategory.VALIDATION
        elif exception.status_code >= 500:
            error_code = ErrorCode.SYSTEM_ERROR
            category = ErrorCategory.SYSTEM
            severity = ErrorSeverity.ERROR
        else:
            error_code = ErrorCode.BAD_REQUEST
            category = ErrorCategory.VALIDATION

        # Create error details
        error_details = [
            ErrorDetail(
                loc=["server"],
                msg=str(exception.detail),
                type=error_code.value.lower()
            )
        ]

        # Create metadata
        meta = {"request_id": request_id} if request_id else {}
        meta["severity"] = severity
        meta["category"] = category

        # Create response
        response = ErrorResponse(
            success=False,
            message=str(exception.detail),
            code=error_code,
            data=None,
            details=error_details,
            meta=meta,
            timestamp=datetime.utcnow().isoformat()
        )

        return response

    def create_error_response(
        self,
        message: str,
        code: ErrorCode,
        status_code: int,
        details: Optional[List[Dict[str, Any]]] = None,
        request_id: Optional[str] = None
    ) -> JSONResponse:
        """Create a JSON error response.

        Args:
            message: Error message
            code: Error code
            status_code: HTTP status code
            details: Optional error details
            request_id: Optional request ID

        Returns:
            JSON response with error details
        """
        error_details = []

        if details:
            for detail in details:
                error_details.append(
                    ErrorDetail(
                        loc=detail.get("loc", ["server"]),
                        msg=detail.get("msg", message),
                        type=detail.get("type", code.value.lower())
                    )
                )
        else:
            error_details.append(
                ErrorDetail(
                    loc=["server"],
                    msg=message,
                    type=code.value.lower()
                )
            )

        # Create metadata
        meta = {"request_id": request_id} if request_id else {}

        # Create response
        response = ErrorResponse(
            success=False,
            message=message,
            code=code,
            data=None,
            details=error_details,
            meta=meta,
            timestamp=datetime.utcnow().isoformat()
        )

        return JSONResponse(
            status_code=status_code,
            content=response.dict()
        )

    def create_validation_error(
        self,
        field: str,
        message: str,
        error_type: str = "validation_error"
    ) -> ValidationException:
        """Create a validation error exception.

        Args:
            field: Field with validation error
            message: Error message
            error_type: Error type

        Returns:
            ValidationException
        """
        return ValidationException(
            message=f"Validation error: {message}",
            code=ErrorCode.VALIDATION_ERROR,
            details={
                "errors": [
                    {
                        "loc": field.split("."),
                        "msg": message,
                        "type": error_type
                    }
                ]
            },
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    def create_business_logic_error(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> BusinessLogicException:
        """Create a business logic error exception.

        Args:
            message: Error message
            details: Optional error details

        Returns:
            BusinessLogicException
        """
        return BusinessLogicException(
            message=message,
            code=ErrorCode.BUSINESS_LOGIC_ERROR,
            details=details or {},
            status_code=status.HTTP_400_BAD_REQUEST
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
            original_error: Optional original exception
            details: Optional error details

        Returns:
            DatabaseException
        """
        error_details = details or {}

        if original_error:
            error_details["original_error"] = str(original_error)
            error_details["traceback"] = traceback.format_exc()

        return DatabaseException(
            message=message,
            code=ErrorCode.DATABASE_ERROR,
            details=error_details,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            original_exception=original_error
        )

    def create_resource_not_found_error(
        self,
        resource_type: str,
        resource_id: Any
    ) -> ResourceNotFoundException:
        """Create a resource not found exception.

        Args:
            resource_type: Type of resource
            resource_id: Resource ID

        Returns:
            ResourceNotFoundException
        """
        return ResourceNotFoundException(
            message=f"{resource_type} with ID {resource_id} not found",
            code=ErrorCode.RESOURCE_NOT_FOUND,
            details={
                "resource_type": resource_type,
                "resource_id": str(resource_id)
            },
            status_code=status.HTTP_404_NOT_FOUND
        )

    def create_permission_denied_error(
        self,
        action: str,
        resource_type: str,
        permission: Optional[str] = None
    ) -> PermissionDeniedException:
        """Create a permission denied exception.

        Args:
            action: Action being performed
            resource_type: Type of resource
            permission: Optional required permission

        Returns:
            PermissionDeniedException
        """
        details = {
            "action": action,
            "resource_type": resource_type
        }

        if permission:
            details["required_permission"] = permission

        return PermissionDeniedException(
            message=f"You don't have permission to {action} {resource_type}",
            code=ErrorCode.PERMISSION_DENIED,
            details=details,
            status_code=status.HTTP_403_FORBIDDEN
        )

    def handle_exception_decorator(self, rethrow: bool = True):
        """Decorator for handling exceptions in functions.

        Args:
            rethrow: Whether to rethrow the exception after handling

        Returns:
            Decorator function
        """
        def decorator(func: F) -> F:
            if inspect.iscoroutinefunction(func):
                @wraps(func)
                async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                    try:
                        return await func(*args, **kwargs)
                    except Exception as e:
                        # Get request ID if available
                        request_id = None
                        for arg in args:
                            if isinstance(arg, Request):
                                request_id = getattr(arg.state, "request_id", None)
                                break

                        # Create context
                        context = ErrorContext(
                            request_id=request_id,
                            component=func.__module__,
                            operation=func.__qualname__
                        )

                        # Report error
                        await self.report_error(e, context)

                        # Rethrow if required
                        if rethrow:
                            raise

                        # Return error response if this is a route handler
                        return self.handle_exception(e, request_id)

                return cast(F, async_wrapper)
            else:
                @wraps(func)
                def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        # Get request ID if available
                        request_id = None
                        for arg in args:
                            if isinstance(arg, Request):
                                request_id = getattr(arg.state, "request_id", None)
                                break

                        # Create context
                        context = ErrorContext(
                            request_id=request_id,
                            component=func.__module__,
                            operation=func.__qualname__
                        )

                        # Report error synchronously
                        import asyncio
                        loop = asyncio.new_event_loop()
                        try:
                            loop.run_until_complete(self.report_error(e, context))
                        finally:
                            loop.close()

                        # Rethrow if required
                        if rethrow:
                            raise

                        # Return error response if this is a route handler
                        return self.handle_exception(e, request_id)

                return cast(F, sync_wrapper)

        return decorator
