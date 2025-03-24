from __future__ import annotations

"""API Key repository implementation.

This module provides data access and persistence operations for API Key entities.
"""

import uuid
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.api_key.models import ApiKey
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException


class ApiKeyRepository(BaseRepository[ApiKey, uuid.UUID]):
    """Repository for API Key entity operations.

    Provides methods for querying, creating, updating, and deleting
    API Key entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the API key repository.

        Args:
            db: The database session.
        """
        super().__init__(model=ApiKey, db=db)

    async def find_by_key_id(self, key_id: str) -> Optional[ApiKey]:
        """Find an API key by its key ID.

        Args:
            key_id: The key ID to search for.

        Returns:
            The API key if found, None otherwise.
        """
        query = select(ApiKey).where(
            ApiKey.key_id == key_id, ApiKey.is_deleted == False
        )

        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_by_user(
        self, user_id: uuid.UUID, active_only: bool = True
    ) -> List[ApiKey]:
        """Get API keys for a specific user.

        Args:
            user_id: The user ID to filter by.
            active_only: Whether to include only active keys.

        Returns:
            List of API keys for the user.
        """
        conditions = [ApiKey.user_id == user_id, ApiKey.is_deleted == False]

        if active_only:
            conditions.append(ApiKey.is_active == True)

        query = (
            select(ApiKey).where(and_(*conditions)).order_by(ApiKey.created_at.desc())
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create_api_key(
        self,
        user_id: uuid.UUID,
        name: str,
        permissions: Optional[List[str]] = None,
        extra_metadata: Optional[Dict[str, Any]] = None,
        expires_in_days: Optional[int] = None,
    ) -> Tuple[ApiKey, str]:
        """Create a new API key.

        Args:
            user_id: ID of the user who will own the key.
            name: Human-readable name for the key.
            permissions: Optional list of permissions to grant.
            extra_metadata: Optional additional metadata.
            expires_in_days: Optional number of days until expiration.

        Returns:
            Tuple containing (API key entity, secret).

        Raises:
            ResourceNotFoundException: If the user doesn't exist.
        """
        # Generate key_id and secret
        key_id = f"key_{secrets.token_hex(8)}"
        secret = secrets.token_hex(32)
        hashed_secret = self._hash_secret(secret)

        # Calculate expiration date if specified
        expires_at = None
        if expires_in_days:
            expires_at = datetime.now() + timedelta(days=expires_in_days)

        # Create the API key
        api_key = ApiKey(
            user_id=user_id,
            key_id=key_id,
            hashed_secret=hashed_secret,
            name=name,
            is_active=True,
            expires_at=expires_at,
            permissions=permissions,
            extra_metadata=extra_metadata,
        )

        self.db.add(api_key)
        await self.db.flush()
        await self.db.refresh(api_key)

        return api_key, secret

    async def verify_api_key(self, key_id: str, secret: str) -> Optional[ApiKey]:
        """Verify an API key by checking the key ID and secret.

        Args:
            key_id: The key ID to verify.
            secret: The secret to verify.

        Returns:
            The API key if valid, None otherwise.
        """
        # Find the API key
        api_key = await self.find_by_key_id(key_id)
        if not api_key or not api_key.is_active:
            return None

        # Check if the key has expired
        if api_key.expires_at and api_key.expires_at < datetime.now():
            return None

        # Verify the secret
        hashed_secret = self._hash_secret(secret)
        if not secrets.compare_digest(api_key.hashed_secret, hashed_secret):
            return None

        # Update last_used_at
        api_key.last_used_at = datetime.now()
        self.db.add(api_key)
        await self.db.flush()

        return api_key

    async def revoke_api_key(self, api_key_id: uuid.UUID) -> bool:
        """Revoke an API key.

        Args:
            api_key_id: The API key ID to revoke.

        Returns:
            True if the key was revoked, False otherwise.
        """
        api_key = await self.get_by_id(api_key_id)
        if not api_key:
            return False

        api_key.is_active = False
        self.db.add(api_key)
        await self.db.flush()

        return True

    async def revoke_all_user_keys(self, user_id: uuid.UUID) -> int:
        """Revoke all API keys for a user.

        Args:
            user_id: The user ID whose keys to revoke.

        Returns:
            Number of keys revoked.
        """
        # Get all active keys for the user
        active_keys = await self.get_by_user(user_id, active_only=True)

        # Revoke each key
        for key in active_keys:
            key.is_active = False
            self.db.add(key)

        await self.db.flush()

        return len(active_keys)

    async def clean_expired_keys(self) -> int:
        """Clean up expired API keys.

        Returns:
            Number of keys deactivated.
        """
        now = datetime.now()

        # Find expired but still active keys
        query = select(ApiKey).where(
            ApiKey.expires_at < now,
            ApiKey.is_active == True,
            ApiKey.is_deleted == False,
        )

        result = await self.db.execute(query)
        expired_keys = list(result.scalars().all())

        # Deactivate expired keys
        for key in expired_keys:
            key.is_active = False
            self.db.add(key)

        await self.db.flush()

        return len(expired_keys)

    async def ensure_exists(self, api_key_id: uuid.UUID) -> ApiKey:
        """Ensure an API key exists by ID, raising an exception if not found.

        Args:
            api_key_id: The API key ID to check.

        Returns:
            The API key if found.

        Raises:
            ResourceNotFoundException: If the API key is not found.
        """
        api_key = await self.get_by_id(api_key_id)
        if not api_key:
            raise ResourceNotFoundException(
                resource_type="ApiKey", resource_id=str(api_key_id)
            )
        return api_key

    def _hash_secret(self, secret: str) -> str:
        """Hash an API key secret.

        Args:
            secret: The secret to hash.

        Returns:
            The hashed secret.
        """
        # In a real application, consider using a more secure hashing algorithm
        # with a salt and multiple iterations.
        return hashlib.sha256(secret.encode()).hexdigest()
