from __future__ import annotations
'Base interfaces and types for the validation system.\n\nThis module defines common types, protocols, and interfaces\nused throughout the validation components.\n'
from typing import Any, Callable, Dict, List, Optional, Protocol, TypeVar, Union
from pydantic import BaseModel
T = TypeVar('T')
R = TypeVar('R', bound=bool)
class ValidationResult(BaseModel):
    is_valid: bool
    errors: List[Dict[str, Any]] = []
    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0
class Validator(Protocol):
    def validate(self, value: Any, **kwargs: Any) -> ValidationResult:
        ...
class ValidatorFactory(Protocol):
    def create_validator(self, validator_type: str, **options: Any) -> Validator:
        ...