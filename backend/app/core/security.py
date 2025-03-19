from __future__ import annotations

"""Security module providing core security primitives and token management.

This module provides fundamental security functionality including:
- Password hashing and verification
- JWT token generation and validation
- Token blacklisting
- CSRF token generation and validation

It serves as the foundation for higher-level security services in the application.
"""

import secrets
import uuid
import datetime
from typing import Any, Dict, List, Optional, Union, cast

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field, ValidationError

from app.core.config import settings
from app.core.exceptions import AuthenticationException, ErrorCode
from app.core.logging import get_logger
from app.utils.redis_manager import delete_key, get_key, set_key

logger = get_logger("app.core.security")

# Initialize password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Setup OAuth2 for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


class TokenType(str):
    """Types of tokens used in the application."""

    ACCESS = "access"
    REFRESH = "refresh"
    RESET_PASSWORD = "reset_password"
    EMAIL_VERIFICATION = "email_verification"
    INVITATION = "invitation"
    API_KEY = "api_key"
    CSRF = "csrf"
    SESSION = "session"


class TokenClaimsModel(BaseModel):
    """Model for JWT token claims."""

    sub: str = Field(..., description="Subject (user ID)")
    exp: datetime.datetime = Field(..., description="Expiration time")
    iat: datetime.datetime = Field(..., description="Issued at time")
    jti: str = Field(..., description="JWT ID (unique identifier)")
    type: str = Field(..., description="Token type")
    role: Optional[str] = Field(None, description="User role")
    permissions: Optional[List[str]] = Field(None, description="User permissions")
    user_data: Optional[Dict[str, Any]] = Field(
        None, description="Additional user data"
    )


class TokenPayload(Dict[str, Any]):
    """Type definition for token payload dictionary."""

    pass


class TokenPair(BaseModel):
    """Model for access and refresh token pair."""

    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Access token lifetime in seconds")


# Core functions for password handling
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash.

    Args:
        plain_password: The plain text password
        hashed_password: The hashed password to compare against

    Returns:
        True if the password matches the hash, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password.

    Args:
        password: The password to hash

    Returns:
        The hashed password
    """
    return pwd_context.hash(password)


def generate_token_jti() -> str:
    """Generate a unique JWT ID.

    Returns:
        A unique string identifier
    """
    return str(uuid.uuid4())


# Core token functions
def create_token(
    subject: Union[str, int],
    token_type: str,
    expires_delta: Optional[timedelta] = None,
    role: str = "",
    permissions: Optional[List[str]] = None,
    user_data: Optional[Dict[str, Any]] = None,
) -> str:
    """Create a JWT token.

    Args:
        subject: The subject identifier (usually user ID)
        token_type: The type of token
        expires_delta: How long the token should be valid
        role: The role of the user
        permissions: Specific permissions for the user
        user_data: Additional user data to include in the token

    Returns:
        The encoded JWT token
    """
    if expires_delta is None:
        if token_type == TokenType.ACCESS:
            expires_delta = datetime.timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        elif token_type == TokenType.REFRESH:
            expires_delta = datetime.timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        elif token_type == TokenType.RESET_PASSWORD:
            expires_delta = datetime.timedelta(
                hours=24
            )  # 24 hour expiry for password reset
        elif token_type == TokenType.EMAIL_VERIFICATION:
            expires_delta = datetime.timedelta(
                days=7
            )  # 7 day expiry for email verification
        else:
            expires_delta = datetime.timedelta(minutes=30)  # Default 30 minute expiry

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
        user_id: The user ID
        role: The user's role
        permissions: The user's permissions
        user_data: Additional user data to include in the tokens

    Returns:
        A TokenPair containing access and refresh tokens
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


async def add_token_to_blacklist(token_jti: str, expires_at: datetime) -> None:
    """Add a token to the blacklist.

    Args:
        token_jti: The JWT ID of the token
        expires_at: When the token expires
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
        token_jti: The JWT ID to check

    Returns:
        True if the token is blacklisted, False otherwise
    """
    blacklist_key = f"token:blacklist:{token_jti}"
    value = await get_key(blacklist_key, None)
    return value is not None


async def decode_token(token: str) -> TokenClaimsModel:
    """Decode and validate a JWT token.

    Args:
        token: The token to decode

    Returns:
        The decoded token claims

    Raises:
        AuthenticationException: If the token is invalid or blacklisted
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # Convert timestamps to datetime objects
        if "exp" in payload:
            payload["exp"] = datetime.fromtimestamp(payload["exp"])
        if "iat" in payload:
            payload["iat"] = datetime.fromtimestamp(payload["iat"])

        token_data = TokenClaimsModel(**payload)

        # Check if token is blacklisted
        if await is_token_blacklisted(token_data.jti):
            logger.warning(f"Blacklisted token used: {token_data.jti}")
            raise AuthenticationException(message="Token has been revoked")

        return token_data
    except JWTError as e:
        logger.warning(f"JWT decode error: {str(e)}")
        raise AuthenticationException(
            message="Could not validate credentials",
        ) from e
    except ValidationError as e:
        logger.warning(f"Token payload validation error: {str(e)}")
        raise AuthenticationException(message="Token has invalid format") from e


