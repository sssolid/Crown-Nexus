from __future__ import annotations
'Base interfaces and types for the error handling system.\n\nThis module defines common types, protocols, and interfaces\nused throughout the error handling components.\n'
from typing import Any, Dict, List, Optional, Protocol, TypeVar
from pydantic import BaseModel
F = TypeVar('F')
T = TypeVar('T')
class ErrorContext(BaseModel):
    function: str
    args: Optional[List[Any]] = None
    kwargs: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = None
    request_id: Optional[str] = None
class ErrorReporter(Protocol):
    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        ...