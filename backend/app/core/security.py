# app/core/security.py
from __future__ import annotations

import secrets
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union

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

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 configuration
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)


class TokenType(str):
    """Token type constants."""
    
    ACCESS = "access"
    REFRESH = "refresh"


class TokenData(BaseModel):
    """Token payload data."""
    
    sub: str = Field(..., description="Subject (user ID)")
    exp: datetime = Field(..., description="Expiration time")
    iat: datetime = Field(..., description="Issued at time")
    type: str = Field(..., description="Token type")
    role: str = Field(..., description="User role")
    jti: str = Field(..., description="JWT ID (unique identifier)")
    user_data: Optional[Dict[str, Any]] = Field(None, description="Additional user data")


class TokenPair(BaseModel):
    """Access and refresh token pair."""
    
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Access token lifetime in seconds")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password
        
    Returns:
        bool: True if password matches
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt.
    
    Args:
        password: Plain text password
        
    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def generate_token_jti() -> str:
    """Generate a unique JWT ID for token tracking.
    
    Returns:
        str: Unique token identifier
    """
    return str(uuid.uuid4())


def create_token(
    subject: Union[str, int],
    token_type: str,
    expires_delta: Optional[timedelta] = None,
    role: str = "",
    user_data: Optional[Dict[str, Any]] = None,
) -> str:
    """Create a JWT token.
    
    Args:
        subject: Subject (user ID)
        token_type: Token type (access or refresh)
        expires_delta: Token expiration time
        role: User role
        user_data: Additional user data to include in token
        
    Returns:
        str: JWT token
    """
    if expires_delta is None:
        if token_type == TokenType.ACCESS:
            expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        else:
            expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
            
    expire = datetime.utcnow() + expires_delta
    token_jti = generate_token_jti()
    
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": token_type,
        "role": role,
        "jti": token_jti,
    }
    
    # Add optional user data
    if user_data:
        to_encode["user_data"] = user_data
        
    return jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )


def create_token_pair(
    user_id: Union[str, int],
    role: str,
    user_data: Optional[Dict[str, Any]] = None,
) -> TokenPair:
    """Create an access and refresh token pair.
    
    Args:
        user_id: User ID
        role: User role
        user_data: Additional user data to include in tokens
        
    Returns:
        TokenPair: Access and refresh token pair
    """
    access_token = create_token(
        subject=user_id,
        token_type=TokenType.ACCESS,
        role=role,
        user_data=user_data,
    )
    
    refresh_token = create_token(
        subject=user_id,
        token_type=TokenType.REFRESH,
        role=role,
        user_data=user_data,
    )
    
    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


async def add_token_to_blacklist(token_jti: str, expires_at: datetime) -> None:
    """Add a token to the blacklist in Redis.
    
    Args:
        token_jti: JWT ID to blacklist
        expires_at: When the token expires
    """
    # Calculate TTL in seconds
    now = datetime.utcnow()
    ttl = int((expires_at - now).total_seconds())
    
    if ttl > 0:
        # Store in Redis with TTL
        blacklist_key = f"token:blacklist:{token_jti}"
        await set_key(blacklist_key, "1", ttl)
        
        logger.debug(f"Token {token_jti} blacklisted for {ttl} seconds")


async def is_token_blacklisted(token_jti: str) -> bool:
    """Check if a token is blacklisted.
    
    Args:
        token_jti: JWT ID to check
        
    Returns:
        bool: True if token is blacklisted
    """
    blacklist_key = f"token:blacklist:{token_jti}"
    value = await get_key(blacklist_key, None)
    return value is not None


async def decode_token(token: str) -> TokenData:
    """Decode and validate a JWT token.
    
    Args:
        token: JWT token
        
    Returns:
        TokenData: Decoded token data
        
    Raises:
        AuthenticationException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        
        token_data = TokenData(**payload)
        
        # Check if token is blacklisted
        if await is_token_blacklisted(token_data.jti):
            raise AuthenticationException(
                message="Token has been revoked", 
                code=ErrorCode.INVALID_TOKEN
            )
            
        return token_data
    except JWTError as e:
        logger.warning(f"JWT decode error: {str(e)}")
        raise AuthenticationException(
            message="Could not validate credentials", 
            code=ErrorCode.INVALID_TOKEN
        ) from e
    except ValidationError as e:
        logger.warning(f"Token payload validation error: {str(e)}")
        raise AuthenticationException(
            message="Token has invalid format", 
            code=ErrorCode.INVALID_TOKEN
        ) from e


async def revoke_token(token: str) -> None:
    """Revoke a token by adding it to the blacklist.
    
    Args:
        token: JWT token to revoke
        
    Raises:
        AuthenticationException: If token is invalid
    """
    try:
        token_data = await decode_token(token)
        await add_token_to_blacklist(token_data.jti, token_data.exp)
    except AuthenticationException as e:
        # If token is already invalid, no need to blacklist
        logger.warning(f"Attempted to revoke invalid token: {str(e)}")
        raise


async def refresh_tokens(refresh_token: str) -> TokenPair:
    """Generate new token pair using a refresh token.
    
    Args:
        refresh_token: JWT refresh token
        
    Returns:
        TokenPair: New access and refresh token pair
        
    Raises:
        AuthenticationException: If refresh token is invalid
    """
    try:
        token_data = await decode_token(refresh_token)
        
        # Verify it's a refresh token
        if token_data.type != TokenType.REFRESH:
            raise AuthenticationException(
                message="Invalid token type", 
                code=ErrorCode.INVALID_TOKEN
            )
            
        # Revoke the used refresh token
        await add_token_to_blacklist(token_data.jti, token_data.exp)
        
        # Create new token pair
        return create_token_pair(
            user_id=token_data.sub,
            role=token_data.role,
            user_data=token_data.user_data,
        )
    except AuthenticationException:
        # Re-raise authentication exceptions
        raise
    except Exception as e:
        logger.error(f"Error refreshing tokens: {str(e)}")
        raise AuthenticationException(
            message="Token refresh failed", 
            code=ErrorCode.INVALID_TOKEN
        ) from e


def generate_random_token(length: int = 32) -> str:
    """Generate a secure random token.
    
    Args:
        length: Length of the token in bytes
        
    Returns:
        str: Secure random token
    """
    return secrets.token_urlsafe(length)
