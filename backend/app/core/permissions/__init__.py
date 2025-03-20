# /app/core/permissions/__init__.py
from __future__ import annotations

"""Permissions package for application-wide authorization.

This package provides a comprehensive permission system for controlling access
to resources and actions throughout the application.
"""

from app.core.permissions.models import Permission, UserRole, ROLE_PERMISSIONS
from app.core.permissions.checker import PermissionChecker, permissions
from app.core.permissions.decorators import (
    require_permission,
    require_permissions,
    require_admin,
)
from app.core.permissions.utils import (
    get_user_by_id,
    check_owner_permission,
    has_any_permission,
    has_all_permissions,
)

__all__ = [
    # Models
    "Permission",
    "UserRole",
    "ROLE_PERMISSIONS",
    # Checker
    "PermissionChecker",
    "permissions",
    # Decorators
    "require_permission",
    "require_permissions",
    "require_admin",
    # Utilities
    "get_user_by_id",
    "check_owner_permission",
    "has_any_permission",
    "has_all_permissions",
]
