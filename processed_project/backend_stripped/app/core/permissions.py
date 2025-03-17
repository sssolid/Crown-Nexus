from __future__ import annotations
import enum
from typing import Any, Callable, Dict, List, Optional, Set, Type, TypeVar, Union, cast
from fastapi import Depends, HTTPException, Request, status
from pydantic import BaseModel
from app.core.exceptions import PermissionDeniedException
from app.core.logging import get_logger
from app.models.user import User, UserRole
logger = get_logger('app.core.permissions')
T = TypeVar('T', bound=Callable[..., Any])
class Permission(str, enum.Enum):
    USER_CREATE = 'user:create'
    USER_READ = 'user:read'
    USER_UPDATE = 'user:update'
    USER_DELETE = 'user:delete'
    USER_ADMIN = 'user:admin'
    PRODUCT_CREATE = 'product:create'
    PRODUCT_READ = 'product:read'
    PRODUCT_UPDATE = 'product:update'
    PRODUCT_DELETE = 'product:delete'
    PRODUCT_ADMIN = 'product:admin'
    MEDIA_CREATE = 'media:create'
    MEDIA_READ = 'media:read'
    MEDIA_UPDATE = 'media:update'
    MEDIA_DELETE = 'media:delete'
    MEDIA_ADMIN = 'media:admin'
    FITMENT_CREATE = 'fitment:create'
    FITMENT_READ = 'fitment:read'
    FITMENT_UPDATE = 'fitment:update'
    FITMENT_DELETE = 'fitment:delete'
    FITMENT_ADMIN = 'fitment:admin'
    COMPANY_CREATE = 'company:create'
    COMPANY_READ = 'company:read'
    COMPANY_UPDATE = 'company:update'
    COMPANY_DELETE = 'company:delete'
    COMPANY_ADMIN = 'company:admin'
    SYSTEM_ADMIN = 'system:admin'
ROLE_PERMISSIONS = {UserRole.ADMIN: {p for p in Permission}, UserRole.MANAGER: {Permission.USER_READ, Permission.USER_CREATE, Permission.USER_UPDATE, Permission.PRODUCT_READ, Permission.PRODUCT_CREATE, Permission.PRODUCT_UPDATE, Permission.PRODUCT_DELETE, Permission.PRODUCT_ADMIN, Permission.MEDIA_READ, Permission.MEDIA_CREATE, Permission.MEDIA_UPDATE, Permission.MEDIA_DELETE, Permission.MEDIA_ADMIN, Permission.FITMENT_READ, Permission.FITMENT_CREATE, Permission.FITMENT_UPDATE, Permission.FITMENT_DELETE, Permission.FITMENT_ADMIN, Permission.COMPANY_READ}, UserRole.CLIENT: {Permission.PRODUCT_READ, Permission.FITMENT_READ, Permission.MEDIA_READ, Permission.COMPANY_READ}, UserRole.DISTRIBUTOR: {Permission.PRODUCT_READ, Permission.FITMENT_READ, Permission.MEDIA_READ, Permission.MEDIA_CREATE, Permission.COMPANY_READ}, UserRole.READ_ONLY: {Permission.PRODUCT_READ, Permission.FITMENT_READ, Permission.MEDIA_READ, Permission.COMPANY_READ}}
class PermissionChecker:
    @staticmethod
    def has_permission(user: User, permission: Permission) -> bool:
        if not user or not user.is_active:
            return False
        role_permissions = ROLE_PERMISSIONS.get(user.role, set())
        return permission in role_permissions
    @staticmethod
    def has_permissions(user: User, permissions: List[Permission], require_all: bool=True) -> bool:
        if not permissions:
            return True
        if require_all:
            return all((PermissionChecker.has_permission(user, p) for p in permissions))
        else:
            return any((PermissionChecker.has_permission(user, p) for p in permissions))
    @staticmethod
    def require_permission(permission: Permission) -> Callable[[T], T]:
        def decorator(func: T) -> T:
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                current_user = kwargs.get('current_user')
                if not current_user:
                    for arg in args:
                        if isinstance(arg, User):
                            current_user = arg
                            break
                if not current_user:
                    raise PermissionDeniedException(message='Authentication required')
                if not PermissionChecker.has_permission(current_user, permission):
                    action = permission.split(':')[-1]
                    resource = permission.split(':')[0]
                    logger.warning(f'Permission denied: {current_user.email} tried to {action} {resource}', extra={'user_id': str(current_user.id), 'user_role': current_user.role, 'permission': permission})
                    raise PermissionDeniedException(message=f"You don't have permission to {action} {resource}")
                return await func(*args, **kwargs)
            return cast(T, wrapper)
        return decorator
    @staticmethod
    def require_permissions(permissions: List[Permission], require_all: bool=True) -> Callable[[T], T]:
        def decorator(func: T) -> T:
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                current_user = kwargs.get('current_user')
                if not current_user:
                    for arg in args:
                        if isinstance(arg, User):
                            current_user = arg
                            break
                if not current_user:
                    raise PermissionDeniedException(message='Authentication required')
                if not PermissionChecker.has_permissions(current_user, permissions, require_all):
                    permission_str = ' and '.join((p for p in permissions)) if require_all else ' or '.join((p for p in permissions))
                    logger.warning(f'Permission denied: {current_user.email} missing required permissions: {permission_str}', extra={'user_id': str(current_user.id), 'user_role': current_user.role, 'permissions': [p for p in permissions]})
                    raise PermissionDeniedException(message=f"You don't have the required permissions: {permission_str}")
                return await func(*args, **kwargs)
            return cast(T, wrapper)
        return decorator
    @staticmethod
    def require_admin() -> Callable[[T], T]:
        return PermissionChecker.require_permission(Permission.SYSTEM_ADMIN)
    @staticmethod
    def check_object_permission(user: User, obj: Any, permission: Permission, owner_field: str='created_by_id') -> bool:
        if PermissionChecker.has_permission(user, permission):
            return True
        if hasattr(obj, owner_field) and getattr(obj, owner_field) == user.id:
            if not permission.endswith('admin'):
                return True
        return False
    @staticmethod
    def ensure_object_permission(user: User, obj: Any, permission: Permission, owner_field: str='created_by_id') -> None:
        if not PermissionChecker.check_object_permission(user, obj, permission, owner_field):
            action = permission.split(':')[-1]
            resource = permission.split(':')[0]
            logger.warning(f'Object permission denied: {user.email} tried to {action} {resource}', extra={'user_id': str(user.id), 'user_role': user.role, 'permission': permission, 'object_id': getattr(obj, 'id', None), 'object_type': obj.__class__.__name__})
            raise PermissionDeniedException(message=f"You don't have permission to {action} this {resource}")
permissions = PermissionChecker()