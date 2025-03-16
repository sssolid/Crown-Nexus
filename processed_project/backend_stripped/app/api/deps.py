from __future__ import annotations
from datetime import datetime
from typing import Annotated, AsyncGenerator, Dict, Optional, Union
from fastapi import Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.user import TokenPayload
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{settings.API_V1_STR}/auth/login')
async def get_current_user(db: Annotated[AsyncSession, Depends(get_db)], token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials', headers={'WWW-Authenticate': 'Bearer'})
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        token_data = TokenPayload(**payload)
        if token_data.exp < int(datetime.utcnow().timestamp()):
            raise credentials_exception
    except (JWTError, ValidationError) as e:
        print(f'Token validation error: {str(e)}')
        raise credentials_exception from e
    stmt = select(User).where(User.id == token_data.sub)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user
async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Inactive user')
    return current_user
async def get_admin_user(current_user: Annotated[User, Depends(get_current_active_user)]) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Insufficient permissions')
    return current_user
async def get_manager_user(current_user: Annotated[User, Depends(get_current_active_user)]) -> User:
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Insufficient permissions')
    return current_user
PaginationParams = Dict[str, Union[int, float]]
def get_pagination(page: Annotated[int, Query(ge=1, description='Page number')]=1, page_size: Annotated[int, Query(ge=1, le=100, description='Items per page')]=20) -> PaginationParams:
    page = max(1, page)
    page_size = max(1, min(100, page_size))
    return {'skip': (page - 1) * page_size, 'limit': page_size, 'page': page, 'page_size': page_size}
async def get_optional_user(db: Annotated[AsyncSession, Depends(get_db)], token: str=Depends(OAuth2PasswordBearer(tokenUrl=f'{settings.API_V1_STR}/auth/login', auto_error=False))) -> Optional[User]:
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        token_data = TokenPayload(**payload)
        if token_data.exp < int(datetime.utcnow().timestamp()):
            return None
        stmt = select(User).where(User.id == token_data.sub)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        if user and user.is_active:
            return user
    except (JWTError, ValidationError):
        pass
    return None
async def get_current_user_ws(websocket: WebSocket, db: AsyncSession=Depends(get_db)) -> User:
    try:
        token = websocket.query_params.get('token')
        if not token and 'token' in websocket.cookies:
            token = websocket.cookies['token']
        if not token:
            headers = dict(websocket.headers)
            auth_header = headers.get('authorization', '')
            if auth_header.startswith('Bearer '):
                token = auth_header[7:]
        if not token:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            raise WebSocketDisconnect(code=status.WS_1008_POLICY_VIOLATION)
        credentials_exception = WebSocketDisconnect(code=status.WS_1008_POLICY_VIOLATION)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            token_data = TokenPayload(**payload)
            if token_data.exp < int(datetime.utcnow().timestamp()):
                await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
                raise credentials_exception
        except (JWTError, ValidationError) as e:
            logger.error(f'Token validation error: {str(e)}')
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            raise credentials_exception
        stmt = select(User).where(User.id == token_data.sub)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        if user is None or not user.is_active:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            raise credentials_exception
        return user
    except WebSocketDisconnect:
        raise
    except Exception as e:
        logger.exception(f'Error authenticating WebSocket: {e}')
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise WebSocketDisconnect(code=status.WS_1008_POLICY_VIOLATION)