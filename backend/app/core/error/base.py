# /app/core/error/base.py
from __future__ import annotations

"""Base interfaces and types for the error handling system.

This module defines common types, protocols, and interfaces
used throughout the error handling components.
"""

from typing import Any, Dict, List, Optional, Protocol, TypeVar

from pydantic import BaseModel

F = TypeVar("F")  # Function type
T = TypeVar("T")  # Generic type


class ErrorContext(BaseModel):
    """Context information for error reporting."""

    function: str
    args: Optional[List[Any]] = None
    kwargs: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = None
    request_id: Optional[str] = None


class ErrorReporter(Protocol):
    """Protocol for error reporting implementations."""

    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        """Report an error to the appropriate system.

        Args:
            exception: The exception to report
            context: Context information about the error
        """
        ...
