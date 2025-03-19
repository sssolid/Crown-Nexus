# backend/app/services/cache/__init__.py
"""Cache service package for application-wide caching.

This package provides services for caching data across different backends,
with support for key management, decorators for function results caching,
and consistent interfaces across backends.
"""
from __future__ import annotations

from app.core.dependency_manager import dependency_manager
from app.services.cache.service import CacheService

# Create a singleton instance
cache_service = CacheService()

# Register with dependency manager
dependency_manager.register_dependency("cache_service", cache_service)

__all__ = ["cache_service", "CacheService"]
