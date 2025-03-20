from __future__ import annotations

"""API Key schema definitions.

This module defines Pydantic schemas for API Key objects,
including creation, update, and response models.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ApiKeyBase(BaseModel):
    """Base schema for API key data.

    Attributes:
        name: Human-readable name for the key.
        permissions: List of permissions granted to the key.
        extra_metadata: Additional metadata about the key.
        expires_at: When the key expires.
    """

    name: str = Field(..., min_length=1, max_length=100, description="API key name")
    permissions: Optional[List[str]] = Field(None, description="Granted permissions")
    extra_metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    expires_at: Optional[datetime] = Field(None, description="Expiration date")

    @field_validator("name")
    @classmethod
    def normalize_name(cls, v: str) -> str:
        """Normalize the API key name.

        Args:
            v: The name to normalize.

        Returns:
            Normalized name.
        """
        return v.strip()


class ApiKeyCreate(ApiKeyBase):
    """Schema for creating a new API key.

    Attributes:
        user_id: ID of the user who will own the key.
    """

    user_id: uuid.UUID = Field(..., description="User who owns the key")


class ApiKeyUpdate(BaseModel):
    """Schema for updating an existing API key.

    All fields are optional to allow partial updates.
    """

    name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="API key name"
    )
    is_active: Optional[bool] = Field(None, description="Whether the key is active")
    permissions: Optional[List[str]] = Field(None, description="Granted permissions")
    extra_metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    expires_at: Optional[datetime] = Field(None, description="Expiration date")

    @field_validator("name")
    @classmethod
    def normalize_name(cls, v: Optional[str]) -> Optional[str]:
        """Normalize the API key name if provided.

        Args:
            v: The name to normalize or None.

        Returns:
            Normalized name or None.
        """
        return v.strip() if v else v


class ApiKeyInDB(ApiKeyBase):
    """Schema for API key data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    user_id: uuid.UUID = Field(..., description="User who owns the key")
    key_id: str = Field(..., description="Public identifier for the API key")
    is_active: bool = Field(..., description="Whether the key is active")
    last_used_at: Optional[datetime] = Field(
        None, description="When the key was last used"
    )
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class ApiKey(ApiKeyInDB):
    """Schema for API key data in API responses."""

    pass


class ApiKeyWithSecret(ApiKey):
    """Schema for API key including the secret.

    This schema is only used when initially creating an API key.
    """

    secret: str = Field(..., description="Secret part of the API key")


class ApiKeyRevokeResponse(BaseModel):
    """Schema for API key revocation response.

    Attributes:
        id: ID of the revoked key.
        revoked: Whether the key was successfully revoked.
        message: Response message.
    """

    id: uuid.UUID = Field(..., description="ID of the revoked key")
    revoked: bool = Field(..., description="Whether the key was successfully revoked")
    message: str = Field(..., description="Response message")
