from __future__ import annotations
from datetime import datetime, timedelta
from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_active_user, get_db
from app.core.config import settings
from app.models.user import User, UserRole, create_access_token, verify_password
from app.schemas.user import Token, TokenPayload, User as UserSchema
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{settings.API_V1_STR}/auth/login')
@router.post('/login', response_model=Token)
async def login_for_access_token(db: Annotated[AsyncSession, Depends(get_db)], form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Any:
    stmt = select(User).where(User.email == form_data.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect email or password', headers={'WWW-Authenticate': 'Bearer'})
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Inactive user account')
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(subject=str(user.id), role=user.role, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}
@router.get('/validate-token')
async def validate_token(token: Annotated[TokenPayload, Depends(get_current_active_user)]) -> dict:
    return {'valid': True}
@router.get('/me', response_model=UserSchema)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]) -> Any:
    return current_user