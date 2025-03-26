from __future__ import annotations

"""Error handling service implementation.

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
from app.core.logging import get_logger

logger = get_logger("app.core.error.service")


class ErrorService:
    """Service for managing error handling and reporting."""

    def __init__(self) -> None:
        """Initialize the ErrorService."""
        self.reporters: List[ErrorReporter] = []

    async def initialize(self) -> None:
        """Initialize the error service.

        This method initializes the error handling system and registers
        the default error reporters.
        """
        logger.info("Initializing error service")

        # Initialize the error handling manager
        await initialize_manager()

        # Register default reporters
        self.reporters = ErrorReporterFactory.create_default_reporters()
        for reporter in self.reporters:
            register_reporter(reporter)

        logger.info(f"Registered {len(self.reporters)} default error reporters")

    async def shutdown(self) -> None:
        """Shut down the error service."""
        logger.info("Shutting down error service")
        await shutdown_manager()
        self.reporters = []

    async def register_reporter(self, reporter: ErrorReporter) -> None:
        """Register an error reporter.

        Args:
            reporter: The error reporter to register
        """
        self.reporters.append(reporter)
        register_reporter(reporter)
        logger.debug(f"Registered error reporter: {reporter.__class__.__name__}")

    async def register_reporter_by_name(self, reporter_name: str) -> None:
        """Register an error reporter by name.

        Args:
            reporter_name: Name of the reporter to register
        """
        reporter = ErrorReporterFactory.create_reporter_by_name(reporter_name)
        if reporter:
            await self.register_reporter(reporter)

    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        """Report an error to all registered reporters.

        Args:
            exception: The exception to report
            context: Context information about where the error occurred
        """
        await report_error(exception, context)

    def handle_exception(
        self,
        exception: Exception,
        request_id: Optional[str] = None,
        user_id: Optional[str] = None,
        function_name: Optional[str] = None,
    ) -> None:
        """Handle an exception by reporting it to all registered reporters.

        Args:
            exception: The exception to handle
            request_id: ID of the request that triggered the exception
            user_id: ID of the user who triggered the exception
            function_name: Name of the function where the exception occurred
        """
        handle_exception(
            exception=exception,
            request_id=request_id,
            user_id=user_id,
            function_name=function_name,
        )

    # Convenience methods for creating specific exception types

    def resource_not_found(
        self, resource_type: str, resource_id: str, message: Optional[str] = None
    ) -> Exception:
        """Create a ResourceNotFoundException.

        Args:
            resource_type: Type of resource that was not found
            resource_id: ID of the resource that was not found
            message: Optional custom message

        Returns:
            A ResourceNotFoundException instance
        """
        return resource_not_found(resource_type, resource_id, message)

    def resource_already_exists(
        self, resource_type: str, identifier: str, field: str = "id", message: Optional[str] = None
    ) -> Exception:
        """Create a ResourceAlreadyExistsException.

        Args:
            resource_type: Type of resource that already exists
            identifier: Identifier value of the resource
            field: Field name that contains the identifier
            message: Optional custom message

        Returns:
            A ResourceAlreadyExistsException instance
        """
        return resource_already_exists(resource_type, identifier, field, message)

    def validation_error(
        self, field: str, message: str, error_type: str = "invalid_value"
    ) -> Exception:
        """Create a ValidationException.

        Args:
            field: The field that failed validation
            message: The validation error message
            error_type: The type of validation error

        Returns:
            A ValidationException instance
        """
        return validation_error(field, message, error_type)

    def permission_denied(
        self, action: str, resource_type: str, permission: str
    ) -> Exception:
        """Create a PermissionDeniedException.

        Args:
            action: The action that was attempted
            resource_type: The type of resource being accessed
            permission: The permission that was required

        Returns:
            A PermissionDeniedException instance
        """
        return permission_denied(action, resource_type, permission)

    def business_logic_error(
        self, message: str, details: Optional[Dict[str, Any]] = None
    ) -> Exception:
        """Create a BusinessException.

        Args:
            message: The error message
            details: Additional details about the error

        Returns:
            A BusinessException instance
        """
        return business_logic_error(message, details)


# Singleton instance
_error_service: Optional[ErrorService] = None


def get_error_service() -> ErrorService:
    """Get the singleton ErrorService instance.

    Returns:
        The ErrorService instance
    """
    global _error_service

    if _error_service is None:
        _error_service = ErrorService()

    return _error_service
