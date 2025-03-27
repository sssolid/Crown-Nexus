from __future__ import annotations

"""Factory for creating error reporters.

This module provides a factory for creating different error reporters
based on configuration settings.
"""

from typing import Any, Dict, List, Optional
from app.core.config import settings
from app.core.logging import get_logger
from app.core.error.base import ErrorReporter
from app.core.error.reporters import (
    DatabaseErrorReporter,
    ExternalServiceReporter,
    LoggingErrorReporter,
)

logger = get_logger("app.core.error.factory")


class ErrorReporterFactory:
    """Factory for creating error reporters."""

    @classmethod
    def create_reporter(cls, reporter_type: str, **kwargs: Any) -> ErrorReporter:
        """Create an error reporter of the specified type.

        Args:
            reporter_type: Type of reporter to create ("logging", "database", or "external")
            **kwargs: Additional arguments to pass to the reporter constructor

        Returns:
            An ErrorReporter instance

        Raises:
            ValueError: If the reporter type is not supported
        """
        if reporter_type == "logging":
            return LoggingErrorReporter()
        elif reporter_type == "database":
            return DatabaseErrorReporter()
        elif reporter_type == "external":
            if "service_url" not in kwargs or "api_key" not in kwargs:
                raise ValueError("External reporter requires service_url and api_key")
            return ExternalServiceReporter(
                service_url=kwargs["service_url"], api_key=kwargs["api_key"]
            )
        else:
            logger.error(f"Unsupported error reporter type: {reporter_type}")
            raise ValueError(f"Unsupported error reporter type: {reporter_type}")

    @classmethod
    def create_default_reporters(cls) -> List[ErrorReporter]:
        """Create the default set of error reporters based on configuration settings.

        Returns:
            List of ErrorReporter instances
        """
        reporters: List[ErrorReporter] = [LoggingErrorReporter()]

        # Add database reporter if enabled
        if (
            hasattr(settings, "ERROR_DATABASE_REPORTING_ENABLED")
            and settings.ERROR_DATABASE_REPORTING_ENABLED
        ):
            reporters.append(DatabaseErrorReporter())

        # Add external reporter if enabled and configured
        if (
            hasattr(settings, "ERROR_EXTERNAL_REPORTING_ENABLED")
            and settings.ERROR_EXTERNAL_REPORTING_ENABLED
        ):
            if hasattr(settings, "ERROR_REPORTING_SERVICE_URL") and hasattr(
                settings, "ERROR_REPORTING_API_KEY"
            ):
                reporters.append(
                    ExternalServiceReporter(
                        service_url=settings.ERROR_REPORTING_SERVICE_URL,
                        api_key=settings.ERROR_REPORTING_API_KEY,
                    )
                )
            else:
                logger.warning(
                    "External error reporting enabled but service URL or API key not configured"
                )

        return reporters

    @classmethod
    def create_reporter_by_name(cls, reporter_name: str) -> Optional[ErrorReporter]:
        """Create an error reporter by name based on configuration settings.

        Args:
            reporter_name: Name of the reporter to create

        Returns:
            An ErrorReporter instance or None if the reporter is not configured
        """
        if reporter_name == "logging":
            return LoggingErrorReporter()

        elif reporter_name == "database":
            if (
                hasattr(settings, "ERROR_DATABASE_REPORTING_ENABLED")
                and settings.ERROR_DATABASE_REPORTING_ENABLED
            ):
                return DatabaseErrorReporter()
            else:
                logger.warning(
                    "Database error reporting requested but not enabled in settings"
                )

        elif reporter_name == "external":
            if (
                hasattr(settings, "ERROR_EXTERNAL_REPORTING_ENABLED")
                and settings.ERROR_EXTERNAL_REPORTING_ENABLED
            ):
                if hasattr(settings, "ERROR_REPORTING_SERVICE_URL") and hasattr(
                    settings, "ERROR_REPORTING_API_KEY"
                ):
                    return ExternalServiceReporter(
                        service_url=settings.ERROR_REPORTING_SERVICE_URL,
                        api_key=settings.ERROR_REPORTING_API_KEY,
                    )
                else:
                    logger.warning(
                        "External error reporting requested but service URL or API key not configured"
                    )
            else:
                logger.warning(
                    "External error reporting requested but not enabled in settings"
                )

        else:
            logger.warning(f"Unknown error reporter name: {reporter_name}")

        return None
