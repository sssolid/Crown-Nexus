# app/core/error/base.py
from __future__ import annotations

"""
Base interfaces and types for the error handling system.

This module defines common types, protocols, and interfaces
used throughout the error handling components.
"""

from typing import Any, Dict, List, Optional, Protocol, TypeVar, Union

from pydantic import BaseModel, Field

from app.logging.context import get_logger

logger = get_logger("app.core.error.base")

F = TypeVar("F")
T = TypeVar("T")


class ErrorContext(BaseModel):
    """
    Context information for error reporting.

    Contains details about where and how an error occurred, including
    function information, arguments, and request context.
    """

    function: str = Field(
        ..., description="Name of the function where the error occurred"
    )
    args: Optional[List[Any]] = Field(
        None, description="Positional arguments to the function"
    )
    kwargs: Optional[Dict[str, Any]] = Field(
        None, description="Keyword arguments to the function"
    )
    user_id: Optional[str] = Field(
        None, description="ID of the user who triggered the error"
    )
    request_id: Optional[str] = Field(
        None, description="ID of the request that triggered the error"
    )

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"


class ErrorReporter(Protocol):
    """
    Protocol for error reporters.

    Error reporters are responsible for reporting errors to various
    destinations (logs, databases, external services, etc.).
    """

    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        """
        Report an error with context information.

        Args:
            exception: The exception to report
            context: Context information about the error
        """
        ...


class ErrorHandler(Protocol):
    """
    Protocol for error handlers.

    Error handlers are responsible for handling errors and performing
    appropriate actions (logging, notifying, etc.).
    """

    async def handle_error(self, exception: Exception, context: ErrorContext) -> Any:
        """
        Handle an error with context information.

        Args:
            exception: The exception to handle
            context: Context information about the error

        Returns:
            Any result from handling the error
        """
        ...


class ErrorLogEntry(BaseModel):
    """
    Model for storing error log entries.

    Contains detailed information about an error occurrence for
    storage in logs or databases.
    """

    error_id: str = Field(..., description="Unique ID for the error")
    timestamp: str = Field(..., description="Timestamp when the error occurred")
    error_type: str = Field(..., description="Type of the exception")
    error_message: str = Field(..., description="Error message")
    function: str = Field(..., description="Function where the error occurred")
    traceback: List[str] = Field(..., description="Error traceback")
    user_id: Optional[str] = Field(
        None, description="ID of the user who triggered the error"
    )
    request_id: Optional[str] = Field(
        None, description="ID of the request that triggered the error"
    )
    context: Dict[str, Any] = Field(
        default_factory=dict, description="Additional context information"
    )

    class Config:
        extra = "allow"
