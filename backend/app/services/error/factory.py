# /app/services/error/factory.py
from __future__ import annotations

"""Factory for creating error reporters.

This module provides a factory for creating different error reporters
based on configuration settings.
"""

from typing import Any, Dict, List, Optional

from app.core.config import settings
from app.core.logging import get_logger
from app.services.error.base import ErrorReporter
from app.services.error.reporters import (
    DatabaseErrorReporter,
    ExternalServiceReporter,
    LoggingErrorReporter,
)

logger = get_logger("app.services.error.factory")


class ErrorReporterFactory:
    """Factory for creating and managing error reporters."""

    @classmethod
    def create_reporter(cls, reporter_type: str, **kwargs: Any) -> ErrorReporter:
        """Create an error reporter of the specified type.

        Args:
            reporter_type: Type of reporter to create ('logging', 'database', 'external')
            **kwargs: Additional arguments for the reporter

        Returns:
            An instance of the specified reporter

        Raises:
            ValueError: If reporter type is not supported
        """
        if reporter_type == "logging":
            return LoggingErrorReporter()
        elif reporter_type == "database":
            return DatabaseErrorReporter()
        elif reporter_type == "external":
            if "service_url" not in kwargs or "api_key" not in kwargs:
                raise ValueError("External reporter requires service_url and api_key")
            return ExternalServiceReporter(
                service_url=kwargs["service_url"],
                api_key=kwargs["api_key"]
            )
        else:
            logger.error(f"Unsupported error reporter type: {reporter_type}")
            raise ValueError(f"Unsupported error reporter type: {reporter_type}")

    @classmethod
    def create_default_reporters(cls) -> List[ErrorReporter]:
        """Create the default set of error reporters based on application settings.

        Returns:
            List of default error reporters
        """
        reporters: List[ErrorReporter] = [LoggingErrorReporter()]

        # Add additional reporters based on configuration
        if hasattr(settings, "ERROR_DATABASE_REPORTING_ENABLED") and settings.ERROR_DATABASE_REPORTING_ENABLED:
            reporters.append(DatabaseErrorReporter())

        if hasattr(settings, "ERROR_EXTERNAL_REPORTING_ENABLED") and settings.ERROR_EXTERNAL_REPORTING_ENABLED:
            if hasattr(settings, "ERROR_REPORTING_SERVICE_URL") and hasattr(settings, "ERROR_REPORTING_API_KEY"):
                reporters.append(ExternalServiceReporter(
                    service_url=settings.ERROR_REPORTING_SERVICE_URL,
                    api_key=settings.ERROR_REPORTING_API_KEY
                ))
            else:
                logger.warning("External error reporting enabled but service URL or API key not configured")

        return reporters
