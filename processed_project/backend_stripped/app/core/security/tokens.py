from __future__ import annotations
'JSON Web Token (JWT) handling functionality.\n\nThis module provides functions for creating, validating, and managing JWT tokens,\nincluding access tokens, refresh tokens, and token blacklisting.\n'
import datetime
import time
import uuid
from typing import Any, Dict, List, Optional, Union
from jose import JWTError, jwt
from pydantic import ValidationError
from app.core.config import settings
from app.core.dependency_manager import get_service
from app.core.error import handle_exception
from app.core.exceptions import AuthenticationException
from app.logging import get_logger
from app.core.security.models import TokenClaimsModel, TokenPair, TokenType
from app.utils.redis_manager import get_key, set_key
logger = get_logger('app.core.security.tokens')
def generate_token_jti() -> str:
    return str(uuid.uuid4())
def create_token(subject: Union[str, int], token_type: str, expires_delta: Optional[datetime.timedelta]=None, role: str='', permissions: Optional[List[str]]=None, user_data: Optional[Dict[str, Any]]=None) -> str:
    if expires_delta is None:
        if token_type == TokenType.ACCESS:
            expires_delta = datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        elif token_type == TokenType.REFRESH:
            expires_delta = datetime.timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        elif token_type == TokenType.RESET_PASSWORD:
            expires_delta = datetime.timedelta(hours=24)
        elif token_type == TokenType.EMAIL_VERIFICATION:
            expires_delta = datetime.timedelta(days=7)
        else:
            expires_delta = datetime.timedelta(minutes=30)
    expire = datetime.datetime.now(datetime.UTC) + expires_delta
    token_jti = generate_token_jti()
    to_encode: Dict[str, Any] = {'sub': str(subject), 'exp': expire, 'iat': datetime.datetime.now(datetime.UTC), 'type': token_type, 'jti': token_jti}
    if role:
        to_encode['role'] = role
    if permissions:
        to_encode['permissions'] = permissions
    if user_data:
        to_encode['user_data'] = user_data
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
def create_token_pair(user_id: Union[str, int], role: str, permissions: Optional[List[str]]=None, user_data: Optional[Dict[str, Any]]=None) -> TokenPair:
    start_time = time.monotonic()
    try:
        access_token = create_token(subject=user_id, token_type=TokenType.ACCESS, role=role, permissions=permissions, user_data=user_data)
        refresh_token = create_token(subject=user_id, token_type=TokenType.REFRESH, role=role, permissions=permissions, user_data=user_data)
        return TokenPair(access_token=access_token, refresh_token=refresh_token, expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    except Exception as e:
        logger.error(f'Error creating token pair: {str(e)}', exc_info=True)
        handle_exception(e, user_id=str(user_id))
        raise
    finally:
        try:
            duration = time.monotonic() - start_time
            metrics_service = get_service('metrics_service')
            metrics_service.observe_histogram('token_pair_creation_duration_seconds', duration)
        except Exception:
            pass
async def add_token_to_blacklist(token_jti: str, expires_at: datetime.datetime) -> None:
    now = datetime.datetime.now(datetime.UTC)
    ttl = int((expires_at - now).total_seconds())
    if ttl > 0:
        blacklist_key = f'token:blacklist:{token_jti}'
        await set_key(blacklist_key, '1', ttl)
        logger.debug(f'Token {token_jti} blacklisted for {ttl} seconds')
        try:
            metrics_service = get_service('metrics_service')
            metrics_service.increment_counter('tokens_blacklisted_total')
        except Exception:
            pass
async def is_token_blacklisted(token_jti: str) -> bool:
    try:
        cache_service = get_service('cache_service')
        cache_key = f'token:blacklist:{token_jti}'
        cached_result = await cache_service.get(cache_key)
        if cached_result is not None:
            return cached_result == '1'
    except Exception:
        pass
    blacklist_key = f'token:blacklist:{token_jti}'
    value = await get_key(blacklist_key)
    is_blacklisted = value is not None
    try:
        cache_service = get_service('cache_service')
        await cache_service.set(cache_key, '1' if is_blacklisted else '0', ttl=60)
    except Exception:
        pass
    return is_blacklisted
async def decode_token(token: str) -> TokenClaimsModel:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if 'exp' in payload:
            payload['exp'] = datetime.datetime.fromtimestamp(payload['exp'], tz=datetime.UTC)
        if 'iat' in payload:
            payload['iat'] = datetime.datetime.fromtimestamp(payload['iat'], tz=datetime.UTC)
        token_data = TokenClaimsModel(**payload)
        if await is_token_blacklisted(token_data.jti):
            logger.warning(f'Blacklisted token used: {token_data.jti}')
            raise AuthenticationException(message='Token has been revoked')
        return token_data
    except JWTError as e:
        logger.warning(f'JWT decode error: {str(e)}')
        raise AuthenticationException(message='Could not validate credentials') from e
    except ValidationError as e:
        logger.warning(f'Token payload validation error: {str(e)}')
        raise AuthenticationException(message='Token has invalid format') from e
async def revoke_token(token: str) -> None:
    try:
        token_data = await decode_token(token)
        await add_token_to_blacklist(token_data.jti, token_data.exp)
        try:
            event_service = get_service('event_service')
            await event_service.publish(event_name='security.token_revoked', payload={'token_jti': token_data.jti, 'user_id': token_data.sub, 'reason': 'explicit_revocation'})
        except Exception:
            pass
    except AuthenticationException:
        raise
    except Exception as e:
        logger.error(f'Error revoking token: {str(e)}')
        handle_exception(e)
        raise AuthenticationException(message='Token revocation failed') from e
async def refresh_tokens(refresh_token: str) -> TokenPair:
    start_time = time.monotonic()
    try:
        token_data = await decode_token(refresh_token)
        if token_data.type != TokenType.REFRESH:
            raise AuthenticationException(message='Invalid token type')
        await add_token_to_blacklist(token_data.jti, token_data.exp)
        return create_token_pair(user_id=token_data.sub, role=token_data.role or '', permissions=token_data.permissions, user_data=token_data.user_data)
    except AuthenticationException:
        raise
    except Exception as e:
        logger.error(f'Error refreshing tokens: {str(e)}')
        handle_exception(e)
        raise AuthenticationException(message='Token refresh failed') from e
    finally:
        try:
            duration = time.monotonic() - start_time
            metrics_service = get_service('metrics_service')
            metrics_service.observe_histogram('token_refresh_duration_seconds', duration)
        except Exception:
            pass
class TokenManager:
    def __init__(self) -> None:
        self.token_blacklist_prefix = 'token:blacklist:'
    def create_token(self, subject: Union[str, int], token_type: str, expires_delta: Optional[datetime.timedelta]=None, role: str='', permissions: Optional[List[str]]=None, user_data: Optional[Dict[str, Any]]=None) -> str:
        return create_token(subject=subject, token_type=token_type, expires_delta=expires_delta, role=role, permissions=permissions, user_data=user_data)
    def create_token_pair(self, user_id: Union[str, int], role: str, permissions: Optional[List[str]]=None, user_data: Optional[Dict[str, Any]]=None) -> TokenPair:
        return create_token_pair(user_id=user_id, role=role, permissions=permissions, user_data=user_data)
    async def decode_token(self, token: str) -> TokenClaimsModel:
        return await decode_token(token)
    async def revoke_token(self, token: str) -> None:
        await revoke_token(token)
    async def refresh_tokens(self, refresh_token: str) -> TokenPair:
        return await refresh_tokens(refresh_token)
    async def add_to_blacklist(self, token_jti: str, expires_at: datetime.datetime) -> None:
        await add_token_to_blacklist(token_jti, expires_at)
    async def is_blacklisted(self, token_jti: str) -> bool:
        return await is_token_blacklisted(token_jti)