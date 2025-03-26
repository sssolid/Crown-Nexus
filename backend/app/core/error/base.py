from __future__ import annotations

"""Base interfaces and types for the error handling system.

This module defines common types, protocols, and interfaces
used throughout the error handling components.
"""

from typing import Any, Dict, List, Optional, Protocol, TypeVar, Union

from pydantic import BaseModel, Field

F = TypeVar("F")
T = TypeVar("T")


class ErrorContext(BaseModel):
    """Context information about where an error occurred."""

    function: str = Field(..., description="Name of the function where the error occurred")
    args: Optional[List[Any]] = Field(None, description="Positional arguments to the function")
    kwargs: Optional[Dict[str, Any]] = Field(None, description="Keyword arguments to the function")
    user_id: Optional[str] = Field(None, description="ID of the user who triggered the error")
    request_id: Optional[str] = Field(None, description="ID of the request that triggered the error")

    class Config:
        """Pydantic model configuration."""

        arbitrary_types_allowed = True
        extra = "allow"


class ErrorReporter(Protocol):
    """Protocol for error reporters.

    An error reporter is responsible for reporting errors to a specific destination
    such as logs, database, or external error reporting service.
    """

    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        """Report an error to the appropriate destination.

        Args:
            exception: The exception to report
            context: Context information about where the error occurred
        """
        ...


class ErrorHandler(Protocol):
    """Protocol for error handlers.

    An error handler is responsible for handling errors in a specific way,
    such as displaying an error page or returning an error response.
    """

    async def handle_error(
        self,
        exception: Exception,
        context: ErrorContext
    ) -> Any:
        """Handle an error in an appropriate way.

        Args:
            exception: The exception to handle
            context: Context information about where the error occurred

        Returns:
            Handler-specific response
        """
        ...


class ErrorLogEntry(BaseModel):
    """Model for storing error log entries."""

    error_id: str = Field(..., description="Unique ID for the error")
    timestamp: str = Field(..., description="Timestamp when the error occurred")
    error_type: str = Field(..., description="Type of the exception")
    error_message: str = Field(..., description="Error message")
    function: str = Field(..., description="Function where the error occurred")
    traceback: List[str] = Field(..., description="Error traceback")
    user_id: Optional[str] = Field(None, description="ID of the user who triggered the error")
    request_id: Optional[str] = Field(None, description="ID of the request that triggered the error")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context information")

    class Config:
        """Pydantic model configuration."""

        extra = "allow"
