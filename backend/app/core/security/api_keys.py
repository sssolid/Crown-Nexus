from __future__ import annotations

"""API key generation and validation functionality.

This module provides functions for generating, validating, and managing API keys
used for machine-to-machine authentication.
"""

import hashlib
import hmac
import secrets
import uuid
import datetime
from typing import List, Optional

from app.logging import get_logger
from app.core.security.models import ApiKeyData, TokenType
from app.core.security.tokens import create_token

logger = get_logger("app.core.security.api_keys")


def generate_api_key(
    user_id: str, name: str, permissions: Optional[List[str]] = None
) -> ApiKeyData:
    """Generate a new API key.

    Args:
        user_id: The user ID.
        name: The name of the API key.
        permissions: Optional list of permissions.

    Returns:
        ApiKeyData: The generated API key data.
    """
    key_id = str(uuid.uuid4())
    secret = secrets.token_urlsafe(32)
    hashed_secret = hashlib.sha256(secret.encode()).hexdigest()
    api_key = f"{key_id}.{secret}"

    token = create_token(
        subject=user_id,
        token_type=TokenType.API_KEY.value,
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


def verify_api_key(api_key: str, stored_hash: str) -> bool:
    """Verify an API key against its stored hash.

    Args:
        api_key: The API key to verify.
        stored_hash: The stored hash to verify against.

    Returns:
        bool: True if the API key is valid, False otherwise.
    """
    try:
        parts = api_key.split(".")
        if len(parts) != 2:
            return False

        _, secret = parts
        hashed_secret = hashlib.sha256(secret.encode()).hexdigest()

        return hmac.compare_digest(hashed_secret, stored_hash)

    except Exception as e:
        logger.error(f"API key verification error: {str(e)}")
        return False


class ApiKeyManager:
    """Manager for API key-related functionality."""

    def generate_api_key(
        self, user_id: str, name: str, permissions: Optional[List[str]] = None
    ) -> ApiKeyData:
        """Generate a new API key.

        Args:
            user_id: The user ID.
            name: The name of the API key.
            permissions: Optional list of permissions.

        Returns:
            ApiKeyData: The generated API key data.
        """
        return generate_api_key(user_id, name, permissions)

    def verify_api_key(self, api_key: str, stored_hash: str) -> bool:
        """Verify an API key against its stored hash.

        Args:
            api_key: The API key to verify.
            stored_hash: The stored hash to verify against.

        Returns:
            bool: True if the API key is valid, False otherwise.
        """
        return verify_api_key(api_key, stored_hash)

    def parse_api_key(self, api_key: str) -> Optional[str]:
        """Parse an API key to extract its ID.

        Args:
            api_key: The API key to parse.

        Returns:
            Optional[str]: The API key ID, or None if parsing fails.
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
