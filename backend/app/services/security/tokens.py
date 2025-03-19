# backend/app/services/security/tokens.py
"""Token generation, validation, and management.

This module provides services for handling authentication tokens,
including JWT tokens, refresh tokens, and special-purpose tokens.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List, Optional, Union

from app.core.config import settings
from app.core.exceptions import AuthenticationException, ErrorCode
from app.core.logging import get_logger
from app.core.security import (
    TokenClaimsModel,
    TokenType,
    create_token,
    create_token_pair,
    decode_token,
)
from app.services.security.base import TokenConfig
from app.utils.redis_manager import get_key, set_key, delete_key

logger = get_logger(__name__)


class TokenService:
    """Service for token management and validation."""

    def __init__(self) -> None:
        """Initialize the token service."""
        self.config = TokenConfig(
            secret_key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
            access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )

        # Used for token blacklisting
        self.token_blacklist_prefix = "token:blacklist:"

    async def create_access_token(
        self,
        subject: Union[str, int],
        expires_delta: Optional[datetime.timedelta] = None,
        role: Optional[str] = None,
        permissions: Optional[List[str]] = None,
        user_data: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Create an access token.

        Args:
            subject: The subject identifier (usually user ID)
            expires_delta: Optional custom expiration time
            role: Optional user role
            permissions: Optional list of permissions
            user_data: Optional additional user data

        Returns:
            JWT access token
        """
        if expires_delta is None:
            expires_delta = datetime.timedelta(
                minutes=self.config.access_token_expire_minutes
            )

        return create_token(
            subject=str(subject),
            token_type=TokenType.ACCESS.value,
            expires_delta=expires_delta,
            role=role or "",
            permissions=permissions,
            user_data=user_data,
        )

    async def create_refresh_token(
        self,
        subject: Union[str, int],
        expires_delta: Optional[datetime.timedelta] = None,
    ) -> str:
        """
        Create a refresh token.

        Args:
            subject: The subject identifier (usually user ID)
            expires_delta: Optional custom expiration time

        Returns:
            JWT refresh token
        """
        if expires_delta is None:
            expires_delta = datetime.timedelta(
                days=self.config.refresh_token_expire_days
            )

        return create_token(
            subject=str(subject),
            token_type=TokenType.REFRESH.value,
            expires_delta=expires_delta,
        )

    async def create_token_pair(
        self,
        subject: Union[str, int],
        role: Optional[str] = None,
        permissions: Optional[List[str]] = None,
        user_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, str]:
        """
        Create a pair of access and refresh tokens.

        Args:
            subject: The subject identifier (usually user ID)
            role: Optional user role
            permissions: Optional list of permissions
            user_data: Optional additional user data

        Returns:
            Dictionary with access_token and refresh_token
        """
        return {
            "access_token": await self.create_access_token(
                subject, role=role, permissions=permissions, user_data=user_data
            ),
            "refresh_token": await self.create_refresh_token(subject),
        }

    async def create_verification_token(
        self,
        subject: Union[str, int],
        purpose: str,
        expires_delta: Optional[datetime.timedelta] = None,
        user_data: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Create a verification token (for email verification, etc).

        Args:
            subject: The subject identifier (usually user ID)
            purpose: The purpose of the verification
            expires_delta: Optional custom expiration time
            user_data: Optional additional user data

        Returns:
            JWT verification token
        """
        if expires_delta is None:
            expires_delta = datetime.timedelta(
                days=self.config.verification_token_expire_days
            )

        data = user_data or {}
        data["purpose"] = purpose

        return create_token(
            subject=str(subject),
            token_type=TokenType.VERIFICATION.value,
            expires_delta=expires_delta,
            user_data=data,
        )

    async def validate_token(
        self,
        token: str,
        expected_type: Optional[TokenType] = None,
        verify_exp: bool = True,
        check_blacklist: bool = True,
    ) -> TokenClaimsModel:
        """
        Validate a token.

        Args:
            token: The token to validate
            expected_type: The expected token type
            verify_exp: Whether to verify expiration
            check_blacklist: Whether to check the token blacklist

        Returns:
            The decoded token claims

        Raises:
            AuthenticationException: If validation fails
        """
        try:
            # Check if token is blacklisted
            if check_blacklist and await self.is_token_blacklisted(token):
                logger.warning("Attempted use of blacklisted token")
                raise AuthenticationException(
                    message="Token has been revoked",
                    details={"reason": "blacklisted"},
                )

            # Decode and validate the token
            token_data = await decode_token(token)

            # Apply additional token validations
            if expected_type and token_data.type != expected_type.value:
                logger.warning(
                    f"Token type mismatch: expected {expected_type}, got {token_data.type}",
                    subject=token_data.sub,
                )
                raise AuthenticationException(
                    message="Invalid token type",
                    details={
                        "expected_type": expected_type.value,
                        "actual_type": token_data.type,
                    },
                )

            return token_data

        except AuthenticationException:
            # Let core authentication exceptions pass through
            raise
        except Exception as e:
            logger.error(f"Token validation error: {str(e)}")
            raise AuthenticationException(
                message="Token validation failed",
                details={"error": str(e)},
            )

    async def refresh_access_token(self, refresh_token: str) -> str:
        """
        Generate a new access token using a refresh token.

        Args:
            refresh_token: The refresh token

        Returns:
            New access token

        Raises:
            AuthenticationException: If refresh token is invalid
        """
        # Validate the refresh token
        token_data = await self.validate_token(
            refresh_token, expected_type=TokenType.REFRESH
        )

        # Create a new access token
        return await self.create_access_token(
            subject=token_data.sub,
            role=getattr(token_data, "role", None),
            permissions=getattr(token_data, "permissions", None),
            user_data=getattr(token_data, "user_data", None),
        )

    async def blacklist_token(self, token: str, reason: str = "revoked") -> None:
        """
        Add a token to the blacklist.

        Args:
            token: The token to blacklist
            reason: Reason for blacklisting
        """
        try:
            # Get token claims without validation
            token_data = await decode_token(token)

            # Calculate seconds until expiration
            exp_time = datetime.datetime.fromtimestamp(token_data.exp)
            now = datetime.datetime.now(datetime.UTC)

            # If token is already expired, no need to blacklist
            if exp_time <= now:
                return

            # Calculate TTL in seconds
            ttl = int((exp_time - now).total_seconds())

            # Add to blacklist with expiration matching token
            blacklist_key = f"{self.token_blacklist_prefix}{token}"
            await set_key(blacklist_key, reason, ttl)

            logger.info(
                f"Token blacklisted",
                subject=token_data.sub,
                token_type=token_data.type,
                reason=reason,
            )
        except Exception as e:
            logger.error(f"Error blacklisting token: {str(e)}")

    async def is_token_blacklisted(self, token: str) -> bool:
        """
        Check if a token is blacklisted.

        Args:
            token: The token to check

        Returns:
            True if token is blacklisted, False otherwise
        """
        try:
            blacklist_key = f"{self.token_blacklist_prefix}{token}"
            result = await get_key(blacklist_key)
            return result is not None
        except Exception as e:
            logger.error(f"Error checking token blacklist: {str(e)}")
            return False
