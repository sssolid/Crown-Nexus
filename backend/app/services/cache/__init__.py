# backend/app/services/cache/__init__.py
"""Cache service package for application-wide caching.

This package provides services for caching data across different backends,
with support for key management, decorators for function results caching,
and consistent interfaces across backends.
"""
from __future__ import annotations

from app.services.cache.service import CacheService

# Factory function for dependency injection
def get_cache_service():
    """Factory function to get CacheService"""
    return CacheService()

__all__ = ["get_cache_service", "CacheService"]
