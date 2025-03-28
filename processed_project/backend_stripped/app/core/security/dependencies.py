from __future__ import annotations
'FastAPI security dependencies.\n\nThis module provides dependency functions for FastAPI to handle authentication\nand authorization in request handlers.\n'
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.core.exceptions import AuthenticationException
from app.logging import get_logger
from app.core.security.tokens import decode_token
logger = get_logger('app.core.security.dependencies')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{settings.API_V1_STR}/auth/login')
optional_oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{settings.API_V1_STR}/auth/login', auto_error=False)
async def get_token_from_header(token: str=Depends(oauth2_scheme)) -> str:
    return token
async def get_current_user_id(token: str=Depends(get_token_from_header)) -> str:
    try:
        token_data = await decode_token(token)
        return token_data.sub
    except AuthenticationException:
        raise
    except Exception as e:
        logger.error(f'Error getting user ID from token: {str(e)}')
        raise AuthenticationException(message='Could not authenticate user') from e