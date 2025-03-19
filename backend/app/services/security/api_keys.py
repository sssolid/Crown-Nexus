# backend/app/services/security/api_keys.py
"""API key management for service authentication.

This module provides services for generating, validating, and managing
API keys used for service-to-service authentication and programmatic access.
"""
from __future__ import annotations

import hashlib
import hmac
import secrets
import uuid
import datetime
from typing import List, Optional

from app.core.logging import get_logger
from app.core.security import TokenType, create_token
from app.services.security.base import ApiKeyData

logger = get_logger(__name__)


class ApiKeyService:
    """Service for API key management."""

    def generate_api_key(
        self, user_id: str, name: str, permissions: Optional[List[str]] = None
    ) -> ApiKeyData:
        """
        Generate a new API key.

        Args:
            user_id: The user ID the key belongs to
            name: A name for the key
            permissions: Specific permissions for this key

        Returns:
            API key details
        """
        key_id = str(uuid.uuid4())
        secret = secrets.token_urlsafe(32)
        hashed_secret = hashlib.sha256(secret.encode()).hexdigest()

        api_key = f"{key_id}.{secret}"

        # Create a JWT token with API key information
        token = create_token(
            subject=user_id,
            token_type=TokenType.API_KEY,
            permissions=permissions,
            user_data={"name": name, "key_id": key_id},
        )

        return ApiKeyData(
            api_key=api_key,
            key_id=key_id,
            hashed_secret=hashed_secret,
            token=token,
            name=name,
            created_at=datetime.datetime.now(datetime.UTC).isoformat(),
            permissions=permissions or [],
        )

    def verify_api_key(self, api_key: str, stored_hash: str) -> bool:
        """
        Verify an API key against a stored hash.

        Args:
            api_key: The API key to verify
            stored_hash: The stored hash to compare against

        Returns:
            True if the key is valid, False otherwise
        """
        try:
            parts = api_key.split(".")
            if len(parts) != 2:
                return False

            _, secret = parts
            hashed_secret = hashlib.sha256(secret.encode()).hexdigest()

            # Use constant-time comparison to prevent timing attacks
            return hmac.compare_digest(hashed_secret, stored_hash)
        except Exception as e:
            logger.error(f"API key verification error: {str(e)}")
            return False

    def parse_api_key(self, api_key: str) -> Optional[str]:
        """
        Parse an API key to extract the key ID.

        Args:
            api_key: The full API key

        Returns:
            The key ID if valid, None otherwise
        """
        try:
            parts = api_key.split(".")
            if len(parts) != 2:
                return None

            key_id, _ = parts
            return key_id
        except Exception as e:
            logger.error(f"API key parsing error: {str(e)}")
            return None
