from __future__ import annotations

"""Permission requirement decorators.

This module provides decorators for enforcing permission requirements
in API endpoints and service methods.
"""

import functools
import time
from typing import Any, Callable, List, TypeVar, cast, TYPE_CHECKING

from app.core.dependency_manager import get_service
from app.core.exceptions import PermissionDeniedException
from app.logging import get_logger
from app.core.permissions.checker import PermissionChecker
from app.core.permissions.models import Permission

if TYPE_CHECKING:
    from app.domains.users.models import User

logger = get_logger("app.core.permissions.decorators")

T = TypeVar("T", bound=Callable[..., Any])


def require_permission(permission: Permission) -> Callable[[T], T]:
    """Decorator to require a permission for a function.

    Args:
        permission: The permission required to execute the function

    Returns:
        Callable: Decorator function
    """

    def decorator(func: T) -> T:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Find the current user from arguments
            current_user = kwargs.get("current_user")
            if not current_user:
                for arg in args:
                    if hasattr(arg, "is_active") and hasattr(arg, "role"):
                        current_user = arg
                        break

            # Verify we have a user
            if not current_user:
                raise PermissionDeniedException(message="Authentication required")

            start_time = time.monotonic()

            # Try to use the permission service if available
            try:
                permission_service = get_service("permission_service")
                await permission_service.ensure_permission(
                    current_user,
                    permission,
                    resource_type=str(permission).split(":")[0],
                )
            except Exception:
                # Fall back to direct permission check if service unavailable
                if not PermissionChecker.has_permission(current_user, permission):
                    action = str(permission).split(":")[-1]
                    resource = str(permission).split(":")[0]

                    logger.warning(
                        f"Permission denied: {getattr(current_user, 'email', 'Unknown')} tried to {action} {resource}",
                        user_id=str(getattr(current_user, "id", "Unknown")),
                        user_role=getattr(current_user, "role", "Unknown"),
                        permission=str(permission),
                    )

                    raise PermissionDeniedException(
                        message=f"You don't have permission to {action} {resource}",
                        action=action,
                        resource_type=resource,
                        permission=str(permission),
                    )

            # Track metrics if available
            try:
                metrics_service = get_service("metrics_service")
                duration = time.monotonic() - start_time
                metrics_service.observe_histogram(
                    "permission_decorator_duration_seconds",
                    duration,
                    {"permission": str(permission)},
                )
            except Exception:
                pass

            # Execute the wrapped function
            return await func(*args, **kwargs)

        return cast(T, wrapper)

    return decorator


def require_permissions(
    permissions: List[Permission], require_all: bool = True
) -> Callable[[T], T]:
    """Decorator to require multiple permissions for a function.

    Args:
        permissions: List of permissions to check
        require_all: Whether all permissions are required (True) or any (False)

    Returns:
        Callable: Decorator function
    """

    def decorator(func: T) -> T:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Find the current user from arguments
            current_user = kwargs.get("current_user")
            if not current_user:
                for arg in args:
                    if hasattr(arg, "is_active") and hasattr(arg, "role"):
                        current_user = arg
                        break

            # Verify we have a user
            if not current_user:
                raise PermissionDeniedException(message="Authentication required")

            start_time = time.monotonic()

            # Try to use the permission service if available
            try:
                permission_service = get_service("permission_service")
                has_permissions = await permission_service.check_permissions(
                    current_user, permissions, require_all=require_all
                )

                if not has_permissions:
                    permission_str = (
                        " and ".join(str(p) for p in permissions)
                        if require_all
                        else " or ".join(str(p) for p in permissions)
                    )

                    logger.warning(
                        f"Permission denied: {getattr(current_user, 'email', 'Unknown')} missing required permissions: {permission_str}",
                        user_id=str(getattr(current_user, "id", "Unknown")),
                        user_role=getattr(current_user, "role", "Unknown"),
                        permissions=[str(p) for p in permissions],
                    )

                    raise PermissionDeniedException(
                        message=f"You don't have the required permissions: {permission_str}"
                    )
            except PermissionDeniedException:
                raise
            except Exception:
                # Fall back to direct permission check if service unavailable
                if not PermissionChecker.has_permissions(
                    current_user, permissions, require_all
                ):
                    permission_str = (
                        " and ".join(str(p) for p in permissions)
                        if require_all
                        else " or ".join(str(p) for p in permissions)
                    )

                    logger.warning(
                        f"Permission denied: {getattr(current_user, 'email', 'Unknown')} missing required permissions: {permission_str}",
                        user_id=str(getattr(current_user, "id", "Unknown")),
                        user_role=getattr(current_user, "role", "Unknown"),
                        permissions=[str(p) for p in permissions],
                    )

                    raise PermissionDeniedException(
                        message=f"You don't have the required permissions: {permission_str}"
                    )

            # Track metrics if available
            try:
                metrics_service = get_service("metrics_service")
                duration = time.monotonic() - start_time
                metrics_service.observe_histogram(
                    "multiple_permissions_decorator_duration_seconds",
                    duration,
                    {
                        "permissions_count": str(len(permissions)),
                        "require_all": str(require_all),
                    },
                )
            except Exception:
                pass

            # Execute the wrapped function
            return await func(*args, **kwargs)

        return cast(T, wrapper)

    return decorator


def require_admin() -> Callable[[T], T]:
    """Decorator to require system admin permission.

    Returns:
        Callable: Decorator function requiring SYSTEM_ADMIN permission
    """
    return require_permission(Permission.SYSTEM_ADMIN)
