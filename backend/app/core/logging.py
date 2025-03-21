# backend/app/core/logging.py

from __future__ import annotations

import logging
import logging.config
import sys
import threading
import uuid
from contextlib import contextmanager
import datetime
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, TypeVar, cast, Union

import pythonjsonlogger
import structlog
from pythonjsonlogger import jsonlogger
from structlog.stdlib import BoundLogger
from structlog.types import EventDict, Processor, WrappedLogger

from app.core.config.base import Environment, LogLevel

# Type variables for function signatures
F = TypeVar("F", bound=Callable[..., Any])
T = TypeVar("T")

# Thread-local storage for request context
_request_context = threading.local()


class RequestIdFilter(logging.Filter):
    """
    Log filter that adds request_id from thread-local storage.

    This filter adds the current request ID to log records if available.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Add request_id to log record if available.

        Args:
            record: Log record to modify

        Returns:
            True to include the record
        """
        request_id = getattr(_request_context, "request_id", None)
        record.request_id = request_id or "no_request_id"
        return True


class UserIdFilter(logging.Filter):
    """
    Log filter that adds user_id from thread-local storage.

    This filter adds the current user ID to log records if available.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Add user_id to log record if available.

        Args:
            record: Log record to modify

        Returns:
            True to include the record
        """
        user_id = getattr(_request_context, "user_id", None)
        record.user_id = user_id or "anonymous"
        return True


def add_request_id_processor(
    logger: WrappedLogger, method_name: str, event_dict: EventDict
) -> EventDict:
    """
    Structlog processor that adds request_id from thread-local storage.

    Args:
        logger: Logger instance
        method_name: Method name being called
        event_dict: Event dictionary to modify

    Returns:
        Modified event dictionary
    """
    request_id = getattr(_request_context, "request_id", None)
    if request_id:
        event_dict["request_id"] = request_id
    return event_dict


def add_user_id_processor(
    logger: WrappedLogger, method_name: str, event_dict: EventDict
) -> EventDict:
    """
    Structlog processor that adds user_id from thread-local storage.

    Args:
        logger: Logger instance
        method_name: Method name being called
        event_dict: Event dictionary to modify

    Returns:
        Modified event dictionary
    """
    user_id = getattr(_request_context, "user_id", None)
    if user_id:
        event_dict["user_id"] = user_id
    return event_dict


def add_timestamp_processor(
    logger: WrappedLogger, method_name: str, event_dict: EventDict
) -> EventDict:
    """
    Structlog processor that adds timestamp to log events.

    Args:
        logger: Logger instance
        method_name: Method name being called
        event_dict: Event dictionary to modify

    Returns:
        Modified event dictionary
    """
    event_dict["timestamp"] = datetime.datetime.now(datetime.UTC).isoformat() + "Z"
    return event_dict


def add_service_info_processor(
    logger: WrappedLogger, method_name: str, event_dict: EventDict
) -> EventDict:
    """
    Structlog processor that adds service information to log events.

    Args:
        logger: Logger instance
        method_name: Method name being called
        event_dict: Event dictionary to modify

    Returns:
        Modified event dictionary
    """
    event_dict["service"] = settings.PROJECT_NAME
    event_dict["version"] = settings.VERSION
    event_dict["environment"] = settings.ENVIRONMENT.value
    return event_dict


def configure_std_logging() -> None:
    """
    Configure standard library logging with appropriate handlers and formatters.

    This sets up log handlers based on environment and configuration settings.
    """
    log_level_name = getattr(settings.logging, "LOG_LEVEL", LogLevel.INFO).value
    log_level = getattr(logging, log_level_name, logging.INFO)

    # Create logging directory if needed
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Base configuration
    config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d [%(request_id)s] [%(user_id)s] - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "json": {
                "()": pythonjsonlogger.json,
                "fmt": "%(timestamp)s %(level)s %(name)s %(request_id)s %(user_id)s %(message)s %(pathname)s %(lineno)d %(funcName)s %(process)d %(thread)d",
                "rename_fields": {
                    "levelname": "level",
                    "asctime": "timestamp",
                },
            },
        },
        "filters": {
            "request_id": {
                "()": RequestIdFilter,
            },
            "user_id": {
                "()": UserIdFilter,
            },
        },
        "handlers": {
            "console": {
                "level": log_level,
                "class": "logging.StreamHandler",
                "formatter": (
                    "standard"
                    if settings.ENVIRONMENT != Environment.PRODUCTION
                    else "json"
                ),
                "filters": ["request_id", "user_id"],
                "stream": sys.stdout,
            },
        },
        "loggers": {
            "app": {
                "handlers": ["console"],
                "level": log_level,
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["console"],
                "level": log_level,
                "propagate": False,
            },
            "fitment": {
                "handlers": ["console"],
                "level": getattr(
                    logging, settings.fitment.FITMENT_LOG_LEVEL, logging.INFO
                ),
                "propagate": False,
            },
            "sqlalchemy.engine": {
                "handlers": ["console"],
                "level": (
                    logging.INFO
                    if settings.ENVIRONMENT == Environment.DEVELOPMENT
                    else logging.WARNING
                ),
                "propagate": False,
            },
        },
        "root": {
            "handlers": ["console"],
            "level": log_level,
        },
    }

    # Add file handlers for non-development environments
    if settings.ENVIRONMENT != Environment.DEVELOPMENT:
        # Add rotating file handler for regular logs
        config["handlers"]["file"] = {
            "level": log_level,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(log_dir / "app.log"),
            "maxBytes": 10485760,  # 10 MB
            "backupCount": 10,
            "formatter": "json",
            "filters": ["request_id", "user_id"],
        }

        # Add rotating file handler for errors
        config["handlers"]["error_file"] = {
            "level": logging.ERROR,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(log_dir / "error.log"),
            "maxBytes": 10485760,  # 10 MB
            "backupCount": 10,
            "formatter": "json",
            "filters": ["request_id", "user_id"],
        }

        # Update handlers for loggers
        for logger_name in config["loggers"]:
            config["loggers"][logger_name]["handlers"].extend(["file", "error_file"])
        config["root"]["handlers"].extend(["file", "error_file"])

    # Apply configuration
    logging.config.dictConfig(config)


