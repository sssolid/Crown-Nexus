from __future__ import annotations

"""Permission service implementation.

This module provides a unified service interface for permission-related functions
throughout the application, integrating with the application's dependency management,
metrics, caching, and error handling systems.
"""

import time
from typing import Any, Dict, List, Optional, Set, Union, cast, TYPE_CHECKING

from app.core.dependency_manager import get_service, register_service
from app.core.error import handle_exception
from app.core.exceptions import AuthenticationException, PermissionDeniedException
from app.core.permissions.checker import PermissionChecker
from app.core.permissions.models import Permission, ROLE_PERMISSIONS
from app.core.permissions.utils import get_user_by_id, check_owner_permission
from app.logging import get_logger

if TYPE_CHECKING:
    from app.domains.users.models import User
    from sqlalchemy.ext.asyncio import AsyncSession

logger = get_logger("app.core.permissions.service")


class PermissionService:
    """Comprehensive permission service for the application.

    This service manages permission checking, caching of permission results,
    integration with metrics, and proper error handling for permission operations.
    """

    def __init__(self, db: Optional["AsyncSession"] = None) -> None:
        """Initialize the permission service.

        Args:
            db: Optional database session for operations requiring database access
        """
        self.db = db
        self.logger = get_logger("app.core.permissions.service")
        self.checker = PermissionChecker()

        # Get core services
        try:
            self.metrics_service = get_service("metrics_service")
        except Exception as e:
            self.logger.warning(f"Metrics service not available: {str(e)}")
            self.metrics_service = None

        try:
            self.cache_service = get_service("cache_service")
        except Exception as e:
            self.logger.warning(f"Cache service not available: {str(e)}")
            self.cache_service = None

        try:
            self.event_service = get_service("event_service")
        except Exception as e:
            self.logger.warning(f"Event service not available: {str(e)}")
            self.event_service = None

        try:
            self.error_service = get_service("error_service")
        except Exception as e:
            self.logger.warning(f"Error service not available: {str(e)}")
            self.error_service = None

        self.logger.info("Permission service initialized")

    async def initialize(self) -> None:
        """Initialize the permission service components."""
        self.logger.info("Initializing permission service")
        # Any async initialization tasks would go here

    async def shutdown(self) -> None:
        """Shutdown the permission service, releasing any resources."""
        self.logger.info("Shutting down permission service")
        # Any cleanup tasks would go here

    async def check_permission(
        self,
        user: "User",
        permission: Permission,
        resource_id: Optional[str] = None,
        resource_type: Optional[str] = None,
    ) -> bool:
        """Check if a user has the specified permission with metrics tracking.

        Args:
            user: The user to check permissions for
            permission: The permission to check
            resource_id: Optional resource ID for contextual logging
            resource_type: Optional resource type for contextual logging

        Returns:
            bool: True if the user has the permission
        """
        start_time = time.monotonic()
        has_permission = False

        try:
            # Try cache first if available
            if self.cache_service:
                cache_key = f"permission:check:{user.id}:{permission}"
                cached_result = await self.cache_service.get(cache_key)

                if cached_result is not None:
                    has_permission = cached_result

                    # Log cache hit/miss
                    self.logger.debug(
                        f"Permission check cache hit: {user.id}, {permission}",
                        user_id=str(user.id),
                        permission=str(permission),
                        result=has_permission,
                    )

                    # Track metrics if available
                    if self.metrics_service:
                        self.metrics_service.increment_counter(
                            "permission_check_cache_hits_total",
                            labels={
                                "permission": str(permission),
                                "granted": str(has_permission),
                            },
                        )

                    return has_permission

            # Not in cache or no cache available, check permission
            has_permission = self.checker.has_permission(user, permission)

            # Cache result if service available
            if self.cache_service:
                await self.cache_service.set(
                    f"permission:check:{user.id}:{permission}",
                    has_permission,
                    ttl=300,  # 5 minutes - balance between performance and security
                )

            # Log if denied
            if not has_permission:
                self.logger.warning(
                    "Permission denied",
                    user_id=str(user.id),
                    user_role=user.role,
                    permission=str(permission),
                    resource_id=resource_id,
                    resource_type=resource_type,
                )

            return has_permission

        except Exception as e:
            handle_exception(
                exception=e,
                user_id=str(getattr(user, "id", None)),
                function_name="check_permission",
            )
            return False

        finally:
            # Track metrics if available
            if self.metrics_service:
                duration = time.monotonic() - start_time
                self.metrics_service.observe_histogram(
                    "permission_check_duration_seconds",
                    duration,
                    {"permission": str(permission), "granted": str(has_permission)},
                )
                self.metrics_service.increment_counter(
                    "permission_checks_total",
                    labels={
                        "permission": str(permission),
                        "granted": str(has_permission),
                    },
                )

    async def check_permissions(
        self,
        user: "User",
        permissions: List[Permission],
        require_all: bool = True,
        resource_id: Optional[str] = None,
        resource_type: Optional[str] = None,
    ) -> bool:
        """Check if a user has multiple permissions.

        Args:
            user: The user to check permissions for
            permissions: List of permissions to check
            require_all: Whether all permissions are required (True) or any (False)
            resource_id: Optional resource ID for contextual logging
            resource_type: Optional resource type for contextual logging

        Returns:
            bool: True if the user has the required permissions
        """
        start_time = time.monotonic()
        result = False

        try:
            # Fast path for empty permissions list
            if not permissions:
                return True

            # Fast path for single permission
            if len(permissions) == 1:
                return await self.check_permission(
                    user, permissions[0], resource_id, resource_type
                )

            # Multiple permissions check
            permission_results = {}

            # Check each permission with caching
            for permission in permissions:
                permission_results[str(permission)] = await self.check_permission(
                    user, permission, resource_id, resource_type
                )

                # Short-circuit for performance
                if require_all and not permission_results[str(permission)]:
                    result = False
                    break
                elif not require_all and permission_results[str(permission)]:
                    result = True
                    break

            # Calculate final result if not short-circuited
            if require_all:
                result = all(permission_results.values())
            else:
                result = any(permission_results.values())

            # Log if denied
            if not result:
                self.logger.warning(
                    "Multiple permissions check failed",
                    user_id=str(user.id),
                    user_role=user.role,
                    permissions=str(permissions),
                    require_all=require_all,
                    results=permission_results,
                    resource_id=resource_id,
                    resource_type=resource_type,
                )

            return result

        except Exception as e:
            handle_exception(
                exception=e,
                user_id=str(getattr(user, "id", None)),
                function_name="check_permissions",
            )
            return False

        finally:
            # Track metrics if available
            if self.metrics_service:
                duration = time.monotonic() - start_time
                self.metrics_service.observe_histogram(
                    "multiple_permissions_check_duration_seconds",
                    duration,
                    {
                        "permissions_count": str(len(permissions)),
                        "require_all": str(require_all),
                        "granted": str(result),
                    },
                )
                self.metrics_service.increment_counter(
                    "multiple_permissions_checks_total",
                    labels={
                        "permissions_count": str(len(permissions)),
                        "require_all": str(require_all),
                        "granted": str(result),
                    },
                )

    async def check_object_permission(
        self,
        user: "User",
        obj: Any,
        permission: Permission,
        owner_field: str = "created_by_id",
    ) -> bool:
        """Check if a user has permission for a specific object.

        Args:
            user: The user to check
            obj: The object to check permissions for
            permission: The permission to check
            owner_field: The field name containing the owner's ID

        Returns:
            bool: True if the user has permission for this object
        """
        start_time = time.monotonic()
        result = False

        try:
            result = self.checker.check_object_permission(
                user, obj, permission, owner_field
            )

            # Log if denied
            if not result:
                obj_id = getattr(obj, "id", None)
                obj_type = obj.__class__.__name__

                self.logger.warning(
                    "Object permission denied",
                    user_id=str(user.id),
                    user_role=user.role,
                    permission=str(permission),
                    object_id=obj_id,
                    object_type=obj_type,
                    owner_field=owner_field,
                )

            return result

        except Exception as e:
            handle_exception(
                exception=e,
                user_id=str(getattr(user, "id", None)),
                function_name="check_object_permission",
            )
            return False

        finally:
            # Track metrics if available
            if self.metrics_service:
                duration = time.monotonic() - start_time
                self.metrics_service.observe_histogram(
                    "object_permission_check_duration_seconds",
                    duration,
                    {
                        "permission": str(permission),
                        "granted": str(result),
                        "object_type": obj.__class__.__name__,
                    },
                )
                self.metrics_service.increment_counter(
                    "object_permission_checks_total",
                    labels={
                        "permission": str(permission),
                        "granted": str(result),
                        "object_type": obj.__class__.__name__,
                    },
                )

    async def ensure_permission(
        self,
        user: "User",
        permission: Permission,
        resource_type: str,
        resource_id: Optional[str] = None,
    ) -> None:
        """Ensure a user has permission, raising an exception if not.

        Args:
            user: The user to check
            permission: The permission to check
            resource_type: The type of resource being accessed
            resource_id: Optional ID of the resource being accessed

        Raises:
            PermissionDeniedException: If the user doesn't have the permission
        """
        has_permission = await self.check_permission(
            user, permission, resource_id, resource_type
        )

        if not has_permission:
            action = str(permission).split(":")[-1]

            # Publish permission denied event if service available
            if self.event_service:
                await self.event_service.publish(
                    event_name="permission.denied",
                    payload={
                        "user_id": str(user.id),
                        "permission": str(permission),
                        "resource_type": resource_type,
                        "resource_id": resource_id,
                        "action": action,
                    },
                )

            # Use error service if available, otherwise raise directly
            if self.error_service:
                raise self.error_service.permission_denied(
                    action=action,
                    resource_type=resource_type,
                    permission=str(permission),
                )
            else:
                raise PermissionDeniedException(
                    message=f"Permission denied to {action} {resource_type}",
                    action=action,
                    resource_type=resource_type,
                    permission=str(permission),
                )

    async def ensure_object_permission(
        self,
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
        has_permission = await self.check_object_permission(
            user, obj, permission, owner_field
        )

        if not has_permission:
            action = str(permission).split(":")[-1]
            resource = str(permission).split(":")[0]
            obj_id = getattr(obj, "id", None)
            obj_type = obj.__class__.__name__

            # Publish permission denied event if service available
            if self.event_service:
                await self.event_service.publish(
                    event_name="permission.object_denied",
                    payload={
                        "user_id": str(user.id),
                        "permission": str(permission),
                        "object_type": obj_type,
                        "object_id": obj_id,
                        "action": action,
                        "resource": resource,
                    },
                )

            # Use error service if available, otherwise raise directly
            if self.error_service:
                raise self.error_service.permission_denied(
                    action=action, resource_type=resource, permission=str(permission)
                )
            else:
                raise PermissionDeniedException(
                    message=f"Permission denied to {action} this {resource}",
                    action=action,
                    resource_type=resource,
                    permission=str(permission),
                )

    async def get_user_permissions(self, user_id: str) -> Set[Permission]:
        """Get all permissions for a user with caching.

        Args:
            user_id: The user ID to get permissions for

        Returns:
            Set[Permission]: Set of all permissions the user has

        Raises:
            AuthenticationException: If the user doesn't exist
        """
        if not self.db:
            raise ValueError("Database session required to get user permissions")

        start_time = time.monotonic()

        try:
            # Try cache first if available
            if self.cache_service:
                cache_key = f"permissions:user:{user_id}"
                cached_permissions = await self.cache_service.get(cache_key)

                if cached_permissions is not None:
                    # Log cache hit
                    self.logger.debug(
                        f"User permissions cache hit: {user_id}",
                        user_id=user_id,
                        permissions_count=len(cached_permissions),
                    )

                    # Track metrics if available
                    if self.metrics_service:
                        self.metrics_service.increment_counter(
                            "user_permissions_cache_hits_total"
                        )

                    # Convert cached string permissions back to enum values
                    return {
                        Permission(p)
                        for p in cached_permissions
                        if p in Permission._value2member_map_
                    }

            # Cache miss or no cache - fetch user and determine permissions
            user = await get_user_by_id(self.db, user_id)

            # Get permissions from role
            role_permissions = ROLE_PERMISSIONS.get(user.role, set())

            # Get explicit user permissions
            user_permissions = getattr(user, "permissions", [])

            # Combine permissions
            if isinstance(role_permissions, set):
                all_permissions = role_permissions.copy()
            else:
                all_permissions = set(role_permissions)

            if user_permissions:
                all_permissions.update(user_permissions)

            # Cache for future requests if service available
            if self.cache_service:
                await self.cache_service.set(
                    f"permissions:user:{user_id}",
                    [p.value for p in all_permissions],
                    ttl=300,  # 5 minutes - balance between performance and security
                )

            return all_permissions

        except AuthenticationException:
            # Re-raise authentication exceptions
            raise

        except Exception as e:
            handle_exception(
                exception=e, user_id=user_id, function_name="get_user_permissions"
            )
            raise

        finally:
            # Track metrics if available
            if self.metrics_service:
                duration = time.monotonic() - start_time
                self.metrics_service.observe_histogram(
                    "get_user_permissions_duration_seconds", duration
                )

    async def invalidate_permissions_cache(self, user_id: str) -> None:
        """Invalidate cached permissions for a user.

        Args:
            user_id: The user ID to invalidate permissions for
        """
        if not self.cache_service:
            return

        try:
            cache_key = f"permissions:user:{user_id}"
            await self.cache_service.delete(cache_key)

            # Also invalidate any specific permission checks
            await self.cache_service.invalidate_pattern(f"permission:check:{user_id}:*")

            self.logger.debug(
                f"Invalidated permissions cache for user: {user_id}", user_id=user_id
            )

        except Exception as e:
            self.logger.warning(
                f"Failed to invalidate permissions cache: {str(e)}",
                user_id=user_id,
                exc_info=True,
            )


# Create a singleton instance for dependency injection
_permission_service: Optional[PermissionService] = None


@register_service
def get_permission_service(db: Optional["AsyncSession"] = None) -> PermissionService:
    """Get or create a PermissionService instance.

    Args:
        db: Optional database session

    Returns:
        PermissionService: The permission service instance
    """
    global _permission_service
    if _permission_service is None:
        _permission_service = PermissionService(db)
    elif db is not None:
        _permission_service.db = db
    return _permission_service
