# /app/core/error/__init__.py
from __future__ import annotations

"""Error handling package for application-wide error handling.

This package provides core functionality for handling errors, reporting them to
various destinations, and creating standardized error responses.
"""

from app.core.error.base import ErrorContext, ErrorReporter
from app.core.error.factory import ErrorReporterFactory
from app.core.error.manager import (
    register_reporter,
    report_error,
    resource_not_found,
    resource_already_exists,
    validation_error,
    permission_denied,
    business_logic_error,
    ensure_not_none,
    handle_exception,
    initialize,
    shutdown,
)
from app.core.error.reporters import (
    LoggingErrorReporter,
    DatabaseErrorReporter,
    ExternalServiceReporter,
)

__all__ = [
    # Base types
    "ErrorContext",
    "ErrorReporter",
    # Factory
    "ErrorReporterFactory",
    # Core functions
    "register_reporter",
    "report_error",
    "resource_not_found",
    "resource_already_exists",
    "validation_error",
    "permission_denied",
    "business_logic_error",
    "ensure_not_none",
    "handle_exception",
    "initialize",
    "shutdown",
    # Reporter implementations
    "LoggingErrorReporter",
    "DatabaseErrorReporter",
    "ExternalServiceReporter",
]
