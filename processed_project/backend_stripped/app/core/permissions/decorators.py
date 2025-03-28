from __future__ import annotations
'Permission requirement decorators.\n\nThis module provides decorators for enforcing permission requirements\nin API endpoints and service methods.\n'
from typing import Any, Callable, List, TypeVar, cast, TYPE_CHECKING
from app.core.exceptions import PermissionDeniedException
from app.logging import get_logger
from app.core.permissions.checker import PermissionChecker
from app.core.permissions.models import Permission
if TYPE_CHECKING:
    pass
logger = get_logger('app.core.permissions.decorators')
T = TypeVar('T', bound=Callable[..., Any])
def require_permission(permission: Permission) -> Callable[[T], T]:
    def decorator(func: T) -> T:
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_user = kwargs.get('current_user')
            if not current_user:
                for arg in args:
                    if hasattr(arg, 'is_active') and hasattr(arg, 'role'):
                        current_user = arg
                        break
            if not current_user:
                raise PermissionDeniedException(message='Authentication required')
            if not PermissionChecker.has_permission(current_user, permission):
                action = permission.split(':')[-1]
                resource = permission.split(':')[0]
                logger.warning(f"Permission denied: {getattr(current_user, 'email', 'Unknown')} tried to {action} {resource}", extra={'user_id': str(getattr(current_user, 'id', 'Unknown')), 'user_role': getattr(current_user, 'role', 'Unknown'), 'permission': permission})
                raise PermissionDeniedException(message=f"You don't have permission to {action} {resource}", action=action, resource_type=resource, permission=permission)
            return await func(*args, **kwargs)
        return cast(T, wrapper)
    return decorator
def require_permissions(permissions: List[Permission], require_all: bool=True) -> Callable[[T], T]:
    def decorator(func: T) -> T:
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_user = kwargs.get('current_user')
            if not current_user:
                for arg in args:
                    if hasattr(arg, 'is_active') and hasattr(arg, 'role'):
                        current_user = arg
                        break
            if not current_user:
                raise PermissionDeniedException(message='Authentication required')
            if not PermissionChecker.has_permissions(current_user, permissions, require_all):
                permission_str = ' and '.join((str(p) for p in permissions)) if require_all else ' or '.join((str(p) for p in permissions))
                logger.warning(f"Permission denied: {getattr(current_user, 'email', 'Unknown')} missing required permissions: {permission_str}", extra={'user_id': str(getattr(current_user, 'id', 'Unknown')), 'user_role': getattr(current_user, 'role', 'Unknown'), 'permissions': [str(p) for p in permissions]})
                raise PermissionDeniedException(message=f"You don't have the required permissions: {permission_str}")
            return await func(*args, **kwargs)
        return cast(T, wrapper)
    return decorator
def require_admin() -> Callable[[T], T]:
    return require_permission(Permission.SYSTEM_ADMIN)