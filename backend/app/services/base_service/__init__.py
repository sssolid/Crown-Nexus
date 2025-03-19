# /app/services/base_service/__init__.py
from __future__ import annotations

"""Base service package for standardized CRUD operations.

This package provides a base service implementation that can be extended
by domain-specific services to provide standardized CRUD operations,
permission checking, and lifecycle hooks.
"""

from app.services.base_service.contracts import BaseServiceProtocol
from app.services.base_service.permissions import PermissionHelper
from app.services.base_service.service import BaseService

__all__ = ["BaseService", "BaseServiceProtocol", "PermissionHelper"]
