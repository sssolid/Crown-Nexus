# app/logging/config.py
from __future__ import annotations

"""
Logging configuration module.

This module handles the configuration of the logging system, including
formatters, filters, and processors for both standard logging and structlog.
"""

import datetime
import logging
import logging.config
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import pythonjsonlogger.jsonlogger as pythonjsonlogger
import structlog
from structlog.stdlib import BoundLogger, LoggerFactory
from structlog.types import EventDict, Processor, WrappedLogger

from app.core.config import settings
from app.core.config.base import Environment

# Default to INFO if LOG_LEVEL isn't available in settings
DEFAULT_LOG_LEVEL = "INFO"

# Track initialization to prevent duplicate configuration
_logging_initialized = False

# Create a thread-local context for request tracking
# Defined here to avoid circular imports
import threading

_request_context = threading.local()


class RequestIdFilter(logging.Filter):
    """Filter for adding request ID to log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Add request ID to log record.

        Args:
            record: The log record to process

        Returns:
            bool: Always True to include the record
        """
        request_id = getattr(_request_context, "request_id", None)
        record.request_id = request_id or "no_request_id"
        return True


class UserIdFilter(logging.Filter):
    """Filter for adding user ID to log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Add user ID to log record.

        Args:
            record: The log record to process

        Returns:
            bool: Always True to include the record
        """
        user_id = getattr(_request_context, "user_id", None)
        record.user_id = user_id or "anonymous"
        return True


def add_request_id_processor(
    logger: WrappedLogger, method_name: str, event_dict: EventDict
) -> EventDict:
    """Add request ID to structured log event."""
    request_id = getattr(_request_context, "request_id", None)
    if request_id:
        event_dict["request_id"] = request_id
    else:
        event_dict["request_id"] = "no_request_id"
    return event_dict


def add_user_id_processor(
    logger: WrappedLogger, method_name: str, event_dict: EventDict
) -> EventDict:
    """Add user ID to structured log event."""
    user_id = getattr(_request_context, "user_id", None)
    if user_id:
        event_dict["user_id"] = user_id
    else:
        event_dict["user_id"] = "anonymous"
    return event_dict


def add_timestamp_processor(
    logger: WrappedLogger, method_name: str, event_dict: EventDict
) -> EventDict:
    """Add ISO format timestamp to structured log event."""
    event_dict["timestamp"] = datetime.datetime.now(datetime.UTC).isoformat() + "Z"
    return event_dict


def add_service_info_processor(
    logger: WrappedLogger, method_name: str, event_dict: EventDict
) -> EventDict:
    """Add service information to structured log event."""
    event_dict["service"] = settings.PROJECT_NAME
    event_dict["version"] = settings.VERSION
    event_dict["environment"] = settings.ENVIRONMENT.value
    return event_dict


class ConsoleRendererWithLineNumbers(structlog.dev.ConsoleRenderer):
    """Custom renderer that includes line numbers in colorized output."""

    def __call__(
        self, logger: logging.Logger, name: str, event_dict: Dict[str, Any]
    ) -> str:
        """Format the event dict with line numbers included."""
        # Extract line number and file information using the keys from CallsiteParameterAdder
        lineno = event_dict.pop("lineno", None)
        filename = event_dict.pop("filename", None)

        # Format using the parent class
        output = super().__call__(logger, name, event_dict)

        # If we have line number info, insert it after the logger name
        if lineno and filename:
            # Find the logger name in the output and append line info
            logger_name_end = (
                output.find("]", output.find("[", output.find("]") + 1)) + 1
            )
            if logger_name_end > 0:
                output = f"{output[:logger_name_end]}:{filename.split('/')[-1]}:{lineno}{output[logger_name_end:]}"

        return output


