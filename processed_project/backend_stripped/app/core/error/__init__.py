from __future__ import annotations
'Error handling package for application-wide error handling.\n\nThis package provides core functionality for handling errors, reporting them to\nvarious destinations, and creating standardized error responses.\n'
from app.core.error.base import ErrorContext, ErrorReporter
from app.core.error.factory import ErrorReporterFactory
from app.core.error.manager import register_reporter, report_error, resource_not_found, resource_already_exists, validation_error, permission_denied, business_logic_error, ensure_not_none, handle_exception, initialize, shutdown
from app.core.error.reporters import LoggingErrorReporter, DatabaseErrorReporter, ExternalServiceReporter
__all__ = ['ErrorContext', 'ErrorReporter', 'ErrorReporterFactory', 'register_reporter', 'report_error', 'resource_not_found', 'resource_already_exists', 'validation_error', 'permission_denied', 'business_logic_error', 'ensure_not_none', 'handle_exception', 'initialize', 'shutdown', 'LoggingErrorReporter', 'DatabaseErrorReporter', 'ExternalServiceReporter']