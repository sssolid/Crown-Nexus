# app/logging/__init__.py
from __future__ import annotations

"""
Logging system for the application.

This package provides a centralized, configurable logging system with
structured logs, context tracking, and integration with FastAPI.
"""

from app.logging.config import (
    get_logger,
    initialize_logging,
    reinitialize_logging,
    shutdown_logging,
)
from app.logging.context import (
    clear_user_id,
    log_execution_time,
    log_execution_time_async,
    request_context,
    set_user_id,
)

__all__ = [
    "initialize_logging",
    "reinitialize_logging",
    "shutdown_logging",
    "get_logger",
    "request_context",
    "set_user_id",
    "clear_user_id",
    "log_execution_time",
    "log_execution_time_async",
]
