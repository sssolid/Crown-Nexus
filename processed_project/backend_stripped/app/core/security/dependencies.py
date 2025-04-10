from __future__ import annotations
'FastAPI security dependencies.\n\nThis module provides dependency functions for FastAPI to handle authentication\nand authorization in request handlers.\n'
import time
from typing import Optional, Union
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.core.dependency_manager import get_service
from app.core.error import handle_exception
from app.core.exceptions import AuthenticationException
from app.logging import get_logger, set_user_id
from app.core.security.service import get_security_service
from app.core.security.tokens import decode_token
logger = get_logger('app.core.security.dependencies')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{settings.API_V1_STR}/auth/login')
optional_oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{settings.API_V1_STR}/auth/login', auto_error=False)
async def get_token_from_header(token: str=Depends(oauth2_scheme), request: Request=None) -> str:
    start_time = time.monotonic()
    try:
        if request and hasattr(request.state, 'request_id'):
            try:
                metrics_service = get_service('metrics_service')
                metrics_service.increment_counter('token_dependencies_total', labels={'dependency': 'get_token_from_header'})
            except Exception:
                pass
        return token
    except Exception as e:
        logger.error(f'Error in token dependency: {str(e)}')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials', headers={'WWW-Authenticate': 'Bearer'})
    finally:
        if request:
            try:
                duration = time.monotonic() - start_time
                metrics_service = get_service('metrics_service')
                metrics_service.observe_histogram('token_dependency_duration_seconds', duration, {'dependency': 'get_token_from_header'})
            except Exception:
                pass
async def get_current_user_id(token: str=Depends(get_token_from_header), request: Request=None) -> str:
    start_time = time.monotonic()
    request_id = getattr(request.state, 'request_id', None) if request else None
    try:
        try:
            security_service = get_security_service()
            token_data = await security_service.validate_token(token, request_id)
            set_user_id(token_data.sub)
            return token_data.sub
        except Exception:
            token_data = await decode_token(token)
            set_user_id(token_data.sub)
            return token_data.sub
    except AuthenticationException:
        raise
    except Exception as e:
        logger.error(f'Error getting user ID from token: {str(e)}')
        handle_exception(e, request_id=request_id)
        raise AuthenticationException(message='Could not authenticate user') from e
    finally:
        if request:
            try:
                duration = time.monotonic() - start_time
                metrics_service = get_service('metrics_service')
                metrics_service.observe_histogram('token_dependency_duration_seconds', duration, {'dependency': 'get_current_user_id'})
            except Exception:
                pass
async def get_optional_user_id(token: Optional[str]=Depends(optional_oauth2_scheme), request: Request=None) -> Optional[str]:
    if not token:
        return None
    try:
        return await get_current_user_id(token, request)
    except (AuthenticationException, HTTPException):
        return None
async def get_current_user_with_permissions(token: str=Depends(get_token_from_header), request: Request=None, db=None) -> Union[dict, Any]:
    start_time = time.monotonic()
    request_id = getattr(request.state, 'request_id', None) if request else None
    try:
        security_service = get_security_service()
        token_data = await security_service.validate_token(token, request_id)
        set_user_id(token_data.sub)
        user_data = {'id': token_data.sub, 'role': token_data.role, 'permissions': token_data.permissions or []}
        if token_data.user_data:
            user_data.update(token_data.user_data)
        return user_data
    except AuthenticationException:
        raise
    except Exception as e:
        logger.error(f'Error getting user from token: {str(e)}')
        handle_exception(e, request_id=request_id)
        raise AuthenticationException(message='Could not authenticate user') from e
    finally:
        if request:
            try:
                duration = time.monotonic() - start_time
                metrics_service = get_service('metrics_service')
                metrics_service.observe_histogram('token_dependency_duration_seconds', duration, {'dependency': 'get_current_user_with_permissions'})
            except Exception:
                pass