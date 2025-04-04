from __future__ import annotations
'Permission utility functions.\n\nThis module provides utility functions for permission-related operations\nlike fetching users and checking specific permission patterns.\n'
from typing import Any, List, Optional, Set, Union, TYPE_CHECKING
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependency_manager import get_service
from app.core.error import handle_exception
from app.core.exceptions import AuthenticationException
from app.logging import get_logger
if TYPE_CHECKING:
    from app.domains.users.models import User
logger = get_logger('app.core.permissions.utils')
async def get_user_by_id(db: AsyncSession, user_id: str) -> 'User':
    try:
        from app.domains.users.models import User
        try:
            cache_service = get_service('cache_service')
            cache_key = f'user:{user_id}'
            cached_user = await cache_service.get(cache_key)
            if cached_user is not None:
                logger.debug(f'User cache hit: {user_id}')
                return cached_user
        except Exception:
            pass
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            logger.warning(f'User with ID {user_id} not found')
            raise AuthenticationException(message='User not found', details={'user_id': user_id})
        try:
            cache_service = get_service('cache_service')
            await cache_service.set(cache_key, user, ttl=300)
        except Exception:
            pass
        return user
    except AuthenticationException:
        raise
    except Exception as e:
        handle_exception(e, user_id=user_id)
        raise AuthenticationException(message='Failed to retrieve user', details={'user_id': user_id, 'error': str(e)}) from e
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