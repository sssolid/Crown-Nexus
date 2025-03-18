from __future__ import annotations
import inspect
import sys
import traceback
from typing import Any, Callable, Dict, List, Optional, Protocol, Type, TypeVar, Union, cast

from fastapi import HTTPException
from pydantic import BaseModel

from app.core.dependency_manager import dependency_manager
from app.core.exceptions import (
    AppException, AuthenticationException, BadRequestException,
    BusinessLogicException, ErrorCode, PermissionDeniedException,
    ResourceAlreadyExistsException, ResourceNotFoundException,
    ValidationException
)
from app.core.logging import get_logger
from app.services.interfaces import ServiceInterface

logger = get_logger("app.services.error_service")
F = TypeVar("F", bound=Callable[..., Any])
T = TypeVar("T")

class ErrorContext(BaseModel):
    """Context information for error reporting."""
    function: str
    args: Optional[List[Any]] = None
    kwargs: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = None
    request_id: Optional[str] = None

class ErrorReporter(Protocol):
    """Base class for error reporting implementations."""

    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        """Report an error to the appropriate system."""
        ...

class DefaultErrorReporter:
    """Default implementation of error reporting that logs errors."""

    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        """Report an error to the logging system."""
        logger.error(
            f"Error in {context.function}",
            exc_info=exception,
            extra={
                "user_id": context.user_id,
                "request_id": context.request_id,
                "args": context.args,
                "kwargs": context.kwargs,
            }
        )

class ErrorService(ServiceInterface):
    """Service for handling, reporting, and creating errors in the application."""

    def __init__(self):
        """Initialize the error handling service."""
        self._reporters: List[ErrorReporter] = []
        dependency_manager.register_dependency("error_service", self)

    def register_reporter(self, reporter: ErrorReporter) -> None:
        """Register a new error reporter."""
        self._reporters.append(reporter)

    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        """Report an error using all registered reporters."""
        for reporter in self._reporters:
            try:
                await reporter.report_error(exception, context)
            except Exception as e:
                logger.error(f"Error reporter failed: {e}", exc_info=e)

    def resource_not_found(
        self,
        resource_type: str,
        resource_id: str,
        message: Optional[str] = None
    ) -> ResourceNotFoundException:
        """Create a resource not found exception."""
        if message is None:
            message = f"{resource_type} with ID {resource_id} not found"

        return ResourceNotFoundException(
            message=message,
            code=ErrorCode.RESOURCE_NOT_FOUND,
            details={
                "resource_type": resource_type,
                "resource_id": resource_id,
            },
            status_code=404,
            original_exception=None,
        )

    def resource_already_exists(
        self,
        resource_type: str,
        identifier: str,
        field: str,
        message: Optional[str] = None
    ) -> ResourceAlreadyExistsException:
        """Create a resource already exists exception."""
        if message is None:
            message = f"{resource_type} with {field} {identifier} already exists"

        return ResourceAlreadyExistsException(
            message=message,
            code=ErrorCode.RESOURCE_ALREADY_EXISTS,
            details={
                "resource_type": resource_type,
                "field": field,
                "identifier": identifier,
            },
            status_code=409,
            original_exception=None,
        )

    def validation_error(
        self,
        field: str,
        message: str,
        error_type: str = "invalid_value"
    ) -> ValidationException:
        """Create a validation error exception."""
        return ValidationException(
            message=f"Validation error: {message}",
            code=ErrorCode.VALIDATION_ERROR,
            details=[{
                "loc": [field],
                "msg": message,
                "type": error_type,
            }],
            status_code=422,
            original_exception=None,
        )

    def permission_denied(
        self,
        action: str,
        resource_type: str,
        permission: str
    ) -> PermissionDeniedException:
        """Create a permission denied exception."""
        return PermissionDeniedException(
            message=f"Permission denied to {action} {resource_type}",
            code=ErrorCode.PERMISSION_DENIED,
            details={
                "action": action,
                "resource_type": resource_type,
                "permission": permission,
            },
            status_code=403,
            original_exception=None,
        )

    def business_logic_error(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> BusinessLogicException:
        """Create a business logic error exception."""
        return BusinessLogicException(
            message=message,
            code=ErrorCode.BUSINESS_LOGIC_ERROR,
            details=details or {},
            status_code=400,
            original_exception=None,
        )

    def ensure_not_none(
        self,
        value: Optional[T],
        resource_type: str,
        resource_id: str,
        message: Optional[str] = None
    ) -> T:
        """Ensure a value is not None or raise a resource not found exception."""
        if value is None:
            raise self.resource_not_found(resource_type, resource_id, message)
        return value

    def handle_exception(self, exception: Exception, request_id: Optional[str] = None) -> None:
        """Handle an exception by logging and reporting it."""
        # Get caller frame information
        frame = inspect.currentframe()
        if frame is not None:
            frame = frame.f_back  # Get caller frame

        if frame is not None:
            function_name = frame.f_code.co_name
            args = inspect.getargvalues(frame).args
            locals_dict = frame.f_locals

            # Extract arguments
            args_values = [locals_dict[arg] for arg in args if arg in locals_dict]
            kwargs_values = {k: v for k, v in locals_dict.items()
                             if k not in args and not k.startswith('__')}

            # Create context
            context = ErrorContext(
                function=function_name,
                args=args_values,
                kwargs=kwargs_values,
                request_id=request_id,
            )

            # Report error
            asyncio.create_task(self.report_error(exception, context))

    async def initialize(self) -> None:
        """Initialize the error handling service."""
        # Register default reporter
        self.register_reporter(DefaultErrorReporter())

    async def shutdown(self) -> None:
        """Shutdown the error handling service."""
        # Nothing to shutdown
        self._reporters = []
