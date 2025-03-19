# /app/services/error/__init__.py
from __future__ import annotations

"""Error service package for application-wide error handling.

This package provides services for handling errors, reporting them to
various destinations, and creating standardized error responses.
"""

from app.services.error.service import ErrorService


# Factory function for dependency injection
def get_error_service():
    """Factory function to get ErrorService"""
    return ErrorService()


__all__ = ["get_error_service", "ErrorService"]
