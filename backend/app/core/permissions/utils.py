# /app/core/permissions/utils.py
from __future__ import annotations

"""Permission utility functions.

This module provides utility functions for permission-related operations
like fetching users and checking specific permission patterns.
"""

from typing import Any, List, Optional, Set, Union, TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthenticationException
from app.core.logging import get_logger

if TYPE_CHECKING:
    from app.domains.users.models import User

logger = get_logger(__name__)


async def get_user_by_id(db: AsyncSession, user_id: str) -> "User":
    """Get user by ID.

    Args:
        db: Database session
        user_id: User ID

    Returns:
        User: User model

    Raises:
        AuthenticationException: If user not found
    """
    # Import User model here to avoid circular imports
    from app.domains.users.models import User

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        logger.warning(f"User with ID {user_id} not found")
        raise AuthenticationException(
            message="User not found",
            details={"user_id": user_id},
        )

    return user


def check_owner_permission(
    user_id: str,
    entity_user_id: Optional[Union[str, Any]],
    owner_field: str = "user_id",
) -> bool:
    """Check if a user is the owner of an entity.

    Args:
        user_id: User ID to check
        entity_user_id: User ID from the entity
        owner_field: Field name containing the owner ID

    Returns:
        bool: True if user is the owner, False otherwise
    """
    if entity_user_id is None:
        return False

    # Handle UUID objects
    if hasattr(entity_user_id, "hex"):
        return str(entity_user_id) == user_id

    return entity_user_id == user_id


def has_any_permission(user: "User", permissions: List[str]) -> bool:
    """Check if a user has any of the specified permissions.

    Args:
        user: User to check permissions for
        permissions: List of permissions to check

    Returns:
        bool: True if user has any permission, False otherwise
    """
    if not permissions:
        return True

    # Get user permissions (direct permissions)
    user_permissions = getattr(user, "permissions", [])

    # Get permissions from user roles
    user_roles = getattr(user, "roles", [])
    role_permissions: Set[str] = set()
    for role in user_roles:
        role_perms = getattr(role, "permissions", [])
        role_permissions.update(role_perms)

    # Also check role-based permissions from the static mapping
    from app.core.permissions.models import ROLE_PERMISSIONS

    static_permissions = ROLE_PERMISSIONS.get(user.role, set())

    # Combine all sources of permissions
    all_permissions = set(user_permissions)
    all_permissions.update(role_permissions)
    all_permissions.update(p.value for p in static_permissions)

    # Check if any required permission is present
    return any(permission in all_permissions for permission in permissions)


def has_all_permissions(user: "User", permissions: List[str]) -> bool:
    """Check if a user has all specified permissions.

    Args:
        user: User to check permissions for
        permissions: List of permissions to check

    Returns:
        bool: True if user has all permissions, False otherwise
    """
    if not permissions:
        return True

    # Get user permissions (direct permissions)
    user_permissions = getattr(user, "permissions", [])

    # Get permissions from user roles
    user_roles = getattr(user, "roles", [])
    role_permissions: Set[str] = set()
    for role in user_roles:
        role_perms = getattr(role, "permissions", [])
        role_permissions.update(role_perms)

    # Also check role-based permissions from the static mapping
    from app.core.permissions.models import ROLE_PERMISSIONS

    static_permissions = ROLE_PERMISSIONS.get(user.role, set())

    # Combine all sources of permissions
    all_permissions = set(user_permissions)
    all_permissions.update(role_permissions)
    all_permissions.update(p.value for p in static_permissions)

    # Check if all required permissions are present
    return all(permission in all_permissions for permission in permissions)
