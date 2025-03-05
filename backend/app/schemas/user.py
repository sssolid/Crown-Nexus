from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRole(str, Enum):
    """User role enumeration."""
    ADMIN = "admin"
    MANAGER = "manager"
    CLIENT = "client"
    DISTRIBUTOR = "distributor"
    READ_ONLY = "read_only"


class Token(BaseModel):
    """Token schema."""
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Token payload schema."""
    sub: str  # User ID
    exp: int  # Expiration timestamp
    role: UserRole  # User role


class CompanyBase(BaseModel):
    """Base schema for Company data."""
    name: str
    account_number: Optional[str] = None
    account_type: str
    is_active: bool = True


class CompanyCreate(CompanyBase):
    """Schema for creating a new Company."""
    pass


class CompanyUpdate(BaseModel):
    """Schema for updating an existing Company."""
    name: Optional[str] = None
    account_number: Optional[str] = None
    account_type: Optional[str] = None
    is_active: Optional[bool] = None


class CompanyInDB(CompanyBase):
    """Schema for Company as stored in the database."""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Company(CompanyInDB):
    """Schema for Company responses."""
    pass


class UserBase(BaseModel):
    """Base schema for User data."""
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.CLIENT
    is_active: bool = True
    company_id: Optional[uuid.UUID] = None


class UserCreate(UserBase):
    """Schema for creating a new User."""
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Schema for updating an existing User."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    company_id: Optional[Union[uuid.UUID, None]] = Field(default=...)


class UserInDB(UserBase):
    """Schema for User as stored in the database."""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class User(UserInDB):
    """Schema for User responses."""
    company: Optional[Company] = None


# Update forward references for nested models
User.model_rebuild()
