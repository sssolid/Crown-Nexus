"""
Custom exceptions for the fitment module.

This module defines custom exceptions for handling
application-specific errors in the fitment module.
"""

from __future__ import annotations

from typing import Any, Dict, Optional


class FitmentError(Exception):
    """Base class for all fitment module exceptions."""

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Initialize a fitment error.

        Args:
            message: Error message
            details: Optional dictionary with additional error details
        """
        self.message = message
        self.details = details or {}
        super().__init__(message)


class ParsingError(FitmentError):
    """Exception raised when parsing a fitment string fails."""

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Initialize a parsing error.

        Args:
            message: Error message
            details: Optional dictionary with additional error details
        """
        super().__init__(message, details)


class ValidationError(FitmentError):
    """Exception raised when validating a fitment fails."""

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Initialize a validation error.

        Args:
            message: Error message
            details: Optional dictionary with additional error details
        """
        super().__init__(message, details)


class MappingError(FitmentError):
    """Exception raised when mapping a fitment fails."""

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Initialize a mapping error.

        Args:
            message: Error message
            details: Optional dictionary with additional error details
        """
        super().__init__(message, details)


class DatabaseError(FitmentError):
    """Exception raised when a database operation fails."""

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Initialize a database error.

        Args:
            message: Error message
            details: Optional dictionary with additional error details
        """
        super().__init__(message, details)


class ConfigurationError(FitmentError):
    """Exception raised when configuration is invalid or missing."""

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Initialize a configuration error.

        Args:
            message: Error message
            details: Optional dictionary with additional error details
        """
        super().__init__(message, details)
