# /app/core/validation/validators.py
from __future__ import annotations

"""Validator implementations for various data types.

This module provides different implementations of the Validator protocol
for validating different types of data.
"""

import ipaddress
import re
import uuid
from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Type, Union

from app.core.logging import get_logger
from app.core.validation.base import ValidationResult, Validator

logger = get_logger("app.core.validation.validators")


class EmailValidator(Validator):
    """Validator for email addresses."""

    def __init__(self) -> None:
        """Initialize the email validator."""
        self.pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    def validate(self, value: Any, **kwargs: Any) -> ValidationResult:
        """Validate an email address.

        Args:
            value: The email address to validate
            **kwargs: Additional validation parameters

        Returns:
            ValidationResult: The result of the validation
        """
        if not isinstance(value, str):
            return ValidationResult(
                is_valid=False,
                errors=[{"msg": "Email must be a string", "type": "type_error"}],
            )

        if not value or len(value) > 255:
            return ValidationResult(
                is_valid=False,
                errors=[
                    {
                        "msg": "Email must be between 1 and 255 characters",
                        "type": "length_error",
                    }
                ],
            )

        if not self.pattern.match(value):
            return ValidationResult(
                is_valid=False,
                errors=[{"msg": "Invalid email format", "type": "format_error"}],
            )

        return ValidationResult(is_valid=True)


class PhoneValidator(Validator):
    """Validator for phone numbers."""

    def __init__(self) -> None:
        """Initialize the phone validator."""
        self.pattern = re.compile(r"^\+?[0-9]{10,15}$")

    def validate(self, value: Any, **kwargs: Any) -> ValidationResult:
        """Validate a phone number.

        Args:
            value: The phone number to validate
            **kwargs: Additional validation parameters

        Returns:
            ValidationResult: The result of the validation
        """
        if not isinstance(value, str):
            return ValidationResult(
                is_valid=False,
                errors=[{"msg": "Phone number must be a string", "type": "type_error"}],
            )

        # Clean the phone number
        cleaned = re.sub(r"[\s\-\(\).]", "", value)

        if not self.pattern.match(cleaned):
            return ValidationResult(
                is_valid=False,
                errors=[{"msg": "Invalid phone number format", "type": "format_error"}],
            )

        return ValidationResult(is_valid=True)


class DateValidator(Validator):
    """Validator for dates."""

    def validate(
        self,
        value: Union[str, date, datetime],
        min_date: Optional[Union[str, date, datetime]] = None,
        max_date: Optional[Union[str, date, datetime]] = None,
        format_str: Optional[str] = None,
        **kwargs: Any,
    ) -> ValidationResult:
        """Validate a date.

        Args:
            value: The date to validate
            min_date: Optional minimum date
            max_date: Optional maximum date
            format_str: Optional date format string for parsing string dates
            **kwargs: Additional validation parameters

        Returns:
            ValidationResult: The result of the validation
        """
        errors: List[Dict[str, Any]] = []
        date_value: Optional[date] = None

        # Convert string to date if needed
        if isinstance(value, str):
            if not format_str:
                format_str = "%Y-%m-%d"
            try:
                date_value = datetime.strptime(value, format_str).date()
            except ValueError:
                errors.append(
                    {
                        "msg": f"Invalid date format, expected format: {format_str}",
                        "type": "format_error",
                    }
                )
                return ValidationResult(is_valid=False, errors=errors)
        elif isinstance(value, datetime):
            date_value = value.date()
        elif isinstance(value, date):
            date_value = value
        else:
            errors.append(
                {
                    "msg": "Value must be a string, date, or datetime",
                    "type": "type_error",
                }
            )
            return ValidationResult(is_valid=False, errors=errors)

        # Process min_date if provided
        min_date_value: Optional[date] = None
        if min_date:
            if isinstance(min_date, str):
                if not format_str:
                    format_str = "%Y-%m-%d"
                try:
                    min_date_value = datetime.strptime(min_date, format_str).date()
                except ValueError:
                    errors.append(
                        {
                            "msg": f"Invalid min_date format, expected format: {format_str}",
                            "type": "format_error",
                        }
                    )
            elif isinstance(min_date, datetime):
                min_date_value = min_date.date()
            elif isinstance(min_date, date):
                min_date_value = min_date

        # Process max_date if provided
        max_date_value: Optional[date] = None
        if max_date:
            if isinstance(max_date, str):
                if not format_str:
                    format_str = "%Y-%m-%d"
                try:
                    max_date_value = datetime.strptime(max_date, format_str).date()
                except ValueError:
                    errors.append(
                        {
                            "msg": f"Invalid max_date format, expected format: {format_str}",
                            "type": "format_error",
                        }
                    )
            elif isinstance(max_date, datetime):
                max_date_value = max_date.date()
            elif isinstance(max_date, date):
                max_date_value = max_date

        # Check constraints
        if min_date_value and date_value < min_date_value:
            errors.append(
                {
                    "msg": f"Date must be on or after {min_date_value.isoformat()}",
                    "type": "range_error",
                }
            )

        if max_date_value and date_value > max_date_value:
            errors.append(
                {
                    "msg": f"Date must be on or before {max_date_value.isoformat()}",
                    "type": "range_error",
                }
            )

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)


