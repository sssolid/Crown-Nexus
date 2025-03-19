# backend/app/services/security/__init__.py
"""Security service package for application-wide security features.

This package provides services for authentication, authorization, password management,
API key handling, CSRF protection, rate limiting, and other security features.
"""
from __future__ import annotations

from app.core.dependency_manager import dependency_manager
from app.services.security.service import SecurityService

# Create a singleton instance
security_service = SecurityService()

# Register with dependency manager
dependency_manager.register_dependency("security_service", security_service)

__all__ = ["security_service", "SecurityService"]
