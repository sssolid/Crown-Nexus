# /app/core/permissions/models.py
from __future__ import annotations

"""Permission models and enums.

This module defines the permission types and role-based permission mappings
used throughout the application.
"""

import enum
from typing import Dict, Set, TYPE_CHECKING

# Use TYPE_CHECKING to avoid runtime circular imports
if TYPE_CHECKING:
    from app.domains.users.models import UserRole
else:
    # Define an enum for UserRole to avoid importing the actual model
    class UserRole(str, enum.Enum):
        """User roles in the system."""

        ADMIN = "admin"
        MANAGER = "manager"
        CLIENT = "client"
        DISTRIBUTOR = "distributor"
        READ_ONLY = "read_only"


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
ROLE_PERMISSIONS: Dict[UserRole, Set[Permission]] = {
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
