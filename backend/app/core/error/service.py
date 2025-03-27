# app/core/error/service.py
from __future__ import annotations

"""
Error handling service implementation.

This module provides a service wrapper around the error handling system,
making it available through the dependency manager.
"""

from typing import Any, Dict, List, Optional, Type

from app.core.error.base import ErrorContext, ErrorReporter
from app.core.error.factory import ErrorReporterFactory
from app.core.error.manager import (
    business_logic_error,
    handle_exception,
    initialize as initialize_manager,
    permission_denied,
    register_reporter,
    report_error,
    resource_already_exists,
    resource_not_found,
    shutdown as shutdown_manager,
    validation_error,
)
from app.core.error.reporters import (
    CompositeErrorReporter,
    DatabaseErrorReporter,
    ExternalServiceReporter,
    LoggingErrorReporter,
)
from app.logging.context import get_logger

logger = get_logger("app.core.error.service")


class ErrorService:
    """
    Service for error handling and reporting.

    This service provides methods for creating and reporting errors,
    as well as initializing and managing error reporters.
    """

    def __init__(self) -> None:
        """Initialize the error service."""
        self.reporters: List[ErrorReporter] = []
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize the error service."""
        if self._initialized:
            logger.debug("Error service already initialized, skipping")
            return

        logger.info("Initializing error service")

        # Initialize the error manager only if needed
        await initialize_manager()

        # Create and register reporters
        self.reporters = ErrorReporterFactory.create_default_reporters()
        for reporter in self.reporters:
            register_reporter(reporter)

        self._initialized = True
        logger.info(f"Registered {len(self.reporters)} default error reporters")

    async def shutdown(self) -> None:
        """Shut down the error service."""
        if not self._initialized:
            return

        logger.info("Shutting down error service")
        await shutdown_manager()
        self.reporters = []
        self._initialized = False

    async def register_reporter(self, reporter: ErrorReporter) -> None:
        """
        Register an error reporter.

        Args:
            reporter: The error reporter to register
        """
        self.reporters.append(reporter)
        register_reporter(reporter)
        logger.debug(f"Registered error reporter: {reporter.__class__.__name__}")

    async def register_reporter_by_name(self, reporter_name: str) -> None:
        """
        Register an error reporter by name.

        Args:
            reporter_name: Name of the reporter to register
        """
        reporter = ErrorReporterFactory.create_reporter_by_name(reporter_name)
        if reporter:
            await self.register_reporter(reporter)

    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        """
        Report an error with context.

        Args:
            exception: The exception to report
            context: Context information for the error
        """
        await report_error(exception, context)

    def handle_exception(
        self,
        exception: Exception,
        request_id: Optional[str] = None,
        user_id: Optional[str] = None,
        function_name: Optional[str] = None,
    ) -> None:
        """
        Handle an exception by reporting it.

        Args:
            exception: The exception to handle
            request_id: Optional request ID
            user_id: Optional user ID
            function_name: Optional function name
        """
        handle_exception(
            exception=exception,
            request_id=request_id,
            user_id=user_id,
            function_name=function_name,
        )

    def resource_not_found(
        self, resource_type: str, resource_id: str, message: Optional[str] = None
    ) -> Exception:
        """
        Create a resource not found exception.

        Args:
            resource_type: Type of resource that was not found
            resource_id: ID of the resource that was not found
            message: Optional custom error message

        Returns:
            A configured ResourceNotFoundException
        """
        return resource_not_found(resource_type, resource_id, message)

    def resource_already_exists(
        self,
        resource_type: str,
        identifier: str,
        field: str = "id",
        message: Optional[str] = None,
    ) -> Exception:
        """
        Create a resource already exists exception.

        Args:
            resource_type: Type of resource that already exists
            identifier: Identifier of the resource
            field: Field name of the identifier (default: 'id')
            message: Optional custom error message

        Returns:
            A configured ResourceAlreadyExistsException
        """
        return resource_already_exists(resource_type, identifier, field, message)

    def validation_error(
        self, field: str, message: str, error_type: str = "invalid_value"
    ) -> Exception:
        """
        Create a validation error exception.

        Args:
            field: Field that failed validation
            message: Error message
            error_type: Type of validation error

        Returns:
            A configured ValidationException
        """
        return validation_error(field, message, error_type)

    def permission_denied(
        self, action: str, resource_type: str, permission: str
    ) -> Exception:
        """
        Create a permission denied exception.

        Args:
            action: Action that was attempted
            resource_type: Type of resource being accessed
            permission: Permission that was required

        Returns:
            A configured PermissionDeniedException
        """
        return permission_denied(action, resource_type, permission)

    def business_logic_error(
        self, message: str, details: Optional[Dict[str, Any]] = None
    ) -> Exception:
        """
        Create a business logic error exception.

        Args:
            message: Error message
            details: Additional error details

        Returns:
            A configured BusinessException
        """
        return business_logic_error(message, details)


# Singleton error service instance
_error_service: Optional[ErrorService] = None


def get_error_service() -> ErrorService:
    """
    Get the error service singleton.

    Returns:
        The error service instance
    """
    global _error_service
    if _error_service is None:
        _error_service = ErrorService()
    return _error_service
