from __future__ import annotations

"""Error handling service for application-wide error management.

This module provides a centralized service for handling errors, creating error
responses, and reporting errors. It consolidates error handling functionality
from the error_handling_service.py and errors.py modules.

The service provides methods for:
- Handling exceptions and creating error responses
- Creating specific typed exceptions
- Reporting errors to logging and monitoring systems
- Helper functions for common error patterns
"""

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
    AuthenticationException,
    BadRequestException,
    BusinessLogicException,
    ConfigurationException,
    DataIntegrityException,
    DatabaseException,
    ErrorCategory,
    ErrorCode,
    ErrorDetail,
    ErrorResponse,
    ErrorSeverity,
    ExternalServiceException,
    InvalidStateException,
    NetworkException,
    OperationNotAllowedException,
    PermissionDeniedException,
    RateLimitException,
    ResourceAlreadyExistsException,
    ResourceNotFoundException,
    ServiceUnavailableException,
    TimeoutException,
    TransactionException,
    ValidationException,
)
from app.core.logging import get_logger

logger = get_logger("app.services.error_handling_service")
F = TypeVar("F", bound=Callable[..., Any])
T = TypeVar("T")


class ErrorContext(BaseModel):
    """Context information for error reporting."""

    request_id: Optional[str] = None
    user_id: Optional[str] = None
    path: Optional[str] = None
    method: Optional[str] = None
    component: Optional[str] = None
    operation: Optional[str] = None
    additional_data: Dict[str, Any] = Field(default_factory=dict)


class ErrorReporter:
    """Base class for error reporting implementations."""

    async def report_error(
        self, exception: Exception, context: Optional[ErrorContext] = None
    ) -> None:
        """Report an error to the appropriate system.

        Args:
            exception: The exception that occurred
            context: Additional context information about the error
        """
        pass


class DefaultErrorReporter(ErrorReporter):
    """Default implementation of error reporting that logs errors."""

    async def report_error(
        self, exception: Exception, context: Optional[ErrorContext] = None
    ) -> None:
        """Report an error to the logging system.

        Args:
            exception: The exception that occurred
            context: Additional context information about the error
        """
        ctx = context or ErrorContext()
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

        log_data = {
            "error_type": exception.__class__.__name__,
            "request_id": ctx.request_id,
            "user_id": ctx.user_id,
            "path": ctx.path,
            "method": ctx.method,
            "component": ctx.component,
            "operation": ctx.operation,
        }

        if ctx.additional_data:
            log_data.update(ctx.additional_data)

        if not isinstance(exception, AppException):
            log_data["traceback"] = traceback.format_exc()

        if hasattr(exception, "code"):
            log_data["error_code"] = getattr(exception, "code")

        log_func = getattr(logger, level)
        log_func(f"Error: {str(exception)}", **log_data)


