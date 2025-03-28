from __future__ import annotations
'User schema definitions.\n\nThis module defines Pydantic schemas for User objects,\nincluding creation, update, and response models, as well as\nauthentication-related schemas like tokens.\n'
import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from app.domains.company.schemas import Company
class UserRole(str, Enum):
    ADMIN = 'admin'
    MANAGER = 'manager'
    CLIENT = 'client'
    DISTRIBUTOR = 'distributor'
    READ_ONLY = 'read_only'
class Token(BaseModel):
    access_token: str = Field(..., description='JWT access token')
    token_type: str = Field('bearer', description='Token type')
class TokenPayload(BaseModel):
    sub: str = Field(..., description='Subject (user ID)')
    exp: int = Field(..., description='Expiration timestamp')
    role: UserRole = Field(..., description='User role')
    iat: Optional[int] = Field(None, description='Issued at timestamp')
class UserBase(BaseModel):
    email: EmailStr = Field(..., description='User email address')
    full_name: str = Field(..., description='User full name')
    role: UserRole = Field(UserRole.CLIENT, description='User role')
    is_active: bool = Field(True, description='Whether user is active')
    company_id: Optional[uuid.UUID] = Field(None, description='Associated company ID')
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description='User password (min 8 characters)')
    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description='User email address')
    full_name: Optional[str] = Field(None, description='User full name')
    password: Optional[str] = Field(None, min_length=8, description='User password (min 8 characters)')
    role: Optional[UserRole] = Field(None, description='User role')
    is_active: Optional[bool] = Field(None, description='Whether user is active')
    company_id: Optional[Union[uuid.UUID, None]] = Field(default=..., description='Company ID, can be null to remove company association')
    @field_validator('password')
    @classmethod
    def password_strength(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
class UserInDB(UserBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    created_at: datetime = Field(..., description='Creation timestamp')
    updated_at: datetime = Field(..., description='Last update timestamp')
    model_config = ConfigDict(from_attributes=True)
class User(UserInDB):
    company: Optional[Company] = Field(None, description='Associated company details')