from __future__ import annotations
'Permission handling for base service operations.\n\nThis module provides functionality for checking and enforcing permissions\nin service operations, ensuring proper access control.\n'
from typing import Any, Optional, Union
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import AuthenticationException, ErrorCode
from app.logging import get_logger
from app.domains.users.models import User
logger = get_logger('app.services.base_service.permissions')
class PermissionHelper:
    @staticmethod
    async def get_user(db: AsyncSession, user_id: str) -> User:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            logger.warning(f'User with ID {user_id} not found')
            raise AuthenticationException('User not found', code=ErrorCode.AUTHENTICATION_FAILED, details={'user_id': user_id}, status_code=401)
        return user
    @staticmethod
    def check_owner_permission(user_id: str, entity_user_id: Optional[Union[str, Any]], owner_field: str='user_id') -> bool:
        if entity_user_id is None:
            return False
        if hasattr(entity_user_id, 'hex'):
            return str(entity_user_id) == user_id
        return entity_user_id == user_id
    @staticmethod
    def has_any_permission(user: User, permissions: list) -> bool:
        if not permissions:
            return True
        user_permissions = getattr(user, 'permissions', [])
        user_roles = getattr(user, 'roles', [])
        for permission in permissions:
            if permission in user_permissions:
                return True
        for role in user_roles:
            role_permissions = getattr(role, 'permissions', [])
            for permission in permissions:
                if permission in role_permissions:
                    return True
        return False
    @staticmethod
    def has_all_permissions(user: User, permissions: list) -> bool:
        if not permissions:
            return True
        user_permissions = getattr(user, 'permissions', [])
        user_roles = getattr(user, 'roles', [])
        all_user_permissions = set(user_permissions)
        for role in user_roles:
            role_permissions = getattr(role, 'permissions', [])
            all_user_permissions.update(role_permissions)
        return all((permission in all_user_permissions for permission in permissions))