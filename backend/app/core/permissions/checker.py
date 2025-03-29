from __future__ import annotations

"""Permission checker for authorization control.

This module provides the core permission checking functionality to determine
if users have the required permissions for various actions.
"""

from typing import Any, List, TYPE_CHECKING

from app.core.exceptions import PermissionDeniedException
from app.logging import get_logger
from app.core.permissions.models import Permission, ROLE_PERMISSIONS

if TYPE_CHECKING:
    from app.domains.users.models import User

logger = get_logger("app.core.permissions.checker")


class PermissionChecker:
    """Permission checking functionality for the application.

    This class provides methods to check if users have specific permissions
    based on their roles and explicit permissions.
    """

    @staticmethod
    def has_permission(user: "User", permission: Permission) -> bool:
        """Check if a user has a specific permission.

        Args:
            user: The user to check permissions for
            permission: The permission to check

        Returns:
            bool: True if the user has the permission
        """
        if not user or not user.is_active:
            return False

        # Get permissions from the user's role
        role_permissions = ROLE_PERMISSIONS.get(user.role, set())

        # Check if permission is in role permissions
        if permission in role_permissions:
            return True

        # Check explicit user permissions
        user_permissions = getattr(user, "permissions", [])
        if permission in user_permissions:
            return True

        # Check permissions from any additional roles
        user_roles = getattr(user, "roles", [])
        for role in user_roles:
            role_permissions = getattr(role, "permissions", [])
            if permission in role_permissions:
                return True

        return False

    @staticmethod
    def has_permissions(
        user: "User", permissions: List[Permission], require_all: bool = True
    ) -> bool:
        """Check if a user has multiple permissions.

        Args:
            user: The user to check permissions for
            permissions: List of permissions to check
            require_all: Whether all permissions are required (True) or any (False)

        Returns:
            bool: True if the user has the required permissions
        """
        if not permissions:
            return True

        if require_all:
            return all(PermissionChecker.has_permission(user, p) for p in permissions)
        else:
            return any(PermissionChecker.has_permission(user, p) for p in permissions)

    @staticmethod
    def check_object_permission(
        user: "User",
        obj: Any,
        permission: Permission,
        owner_field: str = "created_by_id",
    ) -> bool:
        """Check if a user has permission for a specific object.

        This checks both the permission itself and if the user is the object owner.

        Args:
            user: The user to check
            obj: The object to check permissions for
            permission: The permission to check
            owner_field: The field name containing the owner's ID

        Returns:
            bool: True if the user has permission for this object
        """
        # If user has the general permission, allow access
        if PermissionChecker.has_permission(user, permission):
            return True

        # Check ownership if it's not an admin-level permission
        if not str(permission).endswith("admin"):
            if hasattr(obj, owner_field):
                entity_user_id = getattr(obj, owner_field)

                # Handle UUID conversion if needed
                if hasattr(entity_user_id, "hex"):
                    entity_user_id = str(entity_user_id)

                # If user is the owner, allow access
                if entity_user_id == str(user.id):
                    return True

        return False

    @staticmethod
    def ensure_object_permission(
        user: "User",
        obj: Any,
        permission: Permission,
        owner_field: str = "created_by_id",
    ) -> None:
        """Ensure a user has permission for an object, raising an exception if not.

        Args:
            user: The user to check
            obj: The object to check permissions for
            permission: The permission to check
            owner_field: The field indicating object ownership

        Raises:
            PermissionDeniedException: If the user doesn't have the permission
        """
        if not PermissionChecker.check_object_permission(
            user, obj, permission, owner_field
        ):
            action = str(permission).split(":")[-1]
            resource = str(permission).split(":")[0]

            logger.warning(
                f"Object permission denied: {getattr(user, 'email', 'Unknown')} tried to {action} {resource}",
                user_id=str(getattr(user, "id", "Unknown")),
                user_role=getattr(user, "role", "Unknown"),
                permission=str(permission),
                object_id=getattr(obj, "id", None),
                object_type=obj.__class__.__name__,
            )

            raise PermissionDeniedException(
                message=f"You don't have permission to {action} this {resource}",
                action=action,
                resource_type=resource,
                permission=str(permission),
            )


# Create a singleton instance for backward compatibility
permissions = PermissionChecker()
