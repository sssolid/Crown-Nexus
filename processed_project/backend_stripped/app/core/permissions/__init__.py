from __future__ import annotations
'Permissions package for application-wide authorization.\n\nThis package provides a comprehensive permission system for controlling access\nto resources and actions throughout the application.\n'
from app.core.permissions.models import Permission, UserRole, ROLE_PERMISSIONS
from app.core.permissions.checker import PermissionChecker, permissions
from app.core.permissions.decorators import require_permission, require_permissions, require_admin
from app.core.permissions.utils import get_user_by_id, check_owner_permission, has_any_permission, has_all_permissions
__all__ = ['Permission', 'UserRole', 'ROLE_PERMISSIONS', 'PermissionChecker', 'permissions', 'require_permission', 'require_permissions', 'require_admin', 'get_user_by_id', 'check_owner_permission', 'has_any_permission', 'has_all_permissions']