class LengthValidator(Validator):
    """Validator for string length."""

    def validate(
        self,
        value: Any,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        **kwargs: Any,
    ) -> ValidationResult:
        """Validate the length of a string.

        Args:
            value: The string to validate
            min_length: Optional minimum length
            max_length: Optional maximum length
            **kwargs: Additional validation parameters

        Returns:
            ValidationResult: The result of the validation
        """
        errors: List[Dict[str, Any]] = []

        if not isinstance(value, str):
            errors.append({"msg": "Value must be a string", "type": "type_error"})
            return ValidationResult(is_valid=False, errors=errors)

        if min_length is not None and len(value) < min_length:
            errors.append(
                {
                    "msg": f"String length must be at least {min_length} characters",
                    "type": "min_length_error",
                }
            )

        if max_length is not None and len(value) > max_length:
            errors.append(
                {
                    "msg": f"String length must be at most {max_length} characters",
                    "type": "max_length_error",
                }
            )

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)


class RangeValidator(Validator):
    """Validator for numeric ranges."""

    def validate(
        self,
        value: Union[int, float],
        min_value: Optional[Union[int, float]] = None,
        max_value: Optional[Union[int, float]] = None,
        **kwargs: Any,
    ) -> ValidationResult:
        """Validate a numeric value against a range.

        Args:
            value: The number to validate
            min_value: Optional minimum value
            max_value: Optional maximum value
            **kwargs: Additional validation parameters

        Returns:
            ValidationResult: The result of the validation
        """
        errors: List[Dict[str, Any]] = []

        if not isinstance(value, (int, float)):
            errors.append({"msg": "Value must be a number", "type": "type_error"})
            return ValidationResult(is_valid=False, errors=errors)

        if min_value is not None and value < min_value:
            errors.append(
                {
                    "msg": f"Value must be greater than or equal to {min_value}",
                    "type": "min_value_error",
                }
            )

        if max_value is not None and value > max_value:
            errors.append(
                {
                    "msg": f"Value must be less than or equal to {max_value}",
                    "type": "max_value_error",
                }
            )

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)


class RegexValidator(Validator):
    """Validator for regex patterns."""

    def validate(self, value: Any, pattern: str, **kwargs: Any) -> ValidationResult:
        """Validate a string against a regex pattern.

        Args:
            value: The string to validate
            pattern: The regex pattern to validate against
            **kwargs: Additional validation parameters

        Returns:
            ValidationResult: The result of the validation
        """
        errors: List[Dict[str, Any]] = []

        if not isinstance(value, str):
            errors.append({"msg": "Value must be a string", "type": "type_error"})
            return ValidationResult(is_valid=False, errors=errors)

        try:
            compiled_pattern = re.compile(pattern)
            if not compiled_pattern.match(value):
                errors.append(
                    {
                        "msg": f"Value does not match pattern: {pattern}",
                        "type": "pattern_mismatch",
                    }
                )
        except re.error:
            errors.append(
                {"msg": f"Invalid regex pattern: {pattern}", "type": "invalid_pattern"}
            )

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)


