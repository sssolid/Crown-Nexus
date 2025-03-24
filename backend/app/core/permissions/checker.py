# /app/core/permissions/checker.py
from __future__ import annotations

"""Permission checker for authorization control.

This module provides the core permission checking functionality to determine
if users have the required permissions for various actions.
"""

from typing import Any, List, TYPE_CHECKING

from app.core.exceptions import PermissionDeniedException
from app.core.logging import get_logger
from app.core.permissions.models import Permission, ROLE_PERMISSIONS

if TYPE_CHECKING:
    from app.domains.users.models import User

logger = get_logger(__name__)


class PermissionChecker:
    """Permission checker for authorization control.

    This class provides methods to check if a user has the required permissions
    for a given action.
    """

    @staticmethod
    def has_permission(user: "User", permission: Permission) -> bool:
        """Check if a user has a specific permission.

        Args:
            user: User to check
            permission: Required permission

        Returns:
            bool: True if user has the permission
        """
        if not user or not user.is_active:
            return False

        # Get permissions for the user's role
        role_permissions = ROLE_PERMISSIONS.get(user.role, set())

        # Check direct permissions (if the model supports it)
        user_permissions = getattr(user, "permissions", [])
        if permission in user_permissions:
            return True

        # Check role-based permissions
        user_roles = getattr(user, "roles", [])
        for role in user_roles:
            role_permissions = getattr(role, "permissions", [])
            if permission in role_permissions:
                return True

        # Check if user has the required permission from role mapping
        return permission in role_permissions

    @staticmethod
    def has_permissions(
        user: "User", permissions: List[Permission], require_all: bool = True
    ) -> bool:
        """Check if a user has multiple permissions.

        Args:
            user: User to check
            permissions: Required permissions
            require_all: Whether all permissions are required (AND) or any (OR)

        Returns:
            bool: True if user has the required permissions
        """
        if not permissions:
            return True

        if require_all:
            # All permissions are required
            return all(PermissionChecker.has_permission(user, p) for p in permissions)
        else:
            # Any permission is sufficient
            return any(PermissionChecker.has_permission(user, p) for p in permissions)

    @staticmethod
    def check_object_permission(
        user: "User",
        obj: Any,
        permission: Permission,
        owner_field: str = "created_by_id",
    ) -> bool:
        """Check if a user has permission for a specific object.

        This allows for object-level permissions where users can perform actions
        on objects they own, even if they don't have the global permission.

        Args:
            user: User to check
            obj: Object to check permissions for
            permission: Required permission
            owner_field: Field name that contains the owner ID

        Returns:
            bool: True if user has permission
        """
        # Always check if user has the specific permission
        if PermissionChecker.has_permission(user, permission):
            return True

        # Check if user is the owner of the object
        if hasattr(obj, owner_field):
            entity_user_id = getattr(obj, owner_field)

            # Convert to string if it's a UUID
            if hasattr(entity_user_id, "hex"):
                entity_user_id = str(entity_user_id)

            # Check if user is the owner
            if entity_user_id == str(user.id):
                # Object ownership trumps permission check for non-admin operations
                if not permission.endswith("admin"):
                    return True

        return False

    @staticmethod
    def ensure_object_permission(
        user: "User",
        obj: Any,
        permission: Permission,
        owner_field: str = "created_by_id",
    ) -> None:
        """Ensure a user has permission for a specific object.

        Args:
            user: User to check
            obj: Object to check permissions for
            permission: Required permission
            owner_field: Field name that contains the owner ID

        Raises:
            PermissionDeniedException: If user doesn't have permission
        """
        if not PermissionChecker.check_object_permission(
            user, obj, permission, owner_field
        ):
            action = permission.split(":")[-1]
            resource = permission.split(":")[0]

            logger.warning(
                f"Object permission denied: {user.email} tried to {action} {resource}",
                extra={
                    "user_id": str(user.id),
                    "user_role": user.role,
                    "permission": permission,
                    "object_id": getattr(obj, "id", None),
                    "object_type": obj.__class__.__name__,
                },
            )

            raise PermissionDeniedException(
                message=f"You don't have permission to {action} this {resource}",
                action=action,
                resource_type=resource,
                permission=permission,
            )


# Create a singleton instance
permissions = PermissionChecker()
