"""Logging configuration for the Crown Nexus deployment system."""
from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List, Union

import structlog
from structlog.types import Processor


def configure_logging(
    log_level: int = logging.INFO,
    log_file: Optional[Union[str, Path]] = None,
    json_format: bool = True,
) -> None:
    """
    Configure structured logging for the application.

    Args:
        log_level: The logging level (default: INFO)
        log_file: Optional file path to write logs to
        json_format: Whether to use JSON format for logs (default: True)
    """
    # Set up processors for structlog
    processors: List[Processor] = [
        structlog.stdlib.filter_by_level,
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    # Add format-specific processors
    if json_format:
        processors.extend([
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ])
    else:
        processors.extend([
            structlog.dev.ConsoleRenderer(colors=sys.stdout.isatty())
        ])

    # Configure the stdlib logging
    handlers: List[logging.Handler] = [logging.StreamHandler()]

    # Add file handler if specified
    if log_file:
        path = Path(log_file) if isinstance(log_file, str) else log_file
        path.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(path))

    # Basic configuration for stdlib logging
    logging.basicConfig(
        format="%(message)s",
        level=log_level,
        handlers=handlers,
    )

    # Configure structlog
    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: Optional[str] = None) -> structlog.BoundLogger:
    """
    Get a configured structured logger.

    Args:
        name: Optional name for the logger

    Returns:
        A structured logger instance
    """
    return structlog.get_logger(name)
