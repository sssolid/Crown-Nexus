from __future__ import annotations
from typing import Any, Dict, Optional
class FitmentError(Exception):
    def __init__(self, message: str, details: Optional[Dict[str, Any]]=None) -> None:
        self.message = message
        self.details = details or {}
        super().__init__(message)
class ParsingError(FitmentError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]]=None) -> None:
        super().__init__(message, details)
class ValidationError(FitmentError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]]=None) -> None:
        super().__init__(message, details)
class MappingError(FitmentError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]]=None) -> None:
        super().__init__(message, details)
class DatabaseError(FitmentError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]]=None) -> None:
        super().__init__(message, details)
class ConfigurationError(FitmentError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]]=None) -> None:
        super().__init__(message, details)