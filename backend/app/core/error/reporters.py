# app/core/error/reporters.py
from __future__ import annotations

"""
Error reporter implementations.

This module provides different implementations of the ErrorReporter protocol
for reporting errors to various destinations.
"""

import json
import traceback
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

import httpx

from app.core.error.base import ErrorContext, ErrorReporter, ErrorLogEntry
from app.logging.context import get_logger

logger = get_logger("app.core.error.reporters")


class LoggingErrorReporter(ErrorReporter):
    """
    Error reporter that logs errors using the application logging system.

    This reporter formats error information and logs it via the structured
    logging system, ensuring consistent error logging across the application.
    """

    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        """
        Report an error by logging it.

        Args:
            exception: The exception to report
            context: Context information about the error
        """
        error_info = {
            "function": context.function,
            "user_id": context.user_id,
            "request_id": context.request_id,
            "error_type": type(exception).__name__,
            "error_message": str(exception),
        }

        logger.error(
            f"Error in {context.function}: {str(exception)}",
            exc_info=exception,
            user_id=context.user_id,
            request_id=context.request_id,
            args=repr(context.args) if context.args else None,
            kwargs=repr(context.kwargs) if context.kwargs else None,
            error_context=error_info,
        )


class DatabaseErrorReporter(ErrorReporter):
    """
    Error reporter that stores errors in a database.

    This reporter formats error information and stores it in a database
    for later analysis and reporting.
    """

    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        """
        Report an error by storing it in a database.

        Args:
            exception: The exception to report
            context: Context information about the error
        """
        error_id = str(uuid.uuid4())
        timestamp = datetime.now(datetime.UTC).isoformat()

        error_entry = ErrorLogEntry(
            error_id=error_id,
            timestamp=timestamp,
            error_type=type(exception).__name__,
            error_message=str(exception),
            function=context.function,
            traceback=traceback.format_exception(
                type(exception), exception, exception.__traceback__
            ),
            user_id=context.user_id,
            request_id=context.request_id,
            context={"args": context.args, "kwargs": context.kwargs},
        )

        try:
            # In a real implementation, this would store the error in a database
            # For now, we'll just log that we would have stored it
            logger.info(
                f"Database error reporter: Would store error {error_id} from {context.function}",
                error_entry=error_entry.model_dump(),
            )
        except Exception as e:
            logger.error(f"Failed to store error in database: {str(e)}", exc_info=e)


class ExternalServiceReporter(ErrorReporter):
    """
    Error reporter that sends errors to an external service.

    This reporter formats error information and sends it to an external
    error tracking or monitoring service via HTTP.
    """

    def __init__(self, service_url: str, api_key: str) -> None:
        """
        Initialize the reporter with service connection details.

        Args:
            service_url: URL of the external error reporting service
            api_key: API key for authenticating with the service
        """
        self.service_url = service_url
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        """
        Report an error by sending it to an external service.

        Args:
            exception: The exception to report
            context: Context information about the error
        """
        error_data = {
            "error_id": str(uuid.uuid4()),
            "timestamp": datetime.now(datetime.UTC).isoformat(),
            "function": context.function,
            "user_id": context.user_id,
            "request_id": context.request_id,
            "error_type": type(exception).__name__,
            "error_message": str(exception),
            "traceback": traceback.format_exception(
                type(exception), exception, exception.__traceback__
            ),
            "context": {
                "args": repr(context.args) if context.args else None,
                "kwargs": repr(context.kwargs) if context.kwargs else None,
            },
        }

        try:
            # In a real implementation, this would send the error to the external service
            # For now, we'll just log that we would have sent it
            logger.info(
                f"External service reporter: Would send error to {self.service_url}",
                error_data=error_data,
                service_url=self.service_url,
            )
        except Exception as e:
            logger.error(
                f"Failed to report error to external service: {str(e)}", exc_info=e
            )


class CompositeErrorReporter(ErrorReporter):
    """
    Error reporter that delegates to multiple other reporters.

    This reporter sends errors to multiple destinations by delegating
    to a collection of other error reporters.
    """

    def __init__(self, reporters: list[ErrorReporter]) -> None:
        """
        Initialize with a list of reporters.

        Args:
            reporters: List of error reporters to use
        """
        self.reporters = reporters

    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        """
        Report an error using all configured reporters.

        Args:
            exception: The exception to report
            context: Context information about the error
        """
        for reporter in self.reporters:
            try:
                await reporter.report_error(exception, context)
            except Exception as e:
                logger.error(
                    f"Error in reporter {reporter.__class__.__name__}: {str(e)}",
                    exc_info=e,
                )
