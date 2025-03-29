from __future__ import annotations
'Permission utility functions.\n\nThis module provides utility functions for permission-related operations\nlike fetching users and checking specific permission patterns.\n'
from typing import Any, List, Optional, Set, Union, TYPE_CHECKING
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import AuthenticationException
from app.logging import get_logger
if TYPE_CHECKING:
    from app.domains.users.models import User
logger = get_logger('app.core.permissions.utils')
async def get_user_by_id(db: AsyncSession, user_id: str) -> 'User':
    from app.domains.users.models import User
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        logger.warning(f'User with ID {user_id} not found')
        raise AuthenticationException(message='User not found', details={'user_id': user_id})
    return user
def check_owner_permission(user_id: str, entity_user_id: Optional[Union[str, Any]], owner_field: str='user_id') -> bool:
    if entity_user_id is None:
        return False
    if hasattr(entity_user_id, 'hex'):
        return str(entity_user_id) == user_id
    return entity_user_id == user_id
def has_any_permission(user: 'User', permissions: List[str]) -> bool:
    if not permissions:
        return True
    user_permissions = getattr(user, 'permissions', [])
    user_roles = getattr(user, 'roles', [])
    role_permissions: Set[str] = set()
    for role in user_roles:
        role_perms = getattr(role, 'permissions', [])
        role_permissions.update(role_perms)
    from app.core.permissions.models import ROLE_PERMISSIONS
    static_permissions = ROLE_PERMISSIONS.get(user.role, set())
    all_permissions = set(user_permissions)
    all_permissions.update(role_permissions)
    all_permissions.update((p.value for p in static_permissions))
    return any((permission in all_permissions for permission in permissions))
def has_all_permissions(user: 'User', permissions: List[str]) -> bool:
    if not permissions:
        return True
    user_permissions = getattr(user, 'permissions', [])
    user_roles = getattr(user, 'roles', [])
    role_permissions: Set[str] = set()
    for role in user_roles:
        role_perms = getattr(role, 'permissions', [])
        role_permissions.update(role_perms)
    from app.core.permissions.models import ROLE_PERMISSIONS
    static_permissions = ROLE_PERMISSIONS.get(user.role, set())
    all_permissions = set(user_permissions)
    all_permissions.update(role_permissions)
    all_permissions.update((p.value for p in static_permissions))
    return all((permission in all_permissions for permission in permissions))