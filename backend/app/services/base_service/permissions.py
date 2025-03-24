# /app/services/base_service/permissions.py
from __future__ import annotations

"""Permission handling for base service operations.

This module provides functionality for checking and enforcing permissions
in service operations, ensuring proper access control.
"""

from typing import Any, Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthenticationException, ErrorCode
from app.core.logging import get_logger
from app.domains.users.models import User

logger = get_logger("app.services.base_service.permissions")


class PermissionHelper:
    """Helper for permission-related operations."""

    @staticmethod
    async def get_user(db: AsyncSession, user_id: str) -> User:
        """Get user by ID.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            User: User model

        Raises:
            AuthenticationException: If user not found
        """
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()

        if not user:
            logger.warning(f"User with ID {user_id} not found")
            raise AuthenticationException(
                "User not found",
                code=ErrorCode.AUTHENTICATION_FAILED,
                details={"user_id": user_id},
                status_code=401,
            )

        return user

    @staticmethod
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

    @staticmethod
    def has_any_permission(user: User, permissions: list) -> bool:
        """Check if a user has any of the specified permissions.

        Args:
            user: User to check permissions for
            permissions: List of permissions to check

        Returns:
            bool: True if user has any permission, False otherwise
        """
        if not permissions:
            return True

        user_permissions = getattr(user, "permissions", [])
        user_roles = getattr(user, "roles", [])

        # Check direct permissions
        for permission in permissions:
            if permission in user_permissions:
                return True

        # Check role-based permissions
        for role in user_roles:
            role_permissions = getattr(role, "permissions", [])
            for permission in permissions:
                if permission in role_permissions:
                    return True

        return False

    @staticmethod
    def has_all_permissions(user: User, permissions: list) -> bool:
        """Check if a user has all specified permissions.

        Args:
            user: User to check permissions for
            permissions: List of permissions to check

        Returns:
            bool: True if user has all permissions, False otherwise
        """
        if not permissions:
            return True

        user_permissions = getattr(user, "permissions", [])
        user_roles = getattr(user, "roles", [])

        # Collect all permissions from user and roles
        all_user_permissions = set(user_permissions)
        for role in user_roles:
            role_permissions = getattr(role, "permissions", [])
            all_user_permissions.update(role_permissions)

        # Check if all required permissions are present
        return all(permission in all_user_permissions for permission in permissions)
