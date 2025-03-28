from __future__ import annotations
'Base interfaces and types for the validation system.\n\nThis module defines common types, protocols, and interfaces\nused throughout the validation components.\n'
from typing import Any, Dict, List, Optional, Protocol, TypeVar, Union, runtime_checkable
from pydantic import BaseModel, Field
T = TypeVar('T')
R = TypeVar('R', bound=bool)
class ValidationResult(BaseModel):
    is_valid: bool = Field(..., description='Whether the validation passed')
    errors: List[Dict[str, Any]] = Field(default_factory=list, description='List of validation errors when validation fails')
    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0
    @property
    def error_messages(self) -> List[str]:
        return [error.get('msg', 'Unknown error') for error in self.errors]
    def add_error(self, msg: str, error_type: str, loc: Optional[Union[str, List[str]]]=None, **context: Any) -> None:
        error: Dict[str, Any] = {'msg': msg, 'type': error_type}
        if loc:
            if isinstance(loc, str):
                error['loc'] = [loc]
            else:
                error['loc'] = loc
        error.update(context)
        self.errors.append(error)
        self.is_valid = False
@runtime_checkable
class Validator(Protocol):
    def validate(self, value: Any, **kwargs: Any) -> ValidationResult:
        ...
    async def validate_async(self, value: Any, **kwargs: Any) -> ValidationResult:
        raise NotImplementedError('This validator does not support async validation')
@runtime_checkable
class ValidatorFactory(Protocol):
    def create_validator(self, validator_type: str, **options: Any) -> Validator:
        ...