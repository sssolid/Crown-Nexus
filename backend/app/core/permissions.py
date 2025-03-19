# app/core/permissions.py
from __future__ import annotations

import enum
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Type,
    TypeVar,
    Union,
    cast,
    TYPE_CHECKING,
)

from fastapi import Depends, HTTPException, Request, status
from pydantic import BaseModel

from app.core.exceptions import PermissionDeniedException
from app.core.logging import get_logger

# Use TYPE_CHECKING to avoid runtime circular imports
if TYPE_CHECKING:
    from app.models.user import User, UserRole
else:
    # Define an enum for UserRole to avoid importing the actual model
    class UserRole(str, enum.Enum):
        ADMIN = "admin"
        MANAGER = "manager"
        CLIENT = "client"
        DISTRIBUTOR = "distributor"
        READ_ONLY = "read_only"


logger = get_logger("app.core.permissions")

T = TypeVar("T", bound=Callable[..., Any])


class Permission(str, enum.Enum):
    """Permission types for the application.

    This enum defines all available permissions in the system.
    Permissions follow a resource:action format.
    """

    # User permissions
    USER_CREATE = "user:create"
    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"
    USER_ADMIN = "user:admin"

    # Product permissions
    PRODUCT_CREATE = "product:create"
    PRODUCT_READ = "product:read"
    PRODUCT_UPDATE = "product:update"
    PRODUCT_DELETE = "product:delete"
    PRODUCT_ADMIN = "product:admin"

    # Media permissions
    MEDIA_CREATE = "media:create"
    MEDIA_READ = "media:read"
    MEDIA_UPDATE = "media:update"
    MEDIA_DELETE = "media:delete"
    MEDIA_ADMIN = "media:admin"

    # Fitment permissions
    FITMENT_CREATE = "fitment:create"
    FITMENT_READ = "fitment:read"
    FITMENT_UPDATE = "fitment:update"
    FITMENT_DELETE = "fitment:delete"
    FITMENT_ADMIN = "fitment:admin"

    # Company permissions
    COMPANY_CREATE = "company:create"
    COMPANY_READ = "company:read"
    COMPANY_UPDATE = "company:update"
    COMPANY_DELETE = "company:delete"
    COMPANY_ADMIN = "company:admin"

    # System permissions
    SYSTEM_ADMIN = "system:admin"


# Role-to-permission mapping
ROLE_PERMISSIONS = {
    UserRole.ADMIN: {
        # Admin has all permissions
        p
        for p in Permission
    },
    UserRole.MANAGER: {
        # Managers have most permissions except for system administration
        Permission.USER_READ,
        Permission.USER_CREATE,
        Permission.USER_UPDATE,
        Permission.PRODUCT_READ,
        Permission.PRODUCT_CREATE,
        Permission.PRODUCT_UPDATE,
        Permission.PRODUCT_DELETE,
        Permission.PRODUCT_ADMIN,
        Permission.MEDIA_READ,
        Permission.MEDIA_CREATE,
        Permission.MEDIA_UPDATE,
        Permission.MEDIA_DELETE,
        Permission.MEDIA_ADMIN,
        Permission.FITMENT_READ,
        Permission.FITMENT_CREATE,
        Permission.FITMENT_UPDATE,
        Permission.FITMENT_DELETE,
        Permission.FITMENT_ADMIN,
        Permission.COMPANY_READ,
    },
    UserRole.CLIENT: {
        # Clients have basic read permissions and can manage their own data
        Permission.PRODUCT_READ,
        Permission.FITMENT_READ,
        Permission.MEDIA_READ,
        Permission.COMPANY_READ,
    },
    UserRole.DISTRIBUTOR: {
        # Distributors have slightly more permissions than regular clients
        Permission.PRODUCT_READ,
        Permission.FITMENT_READ,
        Permission.MEDIA_READ,
        Permission.MEDIA_CREATE,
        Permission.COMPANY_READ,
    },
    UserRole.READ_ONLY: {
        # Read-only users can only read data
        Permission.PRODUCT_READ,
        Permission.FITMENT_READ,
        Permission.MEDIA_READ,
        Permission.COMPANY_READ,
    },
}


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

        # Check if user has the required permission
        return permission in role_permissions

    @staticmethod
    def has_permissions(
        user: User, permissions: List[Permission], require_all: bool = True
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
    def require_permission(permission: Permission) -> Callable[[T], T]:
        """Decorator to require a specific permission.

        Args:
            permission: Required permission

        Returns:
            Callable: Decorator function
        """

        def decorator(func: T) -> T:
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                # Find current_user in kwargs
                current_user = kwargs.get("current_user")

                if not current_user:
                    # Try to find it in the arguments
                    for arg in args:
                        if isinstance(arg, User):
                            current_user = arg
                            break

                if not current_user:
                    raise PermissionDeniedException(
                        message="Authentication required",
                    )

                if not PermissionChecker.has_permission(current_user, permission):
                    action = permission.split(":")[-1]
                    resource = permission.split(":")[0]

                    logger.warning(
                        f"Permission denied: {current_user.email} tried to {action} {resource}",
                        extra={
                            "user_id": str(current_user.id),
                            "user_role": current_user.role,
                            "permission": permission,
                        },
                    )

                    raise PermissionDeniedException(
                        message=f"You don't have permission to {action} {resource}",
                    )

                return await func(*args, **kwargs)

            return cast(T, wrapper)

        return decorator

    @staticmethod
    def require_permissions(
        permissions: List[Permission],
        require_all: bool = True,
    ) -> Callable[[T], T]:
        """Decorator to require multiple permissions.

        Args:
            permissions: Required permissions
            require_all: Whether all permissions are required (AND) or any (OR)

        Returns:
            Callable: Decorator function
        """

        def decorator(func: T) -> T:
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                # Find current_user in kwargs
                current_user = kwargs.get("current_user")

                if not current_user:
                    # Try to find it in the arguments
                    for arg in args:
                        if isinstance(arg, User):
                            current_user = arg
                            break

                if not current_user:
                    raise PermissionDeniedException(
                        message="Authentication required",
                    )

                if not PermissionChecker.has_permissions(
                    current_user, permissions, require_all
                ):
                    permission_str = (
                        " and ".join(p for p in permissions)
                        if require_all
                        else " or ".join(p for p in permissions)
                    )

                    logger.warning(
                        f"Permission denied: {current_user.email} missing required permissions: {permission_str}",
                        extra={
                            "user_id": str(current_user.id),
                            "user_role": current_user.role,
                            "permissions": [p for p in permissions],
                        },
                    )

                    raise PermissionDeniedException(
                        message=f"You don't have the required permissions: {permission_str}",
                    )

                return await func(*args, **kwargs)

            return cast(T, wrapper)

        return decorator

    @staticmethod
    def require_admin() -> Callable[[T], T]:
        """Decorator to require admin role.

        Returns:
            Callable: Decorator function
        """
        return PermissionChecker.require_permission(Permission.SYSTEM_ADMIN)

    @staticmethod
    def check_object_permission(
        user: User,
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
        if hasattr(obj, owner_field) and getattr(obj, owner_field) == user.id:
            # Object ownership trumps permission check for non-admin operations
            if not permission.endswith("admin"):
                return True

        return False

    @staticmethod
    def ensure_object_permission(
        user: User,
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
            )


# Create a singleton instance
permissions = PermissionChecker()