class ErrorHandlingService:
    """Service for handling, reporting, and creating errors in the application."""

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
        """Shut down the error handling service."""
        self.logger.debug("Shutting down error handling service")

    def _register_known_exceptions(self) -> None:
        """Register known exception types and their properties."""
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
        """Register a new error reporter.

        Args:
            reporter: The error reporter to register
        """
        self.reporters.append(reporter)

    async def report_error(
        self, exception: Exception, context: Optional[ErrorContext] = None
    ) -> None:
        """Report an error using all registered reporters.

        Args:
            exception: The exception that occurred
            context: Additional context information about the error
        """
        for reporter in self.reporters:
            try:
                await reporter.report_error(exception, context)
            except Exception as e:
                self.logger.error(f"Error reporter failed: {str(e)}", exc_info=True)

    def handle_exception(
        self, exception: Exception, request_id: Optional[str] = None
    ) -> ErrorResponse:
        """Convert an exception to a standardized error response.

        Args:
            exception: The exception to handle
            request_id: The request ID for tracking

        Returns:
            A standardized error response object
        """
        if isinstance(exception, AppException):
            return exception.to_response(request_id)

        if isinstance(exception, HTTPException):
            return self._convert_http_exception(exception, request_id)

        error_type = exception.__class__.__name__
        error_details = []
        error_details.append(
            ErrorDetail(loc=["server"], msg=str(exception), type="server_error")
        )
        tb = traceback.format_exc()

        meta = {"request_id": request_id} if request_id else {}
        meta["error_type"] = error_type
        meta["severity"] = ErrorSeverity.ERROR
        meta["category"] = ErrorCategory.UNKNOWN

        response = ErrorResponse(
            success=False,
            message=f"An unexpected error occurred: {str(exception)}",
            code=ErrorCode.UNKNOWN_ERROR,
            data=None,
            details=error_details,
            meta=meta,
            timestamp=datetime.utcnow().isoformat(),
        )
        return response

    def _convert_http_exception(
        self, exception: HTTPException, request_id: Optional[str] = None
    ) -> ErrorResponse:
        """Convert an HTTP exception to a standardized error response.

        Args:
            exception: The HTTP exception to convert
            request_id: The request ID for tracking

        Returns:
            A standardized error response object
        """
        error_code = None
        category = ErrorCategory.UNKNOWN
        severity = ErrorSeverity.WARNING

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

        error_details = [
            ErrorDetail(
                loc=["server"],
                msg=str(exception.detail),
                type=error_code.value.lower(),
            )
        ]

        meta = {"request_id": request_id} if request_id else {}
        meta["severity"] = severity
        meta["category"] = category

        response = ErrorResponse(
            success=False,
            message=str(exception.detail),
            code=error_code,
            data=None,
            details=error_details,
            meta=meta,
            timestamp=datetime.utcnow().isoformat(),
        )
        return response

    def create_error_response(
        self,
        message: str,
        code: ErrorCode,
        status_code: int,
        details: Optional[List[Dict[str, Any]]] = None,
        request_id: Optional[str] = None,
    ) -> JSONResponse:
        """Create a JSON response for an error.

        Args:
            message: The error message
            code: The error code
            status_code: The HTTP status code
            details: Detailed error information
            request_id: The request ID for tracking

        Returns:
            A JSON response with error information
        """
        error_details = []
        if details:
            for detail in details:
                error_details.append(
                    ErrorDetail(
                        loc=detail.get("loc", ["server"]),
                        msg=detail.get("msg", message),
                        type=detail.get("type", code.value.lower()),
                    )
                )
        else:
            error_details.append(
                ErrorDetail(loc=["server"], msg=message, type=code.value.lower())
            )

        meta = {"request_id": request_id} if request_id else {}
        response = ErrorResponse(
            success=False,
            message=message,
            code=code,
            data=None,
            details=error_details,
            meta=meta,
            timestamp=datetime.utcnow().isoformat(),
        )
        return JSONResponse(status_code=status_code, content=response.dict())

    # Helper functions for creating specific error types

    def create_validation_error(
        self, field: str, message: str, error_type: str = "validation_error"
    ) -> ValidationException:
        """Create a validation error exception.

        Args:
            field: The field that failed validation
            message: The error message
            error_type: The type of validation error

        Returns:
            A ValidationException instance
        """
        return ValidationException(
            message=f"Validation error: {message}",
            code=ErrorCode.VALIDATION_ERROR,
            details={
                "errors": [
                    {"loc": field.split("."), "msg": message, "type": error_type}
                ]
            },
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    def create_business_logic_error(
        self, message: str, details: Optional[Dict[str, Any]] = None
    ) -> BusinessLogicException:
        """Create a business logic error exception.

        Args:
            message: The error message
            details: Additional error details

        Returns:
            A BusinessLogicException instance
        """
        return BusinessLogicException(
            message=message,
            code=ErrorCode.BUSINESS_LOGIC_ERROR,
            details=details or {},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def create_database_error(
        self,
        message: str,
        original_error: Optional[Exception] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> DatabaseException:
        """Create a database error exception.

        Args:
            message: The error message
            original_error: The original exception that caused this error
            details: Additional error details

        Returns:
            A DatabaseException instance
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
            original_exception=original_error,
        )

    def create_resource_not_found_error(
        self, resource_type: str, resource_id: Any
    ) -> ResourceNotFoundException:
        """Create a resource not found exception.

        Args:
            resource_type: The type of resource that wasn't found
            resource_id: The ID of the resource that wasn't found

        Returns:
            A ResourceNotFoundException instance
        """
        return ResourceNotFoundException(
            message=f"{resource_type} with ID {resource_id} not found",
            code=ErrorCode.RESOURCE_NOT_FOUND,
            details={"resource_type": resource_type, "resource_id": str(resource_id)},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    def create_permission_denied_error(
        self, action: str, resource_type: str, permission: Optional[str] = None
    ) -> PermissionDeniedException:
        """Create a permission denied exception.

        Args:
            action: The action that was denied
            resource_type: The type of resource involved
            permission: The specific permission that was missing

        Returns:
            A PermissionDeniedException instance
        """
        details = {"action": action, "resource_type": resource_type}
        if permission:
            details["required_permission"] = permission
        return PermissionDeniedException(
            message=f"You don't have permission to {action} {resource_type}",
            code=ErrorCode.PERMISSION_DENIED,
            details=details,
            status_code=status.HTTP_403_FORBIDDEN,
        )

    def handle_exception_decorator(self, rethrow: bool = True):
        """Decorator to handle exceptions in a function.

        Args:
            rethrow: Whether to re-raise the exception after handling it

        Returns:
            A decorator function
        """

        def decorator(func: F) -> F:
            if inspect.iscoroutinefunction(func):

                @wraps(func)
                async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                    try:
                        return await func(*args, **kwargs)
                    except Exception as e:
                        request_id = None
                        for arg in args:
                            if isinstance(arg, Request):
                                request_id = getattr(arg.state, "request_id", None)
                                break
                        context = ErrorContext(
                            request_id=request_id,
                            component=func.__module__,
                            operation=func.__qualname__,
                        )
                        await self.report_error(e, context)
                        if rethrow:
                            raise
                        return self.handle_exception(e, request_id)

                return cast(F, async_wrapper)
            else:

                @wraps(func)
                def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        request_id = None
                        for arg in args:
                            if isinstance(arg, Request):
                                request_id = getattr(arg.state, "request_id", None)
                                break
                        context = ErrorContext(
                            request_id=request_id,
                            component=func.__module__,
                            operation=func.__qualname__,
                        )
                        import asyncio

                        loop = asyncio.new_event_loop()
                        try:
                            loop.run_until_complete(self.report_error(e, context))
                        finally:
                            loop.close()
                        if rethrow:
                            raise
                        return self.handle_exception(e, request_id)

                return cast(F, sync_wrapper)

        return decorator

    # Helper functions migrated from errors.py

    def ensure_not_none(
        self, value: Optional[T], resource_type: str, resource_id: Any, message: Optional[str] = None
    ) -> T:
        """Ensure a value is not None or raise a resource not found exception.

        Args:
            value: The value to check
            resource_type: The type of resource
            resource_id: The ID of the resource
            message: Optional custom error message

        Returns:
            The value if it's not None

        Raises:
            ResourceNotFoundException: If the value is None
        """
        if value is None:
            raise self.create_resource_not_found_error(resource_type, resource_id)
        return value

    def validation_error(
        self, field: str, message: str, error_type: str = "validation_error"
    ) -> ValidationException:
        """Create a validation error exception.

        Args:
            field: The field that failed validation
            message: The error message
            error_type: The type of validation error

        Returns:
            A ValidationException instance
        """
        return self.create_validation_error(field, message, error_type)

    def permission_denied(
        self, action: str, resource_type: str, permission: Optional[str] = None
    ) -> PermissionDeniedException:
        """Create a permission denied exception.

        Args:
            action: The action that was denied
            resource_type: The type of resource involved
            permission: The specific permission that was missing

        Returns:
            A PermissionDeniedException instance
        """
        return self.create_permission_denied_error(action, resource_type, permission)

    def bad_request(
        self, message: str, details: Optional[Dict[str, Any]] = None
    ) -> BadRequestException:
        """Create a bad request exception.

        Args:
            message: The error message
            details: Additional error details

        Returns:
            A BadRequestException instance
        """
        return BadRequestException(
            message=message,
            code=ErrorCode.BAD_REQUEST,
            details=details or {},
            status_code=400,
        )

    def business_logic_error(
        self, message: str, details: Optional[Dict[str, Any]] = None
    ) -> BusinessLogicException:
        """Create a business logic error exception.

        Args:
            message: The error message
            details: Additional error details

        Returns:
            A BusinessLogicException instance
        """
        return self.create_business_logic_error(message, details)

    def database_error(
        self,
        message: str,
        original_error: Optional[Exception] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> DatabaseException:
        """Create a database error exception.

        Args:
            message: The error message
            original_error: The original exception that caused this error
            details: Additional error details

        Returns:
            A DatabaseException instance
        """
        return self.create_database_error(message, original_error, details)

    def resource_not_found(
        self, resource_type: str, resource_id: Any, message: Optional[str] = None
    ) -> ResourceNotFoundException:
        """Create a resource not found exception.

        Args:
            resource_type: The type of resource that wasn't found
            resource_id: The ID of the resource that wasn't found
            message: Optional custom error message

        Returns:
            A ResourceNotFoundException instance
        """
        error_message = message or f"{resource_type} with ID {resource_id} not found"
        return ResourceNotFoundException(
            message=error_message,
            code=ErrorCode.RESOURCE_NOT_FOUND,
            details={"resource_type": resource_type, "resource_id": str(resource_id)},
            status_code=404,
        )

    def resource_already_exists(
        self,
        resource_type: str,
        identifier: Any,
        field: str = "id",
        message: Optional[str] = None,
    ) -> ResourceAlreadyExistsException:
        """Create a resource already exists exception.

        Args:
            resource_type: The type of resource that already exists
            identifier: The identifier of the resource
            field: The field name for the identifier
            message: Optional custom error message

        Returns:
            A ResourceAlreadyExistsException instance
        """
        error_message = (
            message or f"{resource_type} with {field} {identifier} already exists"
        )
        return ResourceAlreadyExistsException(
            message=error_message,
            code=ErrorCode.RESOURCE_ALREADY_EXISTS,
            details={"resource_type": resource_type, field: str(identifier)},
            status_code=409,
        )

    def invalid_state(
        self,
        entity_type: str,
        entity_id: Any,
        current_state: str,
        expected_state: Optional[str] = None,
        allowed_states: Optional[List[str]] = None,
    ) -> InvalidStateException:
        """Create an invalid state exception.

        Args:
            entity_type: The type of entity
            entity_id: The ID of the entity
            current_state: The current state of the entity
            expected_state: The expected state
            allowed_states: List of allowed states

        Returns:
            An InvalidStateException instance
        """
        details = {
            "entity_type": entity_type,
            "entity_id": str(entity_id),
            "current_state": current_state,
        }
        if expected_state:
            message = f"{entity_type} {entity_id} is in invalid state: {current_state} (expected: {expected_state})"
            details["expected_state"] = expected_state
        elif allowed_states:
            message = f"{entity_type} {entity_id} is in invalid state: {current_state} (allowed: {', '.join(allowed_states)})"
            details["allowed_states"] = allowed_states
        else:
            message = f"{entity_type} {entity_id} is in invalid state: {current_state}"
        return InvalidStateException(
            message=message,
            code=ErrorCode.INVALID_STATE_ERROR,
            details=details,
            status_code=409,
        )

    def operation_not_allowed(
        self,
        operation: str,
        entity_type: str,
        entity_id: Optional[Any] = None,
        reason: Optional[str] = None,
    ) -> OperationNotAllowedException:
        """Create an operation not allowed exception.

        Args:
            operation: The operation that's not allowed
            entity_type: The type of entity
            entity_id: The ID of the entity
            reason: The reason the operation is not allowed

        Returns:
            An OperationNotAllowedException instance
        """
        details = {"operation": operation, "entity_type": entity_type}
        if entity_id is not None:
            details["entity_id"] = str(entity_id)

        if entity_id is not None:
            message = f"Operation {operation} is not allowed for {entity_type} {entity_id}"
        else:
            message = f"Operation {operation} is not allowed for {entity_type}"

        if reason:
            message += f": {reason}"
            details["reason"] = reason

        return OperationNotAllowedException(
            message=message,
            code=ErrorCode.OPERATION_NOT_ALLOWED,
            details=details,
            status_code=403,
        )

    def external_service_error(
        self,
        service_name: str,
        message: str,
        original_error: Optional[Exception] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> ExternalServiceException:
        """Create an external service error exception.

        Args:
            service_name: The name of the external service
            message: The error message
            original_error: The original exception
            details: Additional error details

        Returns:
            An ExternalServiceException instance
        """
        error_details = details or {}
        error_details["service_name"] = service_name
        return ExternalServiceException(
            message=f"External service error ({service_name}): {message}",
            code=ErrorCode.EXTERNAL_SERVICE_ERROR,
            details=error_details,
            status_code=502,
            original_exception=original_error,
        )


# Handle Python's lack of function decorators with no function call
from functools import wraps


# Create a singleton instance for easy access
def get_error_service() -> ErrorHandlingService:
    """Get or create the singleton error handling service instance.

    Returns:
        The error handling service instance
    """
    try:
        from app.core.dependency_manager import get_dependency
        return get_dependency("error_handling_service")
    except Exception:
        return ErrorHandlingService()


# Convenience functions for error handling
def ensure_not_none(
    value: Optional[T], resource_type: str, resource_id: Any, message: Optional[str] = None
) -> T:
    """Ensure a value is not None or raise a resource not found exception.

    Args:
        value: The value to check
        resource_type: The type of resource
        resource_id: The ID of the resource
        message: Optional custom error message

    Returns:
        The value if it's not None

    Raises:
        ResourceNotFoundException: If the value is None
    """
    service = get_error_service()
    return service.ensure_not_none(value, resource_type, resource_id, message)


def validation_error(
    field: str, message: str, error_type: str = "validation_error"
) -> ValidationException:
    """Create a validation error exception.

    Args:
        field: The field that failed validation
        message: The error message
        error_type: The type of validation error

    Returns:
        A ValidationException instance
    """
    service = get_error_service()
    return service.validation_error(field, message, error_type)


def permission_denied(
    action: str, resource_type: str, permission: Optional[str] = None
) -> PermissionDeniedException:
    """Create a permission denied exception.

    Args:
        action: The action that was denied
        resource_type: The type of resource involved
        permission: The specific permission that was missing

    Returns:
        A PermissionDeniedException instance
    """
    service = get_error_service()
    return service.permission_denied(action, resource_type, permission)


def bad_request(
    message: str, details: Optional[Dict[str, Any]] = None
) -> BadRequestException:
    """Create a bad request exception.

    Args:
        message: The error message
        details: Additional error details

    Returns:
        A BadRequestException instance
    """
    service = get_error_service()
    return service.bad_request(message, details)


def business_logic_error(
    message: str, details: Optional[Dict[str, Any]] = None
) -> BusinessLogicException:
    """Create a business logic error exception.

    Args:
        message: The error message
        details: Additional error details

    Returns:
        A BusinessLogicException instance
    """
    service = get_error_service()
    return service.business_logic_error(message, details)


def database_error(
    message: str,
    original_error: Optional[Exception] = None,
    details: Optional[Dict[str, Any]] = None,
) -> DatabaseException:
    """Create a database error exception.

    Args:
        message: The error message
        original_error: The original exception that caused this error
        details: Additional error details

    Returns:
        A DatabaseException instance
    """
    service = get_error_service()
    return service.database_error(message, original_error, details)


def resource_not_found(
    resource_type: str, resource_id: Any, message: Optional[str] = None
) -> ResourceNotFoundException:
    """Create a resource not found exception.

    Args:
        resource_type: The type of resource that wasn't found
        resource_id: The ID of the resource that wasn't found
        message: Optional custom error message

    Returns:
        A ResourceNotFoundException instance
    """
    service = get_error_service()
    return service.resource_not_found(resource_type, resource_id, message)


def resource_already_exists(
    resource_type: str,
    identifier: Any,
    field: str = "id",
    message: Optional[str] = None,
) -> ResourceAlreadyExistsException:
    """Create a resource already exists exception.

    Args:
        resource_type: The type of resource that already exists
        identifier: The identifier of the resource
        field: The field name for the identifier
        message: Optional custom error message

    Returns:
        A ResourceAlreadyExistsException instance
    """
    service = get_error_service()
    return service.resource_already_exists(resource_type, identifier, field, message)


def external_service_error(
    service_name: str,
    message: str,
    original_error: Optional[Exception] = None,
    details: Optional[Dict[str, Any]] = None,
) -> ExternalServiceException:
    """Create an external service error exception.

    Args:
        service_name: The name of the external service
        message: The error message
        original_error: The original exception
        details: Additional error details

    Returns:
        An ExternalServiceException instance
    """
    service = get_error_service()
    return service.external_service_error(service_name, message, original_error, details)