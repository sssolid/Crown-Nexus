from __future__ import annotations

"""User schema definitions.

This module defines Pydantic schemas for User objects,
including creation, update, and response models, as well as
authentication-related schemas like tokens.
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.domains.company.schemas import Company


class UserRole(str, Enum):
    """Enumeration of user roles in the system.

    Attributes:
        ADMIN: Administrator role with full system access.
        MANAGER: Manager role with elevated permissions.
        CLIENT: Standard client user.
        DISTRIBUTOR: Distributor with specific permissions.
        READ_ONLY: User with read-only access.
    """

    ADMIN = "admin"
    MANAGER = "manager"
    CLIENT = "client"
    DISTRIBUTOR = "distributor"
    READ_ONLY = "read_only"


class Token(BaseModel):
    """Schema for authentication tokens.

    Attributes:
        access_token: The JWT access token.
        token_type: The token type (typically "bearer").
    """

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")


class TokenPayload(BaseModel):
    """Schema for JWT token payload.

    Attributes:
        sub: Subject (typically user ID).
        exp: Expiration timestamp.
        role: User role.
        iat: Issued at timestamp.
    """

    sub: str = Field(..., description="Subject (user ID)")
    exp: int = Field(..., description="Expiration timestamp")
    role: UserRole = Field(..., description="User role")
    iat: Optional[int] = Field(None, description="Issued at timestamp")


class UserBase(BaseModel):
    """Base schema for user data.

    Attributes:
        email: User's email address.
        full_name: User's full name.
        role: User's role in the system.
        is_active: Whether the user account is active.
        company_id: ID of the associated company.
    """

    email: EmailStr = Field(..., description="User email address")
    full_name: str = Field(..., description="User full name")
    role: UserRole = Field(UserRole.CLIENT, description="User role")
    is_active: bool = Field(True, description="Whether user is active")
    company_id: Optional[uuid.UUID] = Field(None, description="Associated company ID")


class UserCreate(UserBase):
    """Schema for creating a new user.

    Extends UserBase to include password.

    Attributes:
        password: User's plain-text password (will be hashed).
    """

    password: str = Field(
        ...,
        min_length=8,
        description="User password (min 8 characters)",
    )

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        """Validate password strength.

        Args:
            v: The password to validate.

        Returns:
            The password if valid.

        Raises:
            ValueError: If the password doesn't meet strength requirements.
        """
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")

        # Additional strength checks could be added here
        # For example: requiring numbers, special chars, etc.

        return v


class UserUpdate(BaseModel):
    """Schema for updating an existing user.

    All fields are optional to allow partial updates.
    """

    email: Optional[EmailStr] = Field(None, description="User email address")
    full_name: Optional[str] = Field(None, description="User full name")
    password: Optional[str] = Field(
        None, min_length=8, description="User password (min 8 characters)"
    )
    role: Optional[UserRole] = Field(None, description="User role")
    is_active: Optional[bool] = Field(None, description="Whether user is active")
    company_id: Optional[Union[uuid.UUID, None]] = Field(
        default=...,
        description="Company ID, can be null to remove company association",
    )

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: Optional[str]) -> Optional[str]:
        """Validate password strength if provided.

        Args:
            v: The password to validate or None.

        Returns:
            The password if valid or None if not provided.

        Raises:
            ValueError: If the password doesn't meet strength requirements.
        """
        if v is None:
            return v

        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")

        # Additional strength checks could be added here

        return v


class UserInDB(UserBase):
    """Schema for user data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class User(UserInDB):
    """Schema for complete user data in API responses.

    Includes related entities like company details.
    """

    company: Optional[Company] = Field(None, description="Associated company details")
