# backend/app/services/security/__init__.py
"""Security service package for application-wide security features.

This package provides services for authentication, authorization, password management,
API key handling, CSRF protection, rate limiting, and other security features.
"""
from __future__ import annotations

from app.services.security.service import SecurityService


# Factory function for dependency injection
def get_security_service():
    """Factory function to get SecurityService"""
    return SecurityService()


__all__ = ["get_security_service", "SecurityService"]
