# app/core/error/manager.py
from __future__ import annotations

"""
Core error handling functionality.

This module provides the main error handling functions for reporting errors
and creating standardized exceptions throughout the application.
"""

import asyncio
import functools
import inspect
import traceback
from typing import Any, Callable, Dict, List, Optional, TypeVar, cast, Union

from app.core.exceptions import (
    BusinessException,
    ErrorCode,
    PermissionDeniedException,
    ResourceAlreadyExistsException,
    ResourceNotFoundException,
    ValidationException,
)
from app.logging.context import get_logger
from app.core.error.base import ErrorContext, ErrorReporter
from app.core.error.factory import ErrorReporterFactory

logger = get_logger("app.core.error.manager")

T = TypeVar("T")

# Global list of error reporters
_reporters: List[ErrorReporter] = []
_initialized: bool = False


def register_reporter(reporter: ErrorReporter) -> None:
    """
    Register an error reporter.

    Args:
        reporter: The error reporter to register
    """
    _reporters.append(reporter)
    logger.debug(f"Registered error reporter: {reporter.__class__.__name__}")


async def report_error(exception: Exception, context: ErrorContext) -> None:
    """
    Report an error using all registered reporters.

    Args:
        exception: The exception to report
        context: Context information about the error
    """
    for reporter in _reporters:
        try:
            await reporter.report_error(exception, context)
        except Exception as e:
            logger.error(f"Error reporter failed: {str(e)}", exc_info=e)


def resource_not_found(
    resource_type: str, resource_id: str, message: Optional[str] = None
) -> ResourceNotFoundException:
    """
    Create a resource not found exception.

    Args:
        resource_type: Type of resource that was not found
        resource_id: ID of the resource that was not found
        message: Optional custom error message

    Returns:
        A configured ResourceNotFoundException
    """
    return ResourceNotFoundException(
        resource_type=resource_type,
        resource_id=resource_id,
        message=message,
        original_exception=None,
    )


def resource_already_exists(
    resource_type: str,
    identifier: str,
    field: str = "id",
    message: Optional[str] = None,
) -> ResourceAlreadyExistsException:
    """
    Create a resource already exists exception.

    Args:
        resource_type: Type of resource that already exists
        identifier: Identifier of the resource
        field: Field name of the identifier (default: 'id')
        message: Optional custom error message

    Returns:
        A configured ResourceAlreadyExistsException
    """
    return ResourceAlreadyExistsException(
        resource_type=resource_type,
        identifier=identifier,
        field=field,
        message=message,
        original_exception=None,
    )


def validation_error(
    field: str, message: str, error_type: str = "invalid_value"
) -> ValidationException:
    """
    Create a validation error exception.

    Args:
        field: Field that failed validation
        message: Error message
        error_type: Type of validation error

    Returns:
        A configured ValidationException
    """
    return ValidationException(
        message=f"Validation error: {message}",
        errors=[{"loc": [field], "msg": message, "type": error_type}],
        original_exception=None,
    )


def permission_denied(
    action: str, resource_type: str, permission: str
) -> PermissionDeniedException:
    """
    Create a permission denied exception.

    Args:
        action: Action that was attempted
        resource_type: Type of resource being accessed
        permission: Permission that was required

    Returns:
        A configured PermissionDeniedException
    """
    return PermissionDeniedException(
        message=f"Permission denied to {action} {resource_type}",
        action=action,
        resource_type=resource_type,
        permission=permission,
        original_exception=None,
    )


def business_logic_error(
    message: str, details: Optional[Dict[str, Any]] = None
) -> BusinessException:
    """
    Create a business logic error exception.

    Args:
        message: Error message
        details: Additional error details

    Returns:
        A configured BusinessException
    """
    return BusinessException(
        message=message,
        code=ErrorCode.BUSINESS_LOGIC_ERROR,
        details=details or {},
        status_code=400,
        original_exception=None,
    )


def ensure_not_none(
    value: Optional[T],
    resource_type: str,
    resource_id: str,
    message: Optional[str] = None,
) -> T:
    """
    Ensure a value is not None, raising an exception if it is.

    Args:
        value: Value to check
        resource_type: Type of resource being checked
        resource_id: ID of the resource being checked
        message: Optional custom error message

    Returns:
        The value, if it is not None

    Raises:
        ResourceNotFoundException: If the value is None
    """
    if value is None:
        raise resource_not_found(resource_type, resource_id, message)
    return value


