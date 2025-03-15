from __future__ import annotations
import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel, ConfigDict, EmailStr, Field, validator
class UserRole(str, Enum):
    ADMIN = 'admin'
    MANAGER = 'manager'
    CLIENT = 'client'
    DISTRIBUTOR = 'distributor'
    READ_ONLY = 'read_only'
class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
class TokenPayload(BaseModel):
    sub: str
    exp: int
    role: UserRole
    iat: Optional[int] = None
class CompanyBase(BaseModel):
    name: str
    account_number: Optional[str] = None
    account_type: str
    is_active: bool = True
class CompanyCreate(CompanyBase):
    pass
class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    account_number: Optional[str] = None
    account_type: Optional[str] = None
    is_active: Optional[bool] = None
class CompanyInDB(CompanyBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
class Company(CompanyInDB):
    pass
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.CLIENT
    is_active: bool = True
    company_id: Optional[uuid.UUID] = None
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description='User password')
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8, description='User password')
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    company_id: Optional[Union[uuid.UUID, None]] = Field(default=..., description='Company ID, can be null to remove company association')
    @validator('password')
    def password_strength(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
class UserInDB(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
class User(UserInDB):
    company: Optional[Company] = None
User.model_rebuild()