def configure_std_logging() -> None:
    """Configure standard Python logging."""
    # Get log level - check if the attribute exists and use default if not
    log_level_name = getattr(settings, "LOG_LEVEL", DEFAULT_LOG_LEVEL)
    if isinstance(log_level_name, str):
        log_level = getattr(logging, log_level_name, logging.INFO)
    else:
        log_level = logging.INFO

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Custom formatter that passes through structlog's formatted output
    class StructlogPassthroughFormatter(logging.Formatter):
        def format(self, record):
            # If the record was created by structlog, just return the message
            if hasattr(record, "_from_structlog") and record._from_structlog:
                return record.getMessage()
            # Otherwise format it normally
            return super().format(record)

    config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,  # Important to not disable existing loggers
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d [%(request_id)s] [%(user_id)s] - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "json": {
                "()": pythonjsonlogger.JsonFormatter,
                "fmt": "%(timestamp)s %(level)s %(name)s %(request_id)s %(user_id)s %(message)s %(pathname)s %(lineno)d %(funcName)s %(process)d %(thread)d",
                "rename_fields": {"levelname": "level", "asctime": "timestamp"},
            },
            "structlog": {
                "()": StructlogPassthroughFormatter,
            },
        },
        "filters": {
            "request_id": {"()": RequestIdFilter},
            "user_id": {"()": UserIdFilter},
        },
        "handlers": {
            "console": {
                "level": log_level,
                "class": "logging.StreamHandler",
                "formatter": (
                    "structlog"
                    if settings.ENVIRONMENT == Environment.DEVELOPMENT
                    else "json"
                ),
                "filters": ["request_id", "user_id"],
                "stream": sys.stdout,
            }
        },
        "loggers": {
            "app": {"handlers": ["console"], "level": log_level, "propagate": False},
            "uvicorn": {
                "handlers": ["console"],
                "level": log_level,
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
        "root": {"handlers": ["console"], "level": log_level},
    }

    # Add file handlers in non-development environments
    if settings.ENVIRONMENT != Environment.DEVELOPMENT:
        config["handlers"]["file"] = {
            "level": log_level,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(log_dir / "app.log"),
            "maxBytes": 10485760,  # 10MB
            "backupCount": 10,
            "formatter": "json",
            "filters": ["request_id", "user_id"],
        }

        config["handlers"]["error_file"] = {
            "level": logging.ERROR,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(log_dir / "error.log"),
            "maxBytes": 10485760,  # 10MB
            "backupCount": 10,
            "formatter": "json",
            "filters": ["request_id", "user_id"],
        }

        for logger_name in config["loggers"]:
            config["loggers"][logger_name]["handlers"].extend(["file", "error_file"])

        config["root"]["handlers"].extend(["file", "error_file"])

    logging.config.dictConfig(config)


def configure_structlog() -> None:
    """Configure structlog for structured logging."""
    shared_processors: List[Processor] = [
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.CallsiteParameterAdder(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        add_request_id_processor,
        add_user_id_processor,
        add_service_info_processor,
    ]

    # In development mode, use colored console renderer
    if settings.ENVIRONMENT == Environment.DEVELOPMENT:
        structlog.configure(
            processors=shared_processors
            + [
                ConsoleRendererWithLineNumbers(
                    colors=True
                )  # Use custom renderer with line numbers
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
    else:
        # In production mode, route through stdlib logging for proper formatting
        structlog.configure(
            processors=shared_processors
            + [
                structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )


def initialize_logging() -> None:
    """Initialize the logging system at import time."""
    global _logging_initialized

    if _logging_initialized:
        return

    configure_std_logging()
    configure_structlog()
    _logging_initialized = True

    # Get logger after initialization
    logger = get_logger("app.logging")
    logger.info(
        "Logging initialized",
        environment=settings.ENVIRONMENT.value,
        log_level=getattr(settings, "LOG_LEVEL", DEFAULT_LOG_LEVEL),
    )


async def reinitialize_logging() -> None:
    """
    Reinitialize the logging system asynchronously.

    This can be called from the lifespan to update logging configuration
    or reload settings if needed.
    """
    global _logging_initialized

    if not _logging_initialized:
        initialize_logging()
        return

    logger = get_logger("app.logging")
    logger.debug("Logging system already initialized")


async def shutdown_logging() -> None:
    """Shut down the logging system asynchronously."""
    global _logging_initialized

    if not _logging_initialized:
        return

    logger = get_logger("app.logging")
    logger.info("Shutting down logging system")

    logging.shutdown()
    _logging_initialized = False


def get_logger(name: str) -> BoundLogger:
    """
    Get a structured logger for the given name.

    Args:
        name: The name for the logger

    Returns:
        A structured logger instance
    """
    if not _logging_initialized:
        initialize_logging()

    return structlog.get_logger(name)


# Initialize logging at module load time
initialize_logging()
