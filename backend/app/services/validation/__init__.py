# /app/services/validation/__init__.py
from __future__ import annotations

"""Validation service package for application-wide data validation.

This package provides services for validating different types of data,
ensuring data integrity and consistency throughout the application.
"""

from app.services.validation.service import ValidationService

# Factory function for dependency injection
def get_validation_service():
    """Factory function to get ValidationService"""
    return ValidationService()

__all__ = ["get_validation_service", "ValidationService"]
