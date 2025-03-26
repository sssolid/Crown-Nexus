from __future__ import annotations

"""Error reporter implementations.

This module provides different implementations of the ErrorReporter protocol
for reporting errors to various destinations.
"""

import json
import traceback
from typing import Any, Dict, Optional

import httpx

from app.core.logging import get_logger
from app.core.error.base import ErrorContext, ErrorReporter

logger = get_logger("app.core.error.reporters")


class LoggingErrorReporter(ErrorReporter):
    """Error reporter that logs errors using the logging system."""

    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        """Report an error to the logging system.

        Args:
            exception: The exception to report
            context: Context information about where the error occurred
        """
        # Collect relevant error information
        error_info = {
            "function": context.function,
            "user_id": context.user_id,
            "request_id": context.request_id,
            "error_type": type(exception).__name__,
            "error_message": str(exception),
        }

        # Log the error with context
        logger.error(
            f"Error in {context.function}: {str(exception)}",
            exc_info=exception,
            extra={
                "user_id": context.user_id,
                "request_id": context.request_id,
                "args": repr(context.args) if context.args else None,
                "kwargs": repr(context.kwargs) if context.kwargs else None,
                "error_context": error_info,
            }
        )


class DatabaseErrorReporter(ErrorReporter):
    """Error reporter that stores errors in a database."""

    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        """Report an error to the database.

        Args:
            exception: The exception to report
            context: Context information about where the error occurred
        """
        # Format the error data
        error_data = {
            "function": context.function,
            "user_id": context.user_id,
            "request_id": context.request_id,
            "error_type": type(exception).__name__,
            "error_message": str(exception),
            "traceback": traceback.format_exception(
                type(exception), exception, exception.__traceback__
            ),
            "args": context.args,
            "kwargs": context.kwargs,
        }

        try:
            # In a real implementation, this would insert into a database
            # For now, just log that we would store this error
            logger.debug(
                f"Database error reporter: Would store error from {context.function}: {str(exception)}",
                extra={"error_data": error_data}
            )

            # Placeholder for actual database storage implementation
            # from app.db.session import async_session_factory
            # async with async_session_factory() as session:
            #     error_entry = ErrorLog(
            #         function_name=context.function,
            #         user_id=context.user_id,
            #         request_id=context.request_id,
            #         error_type=type(exception).__name__,
            #         error_message=str(exception),
            #         traceback="\n".join(traceback.format_exception(
            #             type(exception), exception, exception.__traceback__
            #         )),
            #         context_data=json.dumps({
            #             "args": repr(context.args),
            #             "kwargs": repr(context.kwargs)
            #         })
            #     )
            #     session.add(error_entry)
            #     await session.commit()

        except Exception as e:
            logger.error(f"Failed to store error in database: {str(e)}", exc_info=e)


class ExternalServiceReporter(ErrorReporter):
    """Error reporter that sends errors to an external error reporting service."""

    def __init__(self, service_url: str, api_key: str) -> None:
        """Initialize the ExternalServiceReporter.

        Args:
            service_url: URL of the error reporting service
            api_key: API key for the error reporting service
        """
        self.service_url = service_url
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        """Report an error to the external service.

        Args:
            exception: The exception to report
            context: Context information about where the error occurred
        """
        # Format the error data for the external service
        error_data = {
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
            }
        }

        try:
            # In a real implementation, this would send to an external service
            # For now, just log that we would send this error
            logger.debug(
                f"External service reporter: Would send error from {context.function} to {self.service_url}",
                extra={
                    "error_data": error_data,
                    "service_url": self.service_url
                }
            )

            # Placeholder for actual API call
            # async with httpx.AsyncClient() as client:
            #     response = await client.post(
            #         self.service_url,
            #         headers=self.headers,
            #         json=error_data,
            #         timeout=5.0
            #     )
            #     response.raise_for_status()

        except Exception as e:
            logger.error(f"Failed to report error to external service: {str(e)}", exc_info=e)


class CompositeErrorReporter(ErrorReporter):
    """Error reporter that delegates to multiple other reporters."""

    def __init__(self, reporters: list[ErrorReporter]) -> None:
        """Initialize the CompositeErrorReporter.

        Args:
            reporters: List of error reporters to delegate to
        """
        self.reporters = reporters

    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        """Report an error to all child reporters.

        Args:
            exception: The exception to report
            context: Context information about where the error occurred
        """
        for reporter in self.reporters:
            try:
                await reporter.report_error(exception, context)
            except Exception as e:
                logger.error(
                    f"Error in reporter {reporter.__class__.__name__}: {str(e)}",
                    exc_info=e
                )