class RequiredValidator(Validator):
    """Validator for required values."""

    def validate(self, value: Any, **kwargs: Any) -> ValidationResult:
        """Validate that a value is not empty.

        Args:
            value: The value to validate
            **kwargs: Additional validation parameters

        Returns:
            ValidationResult: The result of the validation
        """
        if value is None:
            return ValidationResult(
                is_valid=False,
                errors=[{"msg": "Value is required", "type": "required_error"}],
            )

        if isinstance(value, str) and not value.strip():
            return ValidationResult(
                is_valid=False,
                errors=[{"msg": "Value cannot be empty", "type": "required_error"}],
            )

        if isinstance(value, (list, dict, set)) and not value:
            return ValidationResult(
                is_valid=False,
                errors=[{"msg": "Value cannot be empty", "type": "required_error"}],
            )

        return ValidationResult(is_valid=True)


class URLValidator(Validator):
    """Validator for URLs."""

    def __init__(self) -> None:
        """Initialize the URL validator."""
        self.pattern = re.compile(
            r"^(https?:\/\/)?"  # protocol
            r"(([a-z\d]([a-z\d-]*[a-z\d])*)\.)+[a-z]{2,}|"  # domain name
            r"((\d{1,3}\.){3}\d{1,3})"  # OR ip (v4) address
            r"(\:\d+)?(\/[-a-z\d%_.~+]*)*"  # port and path
            r"(\?[;&a-z\d%_.~+=-]*)?"  # query string
            r"(\#[-a-z\d_]*)?$",  # fragment locator
            re.IGNORECASE,
        )

    def validate(self, value: Any, **kwargs: Any) -> ValidationResult:
        """Validate a URL.

        Args:
            value: The URL to validate
            **kwargs: Additional validation parameters

        Returns:
            ValidationResult: The result of the validation
        """
        if not isinstance(value, str):
            return ValidationResult(
                is_valid=False,
                errors=[{"msg": "URL must be a string", "type": "type_error"}],
            )

        if not value:
            return ValidationResult(
                is_valid=False,
                errors=[{"msg": "URL cannot be empty", "type": "empty_error"}],
            )

        if not self.pattern.match(value):
            return ValidationResult(
                is_valid=False,
                errors=[{"msg": "Invalid URL format", "type": "format_error"}],
            )

        return ValidationResult(is_valid=True)


class UUIDValidator(Validator):
    """Validator for UUIDs."""

    def validate(self, value: Any, **kwargs: Any) -> ValidationResult:
        """Validate a UUID.

        Args:
            value: The UUID string to validate
            **kwargs: Additional validation parameters

        Returns:
            ValidationResult: The result of the validation
        """
        if not isinstance(value, str):
            return ValidationResult(
                is_valid=False,
                errors=[{"msg": "UUID must be a string", "type": "type_error"}],
            )

        try:
            uuid_obj = uuid.UUID(value)
            if str(uuid_obj) == value:
                return ValidationResult(is_valid=True)
            else:
                return ValidationResult(
                    is_valid=False,
                    errors=[{"msg": "UUID format is invalid", "type": "format_error"}],
                )
        except (ValueError, AttributeError, TypeError):
            return ValidationResult(
                is_valid=False,
                errors=[{"msg": "Invalid UUID format", "type": "format_error"}],
            )


class CreditCardValidator(Validator):
    """Validator for credit card numbers."""

    def __init__(self) -> None:
        """Initialize the credit card validator."""
        self.pattern = re.compile(r"^[0-9]{13,19}$")

    def validate(self, value: Any, **kwargs: Any) -> ValidationResult:
        """Validate a credit card number using the Luhn algorithm.

        Args:
            value: The credit card number to validate
            **kwargs: Additional validation parameters

        Returns:
            ValidationResult: The result of the validation
        """
        if not isinstance(value, str):
            return ValidationResult(
                is_valid=False,
                errors=[
                    {"msg": "Credit card number must be a string", "type": "type_error"}
                ],
            )

        # Remove spaces and hyphens
        card_number = value.replace(" ", "").replace("-", "")

        # Check if it only contains digits and has appropriate length
        if not self.pattern.match(card_number):
            return ValidationResult(
                is_valid=False,
                errors=[{"msg": "Invalid credit card format", "type": "format_error"}],
            )

        # Luhn algorithm
        digits = [int(d) for d in card_number]
        checksum = 0
        for i, digit in enumerate(reversed(digits)):
            if i % 2 == 1:
                digit *= 2
                if digit > 9:
                    digit -= 9
            checksum += digit

        if checksum % 10 != 0:
            return ValidationResult(
                is_valid=False,
                errors=[
                    {
                        "msg": "Invalid credit card number (failed Luhn check)",
                        "type": "checksum_error",
                    }
                ],
            )

        return ValidationResult(is_valid=True)


