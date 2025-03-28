from __future__ import annotations
'\nError reporter implementations.\n\nThis module provides different implementations of the ErrorReporter protocol\nfor reporting errors to various destinations.\n'
import json
import traceback
import uuid
from datetime import datetime
from typing import Any, Dict, Optional
import httpx
from app.core.error.base import ErrorContext, ErrorReporter, ErrorLogEntry
from app.logging.context import get_logger
logger = get_logger('app.core.error.reporters')
class LoggingErrorReporter(ErrorReporter):
    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        error_info = {'function': context.function, 'user_id': context.user_id, 'request_id': context.request_id, 'error_type': type(exception).__name__, 'error_message': str(exception)}
        logger.error(f'Error in {context.function}: {str(exception)}', exc_info=exception, user_id=context.user_id, request_id=context.request_id, args=repr(context.args) if context.args else None, kwargs=repr(context.kwargs) if context.kwargs else None, error_context=error_info)
class DatabaseErrorReporter(ErrorReporter):
    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        error_id = str(uuid.uuid4())
        timestamp = datetime.now(datetime.UTC).isoformat()
        error_entry = ErrorLogEntry(error_id=error_id, timestamp=timestamp, error_type=type(exception).__name__, error_message=str(exception), function=context.function, traceback=traceback.format_exception(type(exception), exception, exception.__traceback__), user_id=context.user_id, request_id=context.request_id, context={'args': context.args, 'kwargs': context.kwargs})
        try:
            logger.info(f'Database error reporter: Would store error {error_id} from {context.function}', error_entry=error_entry.model_dump())
        except Exception as e:
            logger.error(f'Failed to store error in database: {str(e)}', exc_info=e)
class ExternalServiceReporter(ErrorReporter):
    def __init__(self, service_url: str, api_key: str) -> None:
        self.service_url = service_url
        self.api_key = api_key
        self.headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'}
    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        error_data = {'error_id': str(uuid.uuid4()), 'timestamp': datetime.now(datetime.UTC).isoformat(), 'function': context.function, 'user_id': context.user_id, 'request_id': context.request_id, 'error_type': type(exception).__name__, 'error_message': str(exception), 'traceback': traceback.format_exception(type(exception), exception, exception.__traceback__), 'context': {'args': repr(context.args) if context.args else None, 'kwargs': repr(context.kwargs) if context.kwargs else None}}
        try:
            logger.info(f'External service reporter: Would send error to {self.service_url}', error_data=error_data, service_url=self.service_url)
        except Exception as e:
            logger.error(f'Failed to report error to external service: {str(e)}', exc_info=e)
class CompositeErrorReporter(ErrorReporter):
    def __init__(self, reporters: list[ErrorReporter]) -> None:
        self.reporters = reporters
    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        for reporter in self.reporters:
            try:
                await reporter.report_error(exception, context)
            except Exception as e:
                logger.error(f'Error in reporter {reporter.__class__.__name__}: {str(e)}', exc_info=e)