from __future__ import annotations

"""Autocare domain exceptions.

This module defines exceptions specific to the autocare domain and its subdomains.
These exceptions handle various error cases when working with VCdb, PCdb, PAdb, Qdb,
ACES, and PIES data.
"""

from app.core.exceptions import BusinessException, ResourceNotFoundException


class AutocareException(BusinessException):
    """Base exception for all autocare domain exceptions."""

    def __init__(self, message: str, details: dict = None) -> None:
        """Initialize the exception.

        Args:
            message: The error message
            details: Optional dictionary with additional error details
        """
        super().__init__(message=message, details=details)


class InvalidVehicleDataException(AutocareException):
    """Raised when vehicle data is invalid or incomplete."""

    def __init__(self, message: str = "Invalid vehicle data", details: dict = None) -> None:
        """Initialize the exception.

        Args:
            message: The error message
            details: Optional dictionary with additional error details
        """
        super().__init__(message=message, details=details)


class InvalidPartDataException(AutocareException):
    """Raised when part data is invalid or incomplete."""

    def __init__(self, message: str = "Invalid part data", details: dict = None) -> None:
        """Initialize the exception.

        Args:
            message: The error message
            details: Optional dictionary with additional error details
        """
        super().__init__(message=message, details=details)


class MappingNotFoundException(ResourceNotFoundException):
    """Raised when a requested fitment mapping cannot be found."""

    def __init__(self, resource_id: str, details: dict = None) -> None:
        """Initialize the exception.

        Args:
            resource_id: The ID of the mapping that wasn't found
            details: Optional dictionary with additional error details
        """
        super().__init__(
            resource_type="FitmentMapping",
            resource_id=resource_id,
            message=f"Fitment mapping with ID {resource_id} not found",
            details=details,
        )


class ImportException(AutocareException):
    """Raised when importing data from ACES or PIES files fails."""

    def __init__(self, message: str = "Failed to import data", details: dict = None) -> None:
        """Initialize the exception.

        Args:
            message: The error message
            details: Optional dictionary with additional error details
        """
        super().__init__(message=message, details=details)


class ExportException(AutocareException):
    """Raised when exporting data to ACES or PIES files fails."""

    def __init__(self, message: str = "Failed to export data", details: dict = None) -> None:
        """Initialize the exception.

        Args:
            message: The error message
            details: Optional dictionary with additional error details
        """
        super().__init__(message=message, details=details)


class VCdbException(AutocareException):
    """Raised when there's an issue with VCdb data."""
    
    def __init__(self, message: str = "VCdb operation failed", details: dict = None) -> None:
        """Initialize the exception.

        Args:
            message: The error message
            details: Optional dictionary with additional error details
        """
        super().__init__(message=message, details=details)


class PCdbException(AutocareException):
    """Raised when there's an issue with PCdb data."""
    
    def __init__(self, message: str = "PCdb operation failed", details: dict = None) -> None:
        """Initialize the exception.

        Args:
            message: The error message
            details: Optional dictionary with additional error details
        """
        super().__init__(message=message, details=details)


class PAdbException(AutocareException):
    """Raised when there's an issue with PAdb data."""
    
    def __init__(self, message: str = "PAdb operation failed", details: dict = None) -> None:
        """Initialize the exception.

        Args:
            message: The error message
            details: Optional dictionary with additional error details
        """
        super().__init__(message=message, details=details)


class QdbException(AutocareException):
    """Raised when there's an issue with Qdb data."""
    
    def __init__(self, message: str = "Qdb operation failed", details: dict = None) -> None:
        """Initialize the exception.

        Args:
            message: The error message
            details: Optional dictionary with additional error details
        """
        super().__init__(message=message, details=details)