async def revoke_token(token: str) -> None:
    """Revoke a token by adding it to the blacklist.

    Args:
        token: The token to revoke

    Raises:
        AuthenticationException: If the token is invalid
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
        refresh_token: The refresh token

    Returns:
        A new token pair

    Raises:
        AuthenticationException: If the refresh token is invalid
    """
    try:
        token_data = await decode_token(refresh_token)

        # Verify this is a refresh token
        if token_data.type != TokenType.REFRESH:
            raise AuthenticationException(message="Invalid token type")

        # Blacklist the used refresh token
        await add_token_to_blacklist(token_data.jti, token_data.exp)

        # Create new token pair
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


def generate_random_token(length: int = 32) -> str:
    """Generate a cryptographically secure random token.

    Args:
        length: The desired token length in bytes

    Returns:
        A URL-safe base64-encoded random token
    """
    return secrets.token_urlsafe(length)


def generate_csrf_token(session_id: str) -> str:
    """Generate a CSRF token for a session.

    Args:
        session_id: The session ID to associate with the token

    Returns:
        A CSRF token
    """
    token = generate_random_token()
    timestamp = int(datetime.datetime.now(datetime.UTC).timestamp())
    payload = f"{session_id}:{timestamp}:{token}"
    signature = jwt.encode(
        {"data": payload}, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return f"{payload}:{signature}"


def verify_csrf_token(token: str, session_id: str, max_age: int = 3600) -> bool:
    """Verify a CSRF token.

    Args:
        token: The CSRF token to verify
        session_id: The expected session ID
        max_age: Maximum age of the token in seconds

    Returns:
        True if the token is valid, False otherwise
    """
    try:
        parts = token.rsplit(":", 1)
        if len(parts) != 2:
            return False

        payload, signature = parts
        payload_parts = payload.split(":")
        if len(payload_parts) != 3:
            return False

        token_session_id, timestamp_str, _ = payload_parts

        # Verify session ID matches
        if token_session_id != session_id:
            return False

        # Verify signature
        expected_signature = jwt.encode(
            {"data": payload}, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        if signature != expected_signature:
            return False

        # Verify token age
        timestamp = int(timestamp_str)
        now = int(datetime.datetime.now(datetime.UTC).timestamp())
        if now - timestamp > max_age:
            return False

        return True
    except (ValueError, JWTError):
        return False


# Dependency for getting the current token
async def get_token_from_header(token: str = Depends(oauth2_scheme)) -> str:
    """Extract the token from the Authorization header.

    Args:
        token: The bearer token from the Authorization header

    Returns:
        The token string
    """
    return token


async def get_current_user_id(token: str = Depends(get_token_from_header)) -> str:
    """Get the current user ID from a token.

    Args:
        token: The JWT token

    Returns:
        The user ID from the token

    Raises:
        AuthenticationException: If the token is invalid
    """
    try:
        token_data = await decode_token(token)
        return token_data.sub
    except AuthenticationException:
        raise
    except Exception as e:
        logger.error(f"Error getting user ID from token: {str(e)}")
        raise AuthenticationException(message="Could not authenticate user") from e
