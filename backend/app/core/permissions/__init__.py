from __future__ import annotations

"""Permissions package for application-wide authorization.

This package provides a comprehensive permission system for controlling access
to resources and actions throughout the application. It includes role-based and
permission-based authorization mechanisms, object-level permission checking,
and integration with the application's core systems.
"""

from app.core.permissions.models import Permission, UserRole, ROLE_PERMISSIONS
from app.core.permissions.checker import PermissionChecker
from app.core.permissions.decorators import (
    require_permission,
    require_permissions,
    require_admin,
)
from app.core.permissions.service import PermissionService, get_permission_service
from app.core.permissions.utils import (
    get_user_by_id,
    check_owner_permission,
    has_any_permission,
    has_all_permissions,
)

__all__ = [
    # Models and constants
    "Permission",
    "UserRole",
    "ROLE_PERMISSIONS",
    # Service
    "PermissionService",
    "get_permission_service",
    # Core functionality
    "PermissionChecker",
    # Decorators
    "require_permission",
    "require_permissions",
    "require_admin",
    # Utility functions
    "get_user_by_id",
    "check_owner_permission",
    "has_any_permission",
    "has_all_permissions",
]
