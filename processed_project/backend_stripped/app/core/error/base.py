from __future__ import annotations
'\nBase interfaces and types for the error handling system.\n\nThis module defines common types, protocols, and interfaces\nused throughout the error handling components.\n'
from typing import Any, Dict, List, Optional, Protocol, TypeVar, Union
from pydantic import BaseModel, Field
from app.logging.context import get_logger
logger = get_logger('app.core.error.base')
F = TypeVar('F')
T = TypeVar('T')
class ErrorContext(BaseModel):
    function: str = Field(..., description='Name of the function where the error occurred')
    args: Optional[List[Any]] = Field(None, description='Positional arguments to the function')
    kwargs: Optional[Dict[str, Any]] = Field(None, description='Keyword arguments to the function')
    user_id: Optional[str] = Field(None, description='ID of the user who triggered the error')
    request_id: Optional[str] = Field(None, description='ID of the request that triggered the error')
    class Config:
        arbitrary_types_allowed = True
        extra = 'allow'
class ErrorReporter(Protocol):
    async def report_error(self, exception: Exception, context: ErrorContext) -> None:
        ...
class ErrorHandler(Protocol):
    async def handle_error(self, exception: Exception, context: ErrorContext) -> Any:
        ...
class ErrorLogEntry(BaseModel):
    error_id: str = Field(..., description='Unique ID for the error')
    timestamp: str = Field(..., description='Timestamp when the error occurred')
    error_type: str = Field(..., description='Type of the exception')
    error_message: str = Field(..., description='Error message')
    function: str = Field(..., description='Function where the error occurred')
    traceback: List[str] = Field(..., description='Error traceback')
    user_id: Optional[str] = Field(None, description='ID of the user who triggered the error')
    request_id: Optional[str] = Field(None, description='ID of the request that triggered the error')
    context: Dict[str, Any] = Field(default_factory=dict, description='Additional context information')
    class Config:
        extra = 'allow'