from __future__ import annotations
'Permission checker for authorization control.\n\nThis module provides the core permission checking functionality to determine\nif users have the required permissions for various actions.\n'
from typing import Any, List, TYPE_CHECKING
from app.core.exceptions import PermissionDeniedException
from app.logging import get_logger
from app.core.permissions.models import Permission, ROLE_PERMISSIONS
if TYPE_CHECKING:
    from app.domains.users.models import User
logger = get_logger('app.core.permissions.checkers')
class PermissionChecker:
    @staticmethod
    def has_permission(user: 'User', permission: Permission) -> bool:
        if not user or not user.is_active:
            return False
        role_permissions = ROLE_PERMISSIONS.get(user.role, set())
        user_permissions = getattr(user, 'permissions', [])
        if permission in user_permissions:
            return True
        user_roles = getattr(user, 'roles', [])
        for role in user_roles:
            role_permissions = getattr(role, 'permissions', [])
            if permission in role_permissions:
                return True
        return permission in role_permissions
    @staticmethod
    def has_permissions(user: 'User', permissions: List[Permission], require_all: bool=True) -> bool:
        if not permissions:
            return True
        if require_all:
            return all((PermissionChecker.has_permission(user, p) for p in permissions))
        else:
            return any((PermissionChecker.has_permission(user, p) for p in permissions))
    @staticmethod
    def check_object_permission(user: 'User', obj: Any, permission: Permission, owner_field: str='created_by_id') -> bool:
        if PermissionChecker.has_permission(user, permission):
            return True
        if hasattr(obj, owner_field):
            entity_user_id = getattr(obj, owner_field)
            if hasattr(entity_user_id, 'hex'):
                entity_user_id = str(entity_user_id)
            if entity_user_id == str(user.id):
                if not permission.endswith('admin'):
                    return True
        return False
    @staticmethod
    def ensure_object_permission(user: 'User', obj: Any, permission: Permission, owner_field: str='created_by_id') -> None:
        if not PermissionChecker.check_object_permission(user, obj, permission, owner_field):
            action = permission.split(':')[-1]
            resource = permission.split(':')[0]
            logger.warning(f'Object permission denied: {user.email} tried to {action} {resource}', extra={'user_id': str(user.id), 'user_role': user.role, 'permission': permission, 'object_id': getattr(obj, 'id', None), 'object_type': obj.__class__.__name__})
            raise PermissionDeniedException(message=f"You don't have permission to {action} this {resource}", action=action, resource_type=resource, permission=permission)
permissions = PermissionChecker()