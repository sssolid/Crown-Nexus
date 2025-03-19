# /app/services/error/reporters.py
from __future__ import annotations

"""Error reporter implementations.

This module provides different implementations of the ErrorReporter protocol
for reporting errors to various destinations.
"""

from typing import Any, Dict, Optional

from app.core.logging import get_logger
from app.services.error.base import ErrorContext, ErrorReporter

logger = get_logger("app.services.error.reporters")


class LoggingErrorReporter(ErrorReporter):
    """Reporter that logs errors to the application logging system."""

    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        """Report an error to the logging system.

        Args:
            exception: The exception to report
            context: Context information about the error
        """
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


class DatabaseErrorReporter(ErrorReporter):
    """Reporter that logs errors to a database for persistence."""

    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        """Report an error to the database.

        Args:
            exception: The exception to report
            context: Context information about the error
        """
        # Placeholder for database error reporting implementation
        # This would typically save the error to a database table
        logger.debug(
            f"Database error reporter: {str(exception)} in {context.function}"
        )


class ExternalServiceReporter(ErrorReporter):
    """Reporter that sends errors to an external error tracking service."""

    def __init__(self, service_url: str, api_key: str) -> None:
        """Initialize the external service reporter.

        Args:
            service_url: URL of the error tracking service API
            api_key: API key for authentication
        """
        self.service_url = service_url
        self.api_key = api_key

    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        """Report an error to an external service like Sentry or Rollbar.

        Args:
            exception: The exception to report
            context: Context information about the error
        """
        # Placeholder for external service integration
        # This would typically make an HTTP request to the error service
        logger.debug(
            f"External service reporter: {str(exception)} in {context.function}"
        )
