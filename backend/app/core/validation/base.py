# /app/core/validation/base.py
from __future__ import annotations

"""Base interfaces and types for the validation system.

This module defines common types, protocols, and interfaces
used throughout the validation components.
"""

from typing import Any, Callable, Dict, List, Optional, Protocol, TypeVar, Union

from pydantic import BaseModel

# Type variables
T = TypeVar("T")  # Input type
R = TypeVar("R", bound=bool)  # Result type (usually bool)


class ValidationResult(BaseModel):
    """Result of a validation operation."""

    is_valid: bool
    errors: List[Dict[str, Any]] = []

    @property
    def has_errors(self) -> bool:
        """Check if there are any validation errors.

        Returns:
            bool: True if there are errors, False otherwise
        """
        return len(self.errors) > 0


class Validator(Protocol):
    """Protocol for validator implementations."""

    def validate(self, value: Any, **kwargs: Any) -> ValidationResult:
        """Validate a value.

        Args:
            value: The value to validate
            **kwargs: Additional validation parameters

        Returns:
            ValidationResult: The result of the validation
        """
        ...


class ValidatorFactory(Protocol):
    """Protocol for validator factory implementations."""

    def create_validator(self, validator_type: str, **options: Any) -> Validator:
        """Create a validator of the specified type.

        Args:
            validator_type: The type of validator to create
            **options: Configuration options for the validator

        Returns:
            Validator: An instance of the specified validator

        Raises:
            ValueError: If the validator type is not supported
        """
        ...