class IPAddressValidator(Validator):
    """Validator for IP addresses."""

    def validate(
        self, value: Any, version: Optional[int] = None, **kwargs: Any
    ) -> ValidationResult:
        """Validate an IP address.

        Args:
            value: The IP address to validate
            version: Optional IP version (4 or 6)
            **kwargs: Additional validation parameters

        Returns:
            ValidationResult: The result of the validation
        """
        if not isinstance(value, str):
            return ValidationResult(
                is_valid=False,
                errors=[{"msg": "IP address must be a string", "type": "type_error"}],
            )

        try:
            ip_obj = ipaddress.ip_address(value)

            if version == 4 and not isinstance(ip_obj, ipaddress.IPv4Address):
                return ValidationResult(
                    is_valid=False,
                    errors=[
                        {"msg": "IP address must be IPv4", "type": "version_error"}
                    ],
                )

            if version == 6 and not isinstance(ip_obj, ipaddress.IPv6Address):
                return ValidationResult(
                    is_valid=False,
                    errors=[
                        {"msg": "IP address must be IPv6", "type": "version_error"}
                    ],
                )

            return ValidationResult(is_valid=True)
        except ValueError:
            return ValidationResult(
                is_valid=False,
                errors=[{"msg": "Invalid IP address format", "type": "format_error"}],
            )


class PasswordValidator(Validator):
    """Validator for password strength."""

    def validate(
        self,
        value: Any,
        min_length: int = 8,
        require_lowercase: bool = True,
        require_uppercase: bool = True,
        require_digit: bool = True,
        require_special: bool = True,
        **kwargs: Any,
    ) -> ValidationResult:
        """Validate password strength.

        Args:
            value: The password to validate
            min_length: Minimum password length
            require_lowercase: Whether to require at least one lowercase letter
            require_uppercase: Whether to require at least one uppercase letter
            require_digit: Whether to require at least one digit
            require_special: Whether to require at least one special character
            **kwargs: Additional validation parameters

        Returns:
            ValidationResult: The result of the validation
        """
        errors: List[Dict[str, Any]] = []

        if not isinstance(value, str):
            errors.append({"msg": "Password must be a string", "type": "type_error"})
            return ValidationResult(is_valid=False, errors=errors)

        if len(value) < min_length:
            errors.append(
                {
                    "msg": f"Password must be at least {min_length} characters long",
                    "type": "length_error",
                }
            )

        if require_lowercase and not any(c.islower() for c in value):
            errors.append(
                {
                    "msg": "Password must contain at least one lowercase letter",
                    "type": "complexity_error",
                }
            )

        if require_uppercase and not any(c.isupper() for c in value):
            errors.append(
                {
                    "msg": "Password must contain at least one uppercase letter",
                    "type": "complexity_error",
                }
            )

        if require_digit and not any(c.isdigit() for c in value):
            errors.append(
                {
                    "msg": "Password must contain at least one digit",
                    "type": "complexity_error",
                }
            )

        if require_special and not any(not c.isalnum() for c in value):
            errors.append(
                {
                    "msg": "Password must contain at least one special character",
                    "type": "complexity_error",
                }
            )

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)


class EnumValidator(Validator):
    """Validator for enum values."""

    def validate(
        self, value: Any, enum_class: Type[Enum], **kwargs: Any
    ) -> ValidationResult:
        """Validate that a value is a valid enum member.

        Args:
            value: The value to validate
            enum_class: The Enum class to validate against
            **kwargs: Additional validation parameters

        Returns:
            ValidationResult: The result of the validation
        """
        try:
            enum_class(value)
            return ValidationResult(is_valid=True)
        except (ValueError, TypeError):
            valid_values = ", ".join([f"{e.name} ({e.value})" for e in enum_class])
            return ValidationResult(
                is_valid=False,
                errors=[
                    {
                        "msg": f"Invalid enum value, must be one of: {valid_values}",
                        "type": "enum_error",
                    }
                ],
            )
