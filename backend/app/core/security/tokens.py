from __future__ import annotations

"""JSON Web Token (JWT) handling functionality.

This module provides functions for creating, validating, and managing JWT tokens,
including access tokens, refresh tokens, and token blacklisting.
"""

import datetime
import uuid
from typing import Any, Dict, List, Optional, Union

from jose import JWTError, jwt
from pydantic import ValidationError

from app.core.config import settings
from app.core.exceptions import AuthenticationException
from app.logging import get_logger
from app.core.security.models import TokenClaimsModel, TokenPair, TokenType
from app.utils.redis_manager import get_key, set_key

logger = get_logger("app.core.security.tokens")


def generate_token_jti() -> str:
    """Generate a unique JWT ID.

    Returns:
        str: A unique identifier for a JWT token.
    """
    return str(uuid.uuid4())


def create_token(
    subject: Union[str, int],
    token_type: str,
    expires_delta: Optional[datetime.timedelta] = None,
    role: str = "",
    permissions: Optional[List[str]] = None,
    user_data: Optional[Dict[str, Any]] = None,
) -> str:
    """Create a JWT token.

    Args:
        subject: The subject of the token (usually the user ID).
        token_type: The type of token to create.
        expires_delta: Optional expiration time delta.
        role: Optional user role.
        permissions: Optional list of permissions.
        user_data: Optional additional user data.

    Returns:
        str: The encoded JWT token.
    """
    if expires_delta is None:
        if token_type == TokenType.ACCESS:
            expires_delta = datetime.timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
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

    to_encode: Dict[str, Any] = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.datetime.now(datetime.UTC),
        "type": token_type,
        "jti": token_jti,
    }

    if role:
        to_encode["role"] = role

    if permissions:
        to_encode["permissions"] = permissions

    if user_data:
        to_encode["user_data"] = user_data

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_token_pair(
    user_id: Union[str, int],
    role: str,
    permissions: Optional[List[str]] = None,
    user_data: Optional[Dict[str, Any]] = None,
) -> TokenPair:
    """Create an access and refresh token pair.

    Args:
        user_id: The user ID.
        role: The user role.
        permissions: Optional list of permissions.
        user_data: Optional additional user data.

    Returns:
        TokenPair: A model containing the access and refresh tokens.
    """
    access_token = create_token(
        subject=user_id,
        token_type=TokenType.ACCESS,
        role=role,
        permissions=permissions,
        user_data=user_data,
    )

    refresh_token = create_token(
        subject=user_id,
        token_type=TokenType.REFRESH,
        role=role,
        permissions=permissions,
        user_data=user_data,
    )

    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


async def add_token_to_blacklist(token_jti: str, expires_at: datetime.datetime) -> None:
    """Add a token to the blacklist.

    Args:
        token_jti: The JWT ID of the token.
        expires_at: The expiration time of the token.
    """
    now = datetime.datetime.now(datetime.UTC)
    ttl = int((expires_at - now).total_seconds())

    if ttl > 0:
        blacklist_key = f"token:blacklist:{token_jti}"
        await set_key(blacklist_key, "1", ttl)
        logger.debug(f"Token {token_jti} blacklisted for {ttl} seconds")


async def is_token_blacklisted(token_jti: str) -> bool:
    """Check if a token is blacklisted.

    Args:
        token_jti: The JWT ID of the token.

    Returns:
        bool: True if the token is blacklisted, False otherwise.
    """
    blacklist_key = f"token:blacklist:{token_jti}"
    value = await get_key(blacklist_key)
    return value is not None


async def decode_token(token: str) -> TokenClaimsModel:
    """Decode and validate a JWT token.

    Args:
        token: The token to decode.

    Returns:
        TokenClaimsModel: The decoded token claims.

    Raises:
        AuthenticationException: If the token is invalid.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        if "exp" in payload:
            payload["exp"] = datetime.datetime.fromtimestamp(
                payload["exp"], tz=datetime.UTC
            )

        if "iat" in payload:
            payload["iat"] = datetime.datetime.fromtimestamp(
                payload["iat"], tz=datetime.UTC
            )

        token_data = TokenClaimsModel(**payload)

        if await is_token_blacklisted(token_data.jti):
            logger.warning(f"Blacklisted token used: {token_data.jti}")
            raise AuthenticationException(message="Token has been revoked")

        return token_data

    except JWTError as e:
        logger.warning(f"JWT decode error: {str(e)}")
        raise AuthenticationException(message="Could not validate credentials") from e

    except ValidationError as e:
        logger.warning(f"Token payload validation error: {str(e)}")
        raise AuthenticationException(message="Token has invalid format") from e


async def revoke_token(token: str) -> None:
    """Revoke a token by adding it to the blacklist.

    Args:
        token: The token to revoke.

    Raises:
        AuthenticationException: If the token is invalid.
    """
    try:
        token_data = await decode_token(token)
        await add_token_to_blacklist(token_data.jti, token_data.exp)

    except AuthenticationException as e:
        logger.warning(f"Attempted to revoke invalid token: {str(e)}")
        raise


async def refresh_tokens(refresh_token: str) -> TokenPair:
    """Refresh an access token using a refresh token.

    Args:
        refresh_token: The refresh token.

    Returns:
        TokenPair: A new token pair.

    Raises:
        AuthenticationException: If the token is invalid.
    """
    try:
        token_data = await decode_token(refresh_token)

        if token_data.type != TokenType.REFRESH:
            raise AuthenticationException(message="Invalid token type")

        await add_token_to_blacklist(token_data.jti, token_data.exp)

        return create_token_pair(
            user_id=token_data.sub,
            role=token_data.role or "",
            permissions=token_data.permissions,
            user_data=token_data.user_data,
        )

    except AuthenticationException:
        raise

    except Exception as e:
        logger.error(f"Error refreshing tokens: {str(e)}")
        raise AuthenticationException(message="Token refresh failed") from e


class TokenManager:
    """Manager for token-related functionality."""

    def __init__(self) -> None:
        """Initialize the token manager."""
        self.token_blacklist_prefix = "token:blacklist:"

    # Implement class methods similar to the functions above
    # These would call the global functions to avoid duplication
