from __future__ import annotations
from datetime import datetime
from typing import Annotated, Dict, List, Optional, Union
from fastapi import Depends, HTTPException, Query, WebSocket, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocketDisconnect
from app.core.config import settings
from app.core.exceptions import AuthenticationException, ErrorCode, PermissionDeniedException
from app.core.logging import get_logger, set_user_id
from app.core.permissions import Permission, PermissionChecker
from app.core.security import TokenData, decode_token, oauth2_scheme
from app.db.session import get_db
from app.models.user import User, UserRole
from app.repositories.user import UserRepository
from app.utils.errors import ensure_not_none
logger = get_logger('app.api.deps')
PaginationParams = Dict[str, Union[int, float]]
async def get_current_user(db: AsyncSession=Depends(get_db), token: str=Depends(oauth2_scheme)) -> User:
    try:
        token_data = await decode_token(token)
        user_repo = UserRepository(db)
        user = await user_repo.get_by_id(token_data.sub)
        if user is None:
            logger.warning(f'User not found: {token_data.sub}')
            raise AuthenticationException(message='User not found', code=ErrorCode.AUTHENTICATION_FAILED)
        set_user_id(str(user.id))
        return user
    except (JWTError, ValidationError) as e:
        logger.warning(f'Token validation error: {str(e)}')
        raise AuthenticationException(message='Could not validate credentials', code=ErrorCode.AUTHENTICATION_FAILED) from e
async def get_current_active_user(current_user: User=Depends(get_current_user)) -> User:
    if not current_user.is_active:
        logger.warning(f'Inactive user attempted login: {current_user.id}')
        raise AuthenticationException(message='Inactive user', code=ErrorCode.USER_NOT_ACTIVE)
    return current_user
async def get_admin_user(current_user: User=Depends(get_current_active_user)) -> User:
    if not PermissionChecker.has_permission(current_user, Permission.SYSTEM_ADMIN):
        logger.warning(f'Non-admin user attempted admin action: {current_user.email}', extra={'user_id': str(current_user.id), 'role': current_user.role})
        raise PermissionDeniedException(message='Admin privileges required')
    return current_user
async def get_manager_user(current_user: User=Depends(get_current_active_user)) -> User:
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        logger.warning(f'Non-manager user attempted manager action: {current_user.email}', extra={'user_id': str(current_user.id), 'role': current_user.role})
        raise PermissionDeniedException(message='Manager privileges required')
    return current_user
async def get_optional_user(db: AsyncSession=Depends(get_db), token: Optional[str]=Depends(oauth2_scheme)) -> Optional[User]:
    if token is None:
        return None
    try:
        return await get_current_user(db, token)
    except AuthenticationException:
        return None
async def get_current_user_ws(websocket: WebSocket, db: AsyncSession=Depends(get_db)) -> User:
    try:
        token = websocket.query_params.get('token')
        if not token:
            cookies = websocket.cookies
            if 'token' in cookies:
                token = cookies['token']
        if not token:
            logger.warning('WebSocket connection without token')
            raise WebSocketDisconnect(code=status.WS_1008_POLICY_VIOLATION)
        token_data = await decode_token(token)
        user_repo = UserRepository(db)
        user = await user_repo.get_by_id(token_data.sub)
        if user is None or not user.is_active:
            logger.warning(f'WebSocket auth failed: User not found or inactive: {token_data.sub}')
            raise WebSocketDisconnect(code=status.WS_1008_POLICY_VIOLATION)
        return user
    except (JWTError, ValidationError, AuthenticationException) as e:
        logger.warning(f'WebSocket auth error: {str(e)}')
        raise WebSocketDisconnect(code=status.WS_1008_POLICY_VIOLATION)
def require_permissions(permissions: List[Permission], require_all: bool=True):
    async def dependency(current_user: User=Depends(get_current_active_user)):
        if not PermissionChecker.has_permissions(current_user, permissions, require_all):
            permission_str = ' and '.join((p.value for p in permissions)) if require_all else ' or '.join((p.value for p in permissions))
            logger.warning(f'Permission denied: {current_user.email} missing required permissions: {permission_str}', extra={'user_id': str(current_user.id), 'user_role': current_user.role, 'permissions': [p.value for p in permissions]})
            raise PermissionDeniedException(message=f"You don't have the required permissions: {permission_str}")
        return current_user
    return dependency
def require_permission(permission: Permission):
    return require_permissions([permission])
def get_pagination(page: int=Query(1, ge=1, description='Page number'), page_size: int=Query(20, ge=1, le=100, description='Items per page')) -> PaginationParams:
    skip = (page - 1) * page_size
    return {'skip': skip, 'limit': page_size, 'page': page, 'page_size': page_size}