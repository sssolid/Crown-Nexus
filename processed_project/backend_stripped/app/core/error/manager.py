from __future__ import annotations
'Core error handling functionality.\n\nThis module provides the main error handling functions for reporting errors\nand creating standardized exceptions throughout the application.\n'
import asyncio
import inspect
from typing import Any, Dict, List, Optional, TypeVar
from app.core.exceptions import AppException, AuthenticationException, BusinessException, ErrorCode, PermissionDeniedException, ResourceAlreadyExistsException, ResourceNotFoundException, ValidationException
from app.core.logging import get_logger
from app.core.error.base import ErrorContext, ErrorReporter
from app.core.error.factory import ErrorReporterFactory
logger = get_logger('app.core.error.manager')
T = TypeVar('T')
_reporters: List[ErrorReporter] = []
def register_reporter(reporter: ErrorReporter) -> None:
    _reporters.append(reporter)
    logger.debug(f'Registered error reporter: {reporter.__class__.__name__}')
async def report_error(exception: Exception, context: ErrorContext) -> None:
    for reporter in _reporters:
        try:
            await reporter.report_error(exception, context)
        except Exception as e:
            logger.error(f'Error reporter failed: {str(e)}', exc_info=e)
def resource_not_found(resource_type: str, resource_id: str, message: Optional[str]=None) -> ResourceNotFoundException:
    return ResourceNotFoundException(resource_type=resource_type, resource_id=resource_id, message=message, original_exception=None)
def resource_already_exists(resource_type: str, identifier: str, field: str='id', message: Optional[str]=None) -> ResourceAlreadyExistsException:
    return ResourceAlreadyExistsException(resource_type=resource_type, identifier=identifier, field=field, message=message, original_exception=None)
def validation_error(field: str, message: str, error_type: str='invalid_value') -> ValidationException:
    return ValidationException(message=f'Validation error: {message}', errors=[{'loc': [field], 'msg': message, 'type': error_type}], original_exception=None)
def permission_denied(action: str, resource_type: str, permission: str) -> PermissionDeniedException:
    return PermissionDeniedException(message=f'Permission denied to {action} {resource_type}', action=action, resource_type=resource_type, permission=permission, original_exception=None)
def business_logic_error(message: str, details: Optional[Dict[str, Any]]=None) -> BusinessException:
    return BusinessException(message=message, code=ErrorCode.BUSINESS_LOGIC_ERROR, details=details or {}, status_code=400, original_exception=None)
def ensure_not_none(value: Optional[T], resource_type: str, resource_id: str, message: Optional[str]=None) -> T:
    if value is None:
        raise resource_not_found(resource_type, resource_id, message)
    return value
def handle_exception(exception: Exception, request_id: Optional[str]=None) -> None:
    frame = inspect.currentframe()
    if frame is not None:
        frame = frame.f_back
    if frame is not None:
        function_name = frame.f_code.co_name
        args = inspect.getargvalues(frame).args
        locals_dict = frame.f_locals
        args_values = [locals_dict[arg] for arg in args if arg in locals_dict]
        kwargs_values = {k: v for k, v in locals_dict.items() if k not in args and (not k.startswith('__'))}
        context = ErrorContext(function=function_name, args=args_values, kwargs=kwargs_values, request_id=request_id)
        asyncio.create_task(report_error(exception, context))
async def initialize() -> None:
    logger.info('Initializing error handling system')
    global _reporters
    _reporters = []
    default_reporters = ErrorReporterFactory.create_default_reporters()
    for reporter in default_reporters:
        register_reporter(reporter)
    logger.info(f'Registered {len(default_reporters)} default error reporters')
async def shutdown() -> None:
    logger.info('Shutting down error handling system')
    global _reporters
    _reporters = []