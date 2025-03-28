from __future__ import annotations

"""Base interfaces and types for the validation system.

This module defines common types, protocols, and interfaces
used throughout the validation components.
"""

from typing import (
    Any,
    Dict,
    List,
    Optional,
    Protocol,
    TypeVar,
    Union,
    runtime_checkable,
)

from pydantic import BaseModel, Field

# Type variables for generic typing
T = TypeVar("T")
R = TypeVar("R", bound=bool)


class ValidationResult(BaseModel):
    """Result of a validation operation.

    This class represents the result of a validation operation, including
    whether the validation was successful and any validation errors.
    """

    is_valid: bool = Field(..., description="Whether the validation passed")
    errors: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="List of validation errors when validation fails",
    )

    @property
    def has_errors(self) -> bool:
        """Check if there are any validation errors.

        Returns:
            bool: True if there are errors, False otherwise
        """
        return len(self.errors) > 0

    @property
    def error_messages(self) -> List[str]:
        """Get a list of error messages.

        Returns:
            List[str]: List of error message strings
        """
        return [error.get("msg", "Unknown error") for error in self.errors]

    def add_error(
        self,
        msg: str,
        error_type: str,
        loc: Optional[Union[str, List[str]]] = None,
        **context: Any,
    ) -> None:
        """Add an error to the validation result.

        Args:
            msg: The error message
            error_type: The type of error
            loc: Optional location of the error (field name or path)
            **context: Additional context for the error
        """
        error: Dict[str, Any] = {"msg": msg, "type": error_type}

        if loc:
            if isinstance(loc, str):
                error["loc"] = [loc]
            else:
                error["loc"] = loc

        error.update(context)
        self.errors.append(error)
        self.is_valid = False


@runtime_checkable
class Validator(Protocol):
    """Protocol defining the interface for validators.

    Validators must implement the validate method, which takes a value
    and optional additional parameters and returns a ValidationResult.
    """

    def validate(self, value: Any, **kwargs: Any) -> ValidationResult:
        """Validate a value.

        Args:
            value: The value to validate
            **kwargs: Additional validation parameters

        Returns:
            ValidationResult: The result of the validation
        """
        ...

    async def validate_async(self, value: Any, **kwargs: Any) -> ValidationResult:
        """Asynchronously validate a value.

        This method is optional. Validators that require async operations
        should implement this method. Default implementation raises NotImplementedError.

        Args:
            value: The value to validate
            **kwargs: Additional validation parameters

        Returns:
            ValidationResult: The result of the validation

        Raises:
            NotImplementedError: If the validator doesn't support async validation
        """
        raise NotImplementedError("This validator does not support async validation")


@runtime_checkable
class ValidatorFactory(Protocol):
    """Protocol defining the interface for validator factories.

    Validator factories must implement the create_validator method, which
    creates and returns validator instances based on a validator type.
    """

    def create_validator(self, validator_type: str, **options: Any) -> Validator:
        """Create a validator instance.

        Args:
            validator_type: The type of validator to create
            **options: Additional options for the validator

        Returns:
            Validator: An instance of the requested validator
        """
        ...
