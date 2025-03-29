from __future__ import annotations

"""Permission utility functions.

This module provides utility functions for permission-related operations
like fetching users and checking specific permission patterns.
"""

from typing import Any, List, Optional, Set, Union, TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependency_manager import get_service
from app.core.error import handle_exception
from app.core.exceptions import AuthenticationException
from app.logging import get_logger

if TYPE_CHECKING:
    from app.domains.users.models import User

logger = get_logger("app.core.permissions.utils")


async def get_user_by_id(db: AsyncSession, user_id: str) -> "User":
    """Get a user by ID from the database.

    Args:
        db: Database session
        user_id: ID of the user to retrieve

    Returns:
        User: The user object

    Raises:
        AuthenticationException: If the user is not found
    """
    try:
        from app.domains.users.models import User

        # Try to use cache first if available
        try:
            cache_service = get_service("cache_service")
            cache_key = f"user:{user_id}"
            cached_user = await cache_service.get(cache_key)

            if cached_user is not None:
                logger.debug(f"User cache hit: {user_id}")
                return cached_user
        except Exception:
            pass

        # Cache miss or no cache - fetch from database
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()

        if not user:
            logger.warning(f"User with ID {user_id} not found")
            raise AuthenticationException(
                message="User not found", details={"user_id": user_id}
            )

        # Cache for future requests if service available
        try:
            cache_service = get_service("cache_service")
            await cache_service.set(cache_key, user, ttl=300)  # 5 minutes TTL
        except Exception:
            pass

        return user
    except AuthenticationException:
        raise
    except Exception as e:
        handle_exception(e, user_id=user_id)
        raise AuthenticationException(
            message="Failed to retrieve user",
            details={"user_id": user_id, "error": str(e)},
        ) from e


def check_owner_permission(
    user_id: str,
    entity_user_id: Optional[Union[str, Any]],
    owner_field: str = "user_id",
) -> bool:
    """Check if a user is the owner of an entity.

    Args:
        user_id: The user ID
        entity_user_id: The user ID stored in the entity
        owner_field: The field name used for ownership

    Returns:
        bool: True if the user is the owner
    """
    if entity_user_id is None:
        return False

    # Handle UUID objects
    if hasattr(entity_user_id, "hex"):
        return str(entity_user_id) == user_id

    # Direct comparison
    return entity_user_id == user_id


def has_any_permission(user: "User", permissions: List[str]) -> bool:
    """Check if a user has any of the specified permissions.

    Args:
        user: The user to check
        permissions: List of permission strings to check

    Returns:
        bool: True if the user has any of the permissions
    """
    if not permissions:
        return True

    # Get user permissions
    user_permissions = getattr(user, "permissions", [])

    # Get permissions from user roles
    user_roles = getattr(user, "roles", [])
    role_permissions: Set[str] = set()
    for role in user_roles:
        role_perms = getattr(role, "permissions", [])
        role_permissions.update(role_perms)

    # Get permissions from static role mapping
    from app.core.permissions.models import ROLE_PERMISSIONS

    static_permissions = ROLE_PERMISSIONS.get(user.role, set())

    # Combine all permissions
    all_permissions = set(user_permissions)
    all_permissions.update(role_permissions)
    all_permissions.update(p.value for p in static_permissions)

    # Check if any required permission is in the user's permissions
    return any(permission in all_permissions for permission in permissions)


def has_all_permissions(user: "User", permissions: List[str]) -> bool:
    """Check if a user has all of the specified permissions.

    Args:
        user: The user to check
        permissions: List of permission strings to check

    Returns:
        bool: True if the user has all of the permissions
    """
    if not permissions:
        return True

    # Get user permissions
    user_permissions = getattr(user, "permissions", [])

    # Get permissions from user roles
    user_roles = getattr(user, "roles", [])
    role_permissions: Set[str] = set()
    for role in user_roles:
        role_perms = getattr(role, "permissions", [])
        role_permissions.update(role_perms)

    # Get permissions from static role mapping
    from app.core.permissions.models import ROLE_PERMISSIONS

    static_permissions = ROLE_PERMISSIONS.get(user.role, set())

    # Combine all permissions
    all_permissions = set(user_permissions)
    all_permissions.update(role_permissions)
    all_permissions.update(p.value for p in static_permissions)

    # Check if all required permissions are in the user's permissions
    return all(permission in all_permissions for permission in permissions)
