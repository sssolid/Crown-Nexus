from __future__ import annotations
'\nError handling service implementation.\n\nThis module provides a service wrapper around the error handling system,\nmaking it available through the dependency manager.\n'
from typing import Any, Dict, List, Optional, Type
from app.core.error.base import ErrorContext, ErrorReporter
from app.core.error.factory import ErrorReporterFactory
from app.core.error.manager import business_logic_error, handle_exception, initialize as initialize_manager, permission_denied, register_reporter, report_error, resource_already_exists, resource_not_found, shutdown as shutdown_manager, validation_error
from app.core.error.reporters import CompositeErrorReporter, DatabaseErrorReporter, ExternalServiceReporter, LoggingErrorReporter
from app.logging.context import get_logger
logger = get_logger('app.core.error.service')
class ErrorService:
    def __init__(self) -> None:
        self.reporters: List[ErrorReporter] = []
        self._initialized = False
    async def initialize(self) -> None:
        if self._initialized:
            logger.debug('Error service already initialized, skipping')
            return
        logger.info('Initializing error service')
        await initialize_manager()
        self.reporters = ErrorReporterFactory.create_default_reporters()
        for reporter in self.reporters:
            register_reporter(reporter)
        self._initialized = True
        logger.info(f'Registered {len(self.reporters)} default error reporters')
    async def shutdown(self) -> None:
        if not self._initialized:
            return
        logger.info('Shutting down error service')
        await shutdown_manager()
        self.reporters = []
        self._initialized = False
    async def register_reporter(self, reporter: ErrorReporter) -> None:
        self.reporters.append(reporter)
        register_reporter(reporter)
        logger.debug(f'Registered error reporter: {reporter.__class__.__name__}')
    async def register_reporter_by_name(self, reporter_name: str) -> None:
        reporter = ErrorReporterFactory.create_reporter_by_name(reporter_name)
        if reporter:
            await self.register_reporter(reporter)
    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        await report_error(exception, context)
    def handle_exception(self, exception: Exception, request_id: Optional[str]=None, user_id: Optional[str]=None, function_name: Optional[str]=None) -> None:
        handle_exception(exception=exception, request_id=request_id, user_id=user_id, function_name=function_name)
    def resource_not_found(self, resource_type: str, resource_id: str, message: Optional[str]=None) -> Exception:
        return resource_not_found(resource_type, resource_id, message)
    def resource_already_exists(self, resource_type: str, identifier: str, field: str='id', message: Optional[str]=None) -> Exception:
        return resource_already_exists(resource_type, identifier, field, message)
    def validation_error(self, field: str, message: str, error_type: str='invalid_value') -> Exception:
        return validation_error(field, message, error_type)
    def permission_denied(self, action: str, resource_type: str, permission: str) -> Exception:
        return permission_denied(action, resource_type, permission)
    def business_logic_error(self, message: str, details: Optional[Dict[str, Any]]=None) -> Exception:
        return business_logic_error(message, details)
_error_service: Optional[ErrorService] = None
def get_error_service() -> ErrorService:
    global _error_service
    if _error_service is None:
        _error_service = ErrorService()
    return _error_service