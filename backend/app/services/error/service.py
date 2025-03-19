# /app/services/error/service.py
from __future__ import annotations

"""Main error service implementation.

This module provides the primary ErrorService that coordinates error
handling, reporting, and creation of error types throughout the application.
"""

import asyncio
import inspect
from typing import Any, Dict, List, Optional, TypeVar

from app.core.dependency_manager import dependency_manager
from app.core.exceptions import (
    AppException,
    AuthenticationException,
    BusinessLogicException,
    ErrorCode,
    PermissionDeniedException,
    ResourceAlreadyExistsException,
    ResourceNotFoundException,
    ValidationException
)
from app.core.logging import get_logger
from app.services.error.base import ErrorContext, ErrorReporter
from app.services.error.factory import ErrorReporterFactory
from app.services.interfaces import ServiceInterface

logger = get_logger("app.services.error.service")
T = TypeVar("T")


class ErrorService(ServiceInterface):
    """Service for handling, reporting, and creating errors in the application."""

    def __init__(self) -> None:
        """Initialize the error handling service."""
        self._reporters: List[ErrorReporter] = []

    def register_reporter(self, reporter: ErrorReporter) -> None:
        """Register a new error reporter.

        Args:
            reporter: Error reporter to register
        """
        self._reporters.append(reporter)
        logger.debug(f"Registered error reporter: {reporter.__class__.__name__}")

    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        """Report an error using all registered reporters.

        Args:
            exception: Exception to report
            context: Context information for the error
        """
        for reporter in self._reporters:
            try:
                await reporter.report_error(exception, context)
            except Exception as e:
                logger.error(f"Error reporter failed: {str(e)}", exc_info=e)

    def resource_not_found(
        self,
        resource_type: str,
        resource_id: str,
        message: Optional[str] = None
    ) -> ResourceNotFoundException:
        """Create a resource not found exception.

        Args:
            resource_type: Type of resource
            resource_id: ID of the resource
            message: Optional custom error message

        Returns:
            ResourceNotFoundException
        """
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
        """Create a resource already exists exception.

        Args:
            resource_type: Type of resource
            identifier: Value of the identifier
            field: Field name that must be unique
            message: Optional custom error message

        Returns:
            ResourceAlreadyExistsException
        """
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
        """Create a validation error exception.

        Args:
            field: Field with the validation error
            message: Validation error message
            error_type: Type of validation error

        Returns:
            ValidationException
        """
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
        """Create a permission denied exception.

        Args:
            action: Action being attempted
            resource_type: Type of resource
            permission: Required permission

        Returns:
            PermissionDeniedException
        """
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
        """Create a business logic error exception.

        Args:
            message: Error message
            details: Additional error details

        Returns:
            BusinessLogicException
        """
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
        """Ensure a value is not None or raise a resource not found exception.

        Args:
            value: Value to check
            resource_type: Type of resource
            resource_id: ID of the resource
            message: Optional custom error message

        Returns:
            The value if not None

        Raises:
            ResourceNotFoundException: If value is None
        """
        if value is None:
            raise self.resource_not_found(resource_type, resource_id, message)
        return value

    def handle_exception(self, exception: Exception, request_id: Optional[str] = None) -> None:
        """Handle an exception by logging and reporting it.

        Args:
            exception: Exception to handle
            request_id: Optional request ID for tracking
        """
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

            # Report error asynchronously
            asyncio.create_task(self.report_error(exception, context))

    async def initialize(self) -> None:
        """Initialize the error handling service."""
        logger.info("Initializing error service")

        # Register default reporters from factory
        default_reporters = ErrorReporterFactory.create_default_reporters()
        for reporter in default_reporters:
            self.register_reporter(reporter)

        logger.info(f"Registered {len(default_reporters)} default error reporters")

    async def shutdown(self) -> None:
        """Shutdown the error handling service."""
        logger.info("Shutting down error service")
        self._reporters = []
