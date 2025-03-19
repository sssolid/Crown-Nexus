# backend/app/schemas/user.py
"""
User data schemas.

This module provides Pydantic schemas for user-related data validation
and serialization. The schemas support:
- Request validation for user creation and updates
- Response serialization for user data
- JWT token data validation
- Company-related data structures

These schemas ensure that data passed to and from API endpoints
is properly validated and transformed according to the application's
requirements.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserRole(str, Enum):
    """
    User role enumeration.

    Defines the possible roles a user can have in the system,
    determining their access privileges.
    """

    ADMIN = "admin"
    MANAGER = "manager"
    CLIENT = "client"
    DISTRIBUTOR = "distributor"
    READ_ONLY = "read_only"


class Token(BaseModel):
    """
    Token schema for authentication responses.

    This schema defines the structure of token responses sent
    to clients after successful authentication.

    Attributes:
        access_token: JWT access token
        token_type: Token type (usually "bearer")
    """

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """
    Token payload schema.

    This schema defines the structure of the JWT token payload
    for validation and extraction of token data.

    Attributes:
        sub: User ID (subject)
        exp: Expiration timestamp
        role: User role
        iat: Issued at timestamp (optional)
    """

    sub: str  # User ID
    exp: int  # Expiration timestamp
    role: UserRole  # User role
    iat: Optional[int] = None  # Issued at timestamp


class CompanyBase(BaseModel):
    """
    Base schema for Company data.

    Defines common fields used across company-related schemas.

    Attributes:
        name: Company name
        account_number: External account number (optional)
        account_type: Type of account
        is_active: Whether the account is active
    """

    name: str
    account_number: Optional[str] = None
    account_type: str
    is_active: bool = True


class CompanyCreate(CompanyBase):
    """
    Schema for creating a new Company.

    Extends the base company schema for creation requests.
    """

    pass


class CompanyUpdate(BaseModel):
    """
    Schema for updating an existing Company.

    Defines fields that can be updated on a company, with all
    fields being optional to allow partial updates.

    Attributes:
        name: Company name (optional)
        account_number: External account number (optional)
        account_type: Type of account (optional)
        is_active: Whether the account is active (optional)
    """

    name: Optional[str] = None
    account_number: Optional[str] = None
    account_type: Optional[str] = None
    is_active: Optional[bool] = None


class CompanyInDB(CompanyBase):
    """
    Schema for Company as stored in the database.

    Extends the base company schema with database-specific fields.

    Attributes:
        id: Company UUID
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Company(CompanyInDB):
    """
    Schema for Company responses.

    This schema is used for API responses returning company data.
    It extends the database schema with any additional computed fields.
    """

    pass


class UserBase(BaseModel):
    """
    Base schema for User data.

    Defines common fields used across user-related schemas.

    Attributes:
        email: User email address
        full_name: User's full name
        role: User role
        is_active: Whether the user account is active
        company_id: Reference to associated company (optional)
    """

    email: EmailStr
    full_name: str
    role: UserRole = UserRole.CLIENT
    is_active: bool = True
    company_id: Optional[uuid.UUID] = None


class UserCreate(UserBase):
    """
    Schema for creating a new User.

    Extends the base user schema with password field for user creation.

    Attributes:
        password: User password (min length: 8)
    """

    password: str = Field(..., min_length=8, description="User password")


class UserUpdate(BaseModel):
    """
    Schema for updating an existing User.

    Defines fields that can be updated on a user, with all
    fields being optional to allow partial updates.

    Attributes:
        email: User email address (optional)
        full_name: User's full name (optional)
        password: User password (optional, min length: 8)
        role: User role (optional)
        is_active: Whether the user account is active (optional)
        company_id: Reference to associated company (optional, can be set to None)
    """

    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8, description="User password")
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    company_id: Optional[Union[uuid.UUID, None]] = Field(
        default=..., description="Company ID, can be null to remove company association"
    )

    @field_validator("password", mode="before")
    @classmethod
    def password_strength(cls, v: Optional[str]) -> Optional[str]:
        """
        Validate password strength.

        Args:
            v: Password value

        Returns:
            Optional[str]: Validated password

        Raises:
            ValueError: If password doesn't meet strength requirements
        """
        if v is None:
            return v

        # Check password strength (example only, adjust as needed)
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")

        # Additional checks could be added here (e.g., requiring numbers, special chars)

        return v


class UserInDB(UserBase):
    """
    Schema for User as stored in the database.

    Extends the base user schema with database-specific fields.

    Attributes:
        id: User UUID
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class User(UserInDB):
    """
    Schema for User responses.

    This schema is used for API responses returning user data.
    It extends the database schema with the associated company.

    Attributes:
        company: Associated company information (optional)
    """

    company: Optional[Company] = None


# Update forward references for nested models
User.model_rebuild()
