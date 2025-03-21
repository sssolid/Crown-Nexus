from __future__ import annotations
'Error reporter implementations.\n\nThis module provides different implementations of the ErrorReporter protocol\nfor reporting errors to various destinations.\n'
from typing import Any, Dict, Optional
from app.core.logging import get_logger
from app.core.error.base import ErrorContext, ErrorReporter
logger = get_logger('app.core.error.reporters')
class LoggingErrorReporter(ErrorReporter):
    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        logger.error(f'Error in {context.function}', exc_info=exception, extra={'user_id': context.user_id, 'request_id': context.request_id, 'args': context.args, 'kwargs': context.kwargs})
class DatabaseErrorReporter(ErrorReporter):
    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        logger.debug(f'Database error reporter: {str(exception)} in {context.function}')
class ExternalServiceReporter(ErrorReporter):
    def __init__(self, service_url: str, api_key: str) -> None:
        self.service_url = service_url
        self.api_key = api_key
    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        logger.debug(f'External service reporter: {str(exception)} in {context.function}')