def configure_structlog() -> None:
    """
    Configure structlog with processors and renderers.

    This sets up structlog to work alongside the standard library logging,
    with consistent formatting and context handling.
    """
    shared_processors: List[Processor] = [
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        add_request_id_processor,
        add_user_id_processor,
        add_service_info_processor,
    ]

    # Configure structlog based on environment
    if settings.ENVIRONMENT == Environment.DEVELOPMENT:
        # Development: pretty console output
        structlog.configure(
            processors=shared_processors
            + [
                structlog.dev.ConsoleRenderer(colors=True),
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        # Production: JSON output through stdlib logging
        structlog.configure(
            processors=shared_processors
            + [
                structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )


def setup_logging() -> None:
    """
    Set up the logging system.

    This function should be called early in the application startup process
    to configure all logging components.
    """
    # Configure standard library logging
    configure_std_logging()

    # Configure structlog
    configure_structlog()

    # Log startup message
    logger = get_logger("app.core.logging")
    logger.info(
        f"Logging initialized",
        environment=settings.ENVIRONMENT.value,
        log_level=settings.logging.LOG_LEVEL.value,
    )


def get_logger(name: str) -> BoundLogger:
    """
    Get a structlog logger instance.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Structured logger instance
    """
    return cast(BoundLogger, structlog.get_logger(name))


@contextmanager
def request_context(request_id: Optional[str] = None, user_id: Optional[str] = None):
    """
    Context manager for tracking request context in logs.

    Args:
        request_id: Request ID (generated if not provided)
        user_id: User ID (optional)

    Yields:
        The request_id
    """
    # Generate or use provided request ID
    _request_id = request_id or str(uuid.uuid4())

    # Store in thread-local storage
    old_request_id = getattr(_request_context, "request_id", None)
    old_user_id = getattr(_request_context, "user_id", None)

    _request_context.request_id = _request_id
    if user_id:
        _request_context.user_id = user_id

    try:
        yield _request_id
    finally:
        # Restore previous values or clear
        if old_request_id:
            _request_context.request_id = old_request_id
        else:
            delattr(_request_context, "request_id")

        if user_id:
            if old_user_id:
                _request_context.user_id = old_user_id
            else:
                delattr(_request_context, "user_id")


def set_user_id(user_id: str) -> None:
    """
    Set the current user ID in the logging context.

    Args:
        user_id: User ID to set
    """
    _request_context.user_id = user_id


def clear_user_id() -> None:
    """Clear the current user ID from the logging context."""
    if hasattr(_request_context, "user_id"):
        delattr(_request_context, "user_id")


def log_execution_time(logger: Optional[BoundLogger] = None, level: str = "info"):
    """
    Decorator to log function execution time.

    Args:
        logger: Logger to use (created from function name if not provided)
        level: Log level to use ("debug", "info", etc.)

    Returns:
        Decorated function
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Get or create logger
            log = logger or get_logger(func.__module__)
            log_method = getattr(log, level)

            # Log start and execute function
            start_time = datetime.datetime.now()
            log_method(f"{func.__name__} started")

            try:
                result = func(*args, **kwargs)

                # Log completion time
                execution_time = (datetime.datetime.now() - start_time).total_seconds()
                log_method(
                    f"{func.__name__} completed",
                    execution_time=execution_time,
                )

                return result
            except Exception as e:
                # Log exception
                execution_time = (datetime.datetime.now() - start_time).total_seconds()
                log.exception(
                    f"{func.__name__} failed",
                    error=str(e),
                    execution_time=execution_time,
                )
                raise

        return cast(F, wrapper)

    return decorator


def log_execution_time_async(logger: Optional[BoundLogger] = None, level: str = "info"):
    """
    Decorator to log async function execution time.

    Args:
        logger: Logger to use (created from function name if not provided)
        level: Log level to use ("debug", "info", etc.)

    Returns:
        Decorated async function
    """

    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Get or create logger
            log = logger or get_logger(func.__module__)
            log_method = getattr(log, level)

            # Log start and execute function
            start_time = datetime.datetime.now()
            log_method(f"{func.__name__} started")

            try:
                result = await func(*args, **kwargs)

                # Log completion time
                execution_time = (datetime.datetime.now() - start_time).total_seconds()
                log_method(
                    f"{func.__name__} completed",
                    execution_time=execution_time,
                )

                return result
            except Exception as e:
                # Log exception
                execution_time = (datetime.datetime.now() - start_time).total_seconds()
                log.exception(
                    f"{func.__name__} failed",
                    error=str(e),
                    execution_time=execution_time,
                )
                raise

        return cast(F, wrapper)

    return decorator