def create_error_context(
    function_name: Optional[str] = None,
    args: Optional[List[Any]] = None,
    kwargs: Optional[Dict[str, Any]] = None,
    user_id: Optional[str] = None,
    request_id: Optional[str] = None,
) -> ErrorContext:
    """
    Create an error context from the current call frame.

    Args:
        function_name: Optional name of the function
        args: Optional positional arguments
        kwargs: Optional keyword arguments
        user_id: Optional user ID
        request_id: Optional request ID

    Returns:
        A configured ErrorContext
    """
    if function_name is None:
        frame = inspect.currentframe()
        if frame is not None:
            frame = frame.f_back
            if frame is not None:
                function_name = frame.f_code.co_name
                if args is None and kwargs is None:
                    arg_names = inspect.getargvalues(frame).args
                    locals_dict = frame.f_locals
                    args = [locals_dict[arg] for arg in arg_names if arg in locals_dict]
                    kwargs = {
                        k: v
                        for k, v in locals_dict.items()
                        if k not in arg_names and not k.startswith("__")
                    }

    function_name = function_name or "unknown_function"
    args = args or []
    kwargs = kwargs or {}

    return ErrorContext(
        function=function_name,
        args=args,
        kwargs=kwargs,
        user_id=user_id,
        request_id=request_id,
    )


def handle_exception(
    exception: Exception,
    request_id: Optional[str] = None,
    user_id: Optional[str] = None,
    function_name: Optional[str] = None,
) -> None:
    """
    Handle an exception by reporting it.

    Args:
        exception: The exception to handle
        request_id: Optional request ID
        user_id: Optional user ID
        function_name: Optional function name
    """
    frame = inspect.currentframe()
    if frame is not None and frame.f_back is not None:
        frame = frame.f_back
        function_name = function_name or frame.f_code.co_name
        arg_names = inspect.getargvalues(frame).args
        locals_dict = frame.f_locals
        args_values = [locals_dict[arg] for arg in arg_names if arg in locals_dict]
        kwargs_values = {
            k: v
            for k, v in locals_dict.items()
            if k not in arg_names and not k.startswith("__")
        }

        context = ErrorContext(
            function=function_name,
            args=args_values,
            kwargs=kwargs_values,
            user_id=user_id,
            request_id=request_id,
        )

        asyncio.create_task(report_error(exception, context))
    else:
        context = ErrorContext(
            function=function_name or "unknown_function",
            args=[],
            kwargs={},
            user_id=user_id,
            request_id=request_id,
        )

        asyncio.create_task(report_error(exception, context))


def error_context_decorator(
    user_id_param: Optional[str] = None, request_id_param: Optional[str] = None
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator that adds error handling to a function.

    Args:
        user_id_param: Optional parameter name for user ID
        request_id_param: Optional parameter name for request ID

    Returns:
        A decorator function
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            user_id = kwargs.get(user_id_param) if user_id_param else None
            request_id = kwargs.get(request_id_param) if request_id_param else None

            try:
                return await func(*args, **kwargs)
            except Exception as e:
                handle_exception(
                    exception=e,
                    request_id=request_id,
                    user_id=user_id,
                    function_name=func.__name__,
                )
                raise

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            user_id = kwargs.get(user_id_param) if user_id_param else None
            request_id = kwargs.get(request_id_param) if request_id_param else None

            try:
                return func(*args, **kwargs)
            except Exception as e:
                handle_exception(
                    exception=e,
                    request_id=request_id,
                    user_id=user_id,
                    function_name=func.__name__,
                )
                raise

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


async def initialize() -> None:
    """Initialize the error handling system."""
    global _reporters, _initialized

    if _initialized:
        logger.debug("Error handling system already initialized, skipping")
        return

    logger.info("Initializing error handling system")

    _reporters = []
    default_reporters = ErrorReporterFactory.create_default_reporters()
    for reporter in default_reporters:
        register_reporter(reporter)

    _initialized = True
    logger.info(f"Registered {len(default_reporters)} default error reporters")


async def shutdown() -> None:
    """Shut down the error handling system."""
    global _reporters, _initialized

    if not _initialized:
        return

    logger.info("Shutting down error handling system")
    _reporters = []
    _initialized = False
