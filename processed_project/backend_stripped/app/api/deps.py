from __future__ import annotations
from typing import Dict, List, Optional, Union, Callable
from app.core.security.dependencies import optional_oauth2_scheme
from app.core.audit.service import AuditService
from fastapi import Depends, Query, WebSocket, status
from jose import JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocketDisconnect
from app.core.exceptions import AuthenticationException, PermissionDeniedException, RateLimitException
from app.logging import get_logger, set_user_id
from app.core.permissions import Permission, PermissionChecker
from app.core.rate_limiting import RateLimiter, RateLimitRule
from app.core.security import decode_token, oauth2_scheme
from app.db.session import get_db
from app.domains.users.models import User, UserRole
from app.domains.users.repository import UserRepository
logger = get_logger('app.api.deps')
PaginationParams = Dict[str, Union[int, float]]
async def get_audit_service(db: AsyncSession=Depends(get_db)) -> AuditService:
    return AuditService(db)
def rate_limit(requests_per_window: int=10, window_seconds: int=60) -> Callable:
    limiter = RateLimiter()
    rule = RateLimitRule(requests_per_window=requests_per_window, window_seconds=window_seconds)
    async def limit_requests(request: Request, error_handling_service: ErrorHandlingService=Depends(get_error_handling_service)) -> None:
        key = limiter.get_key_for_request(request, rule)
        is_limited, count, limit = await limiter.is_rate_limited(key, rule)
        if is_limited:
            headers = {'Retry-After': str(window_seconds), 'X-RateLimit-Limit': str(limit), 'X-RateLimit-Remaining': '0', 'X-RateLimit-Reset': str(window_seconds)}
            raise RateLimitException(message='Rate limit exceeded')
    return limit_requests
async def get_current_user(db: AsyncSession=Depends(get_db), token: str=Depends(oauth2_scheme)) -> User:
    try:
        token_data = await decode_token(token)
        user_repo = UserRepository(db)
        user = await user_repo.get_by_id(token_data.sub)
        if user is None:
            logger.warning(f'User not found: {token_data.sub}')
            raise AuthenticationException(message='User not found')
        set_user_id(str(user.id))
        return user
    except (JWTError, ValidationError) as e:
        logger.warning(f'Token validation error: {str(e)}')
        raise AuthenticationException(message='Could not validate credentials') from e
async def get_current_active_user(current_user: User=Depends(get_current_user)) -> User:
    if not current_user.is_active:
        logger.warning(f'Inactive user attempted login: {current_user.id}')
        raise AuthenticationException(message='Inactive user')
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
async def get_optional_user(db: AsyncSession=Depends(get_db), token: Optional[str]=Depends(optional_oauth2_scheme)) -> Optional[User]:
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
        raise WebSocketDisconnect(code=status.WS_1008_POLICY_VIOLATION) from e
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