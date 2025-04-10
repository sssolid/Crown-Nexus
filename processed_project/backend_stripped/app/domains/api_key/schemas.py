from __future__ import annotations
'API Key schema definitions.\n\nThis module defines Pydantic schemas for API Key objects,\nincluding creation, update, and response models.\n'
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
class ApiKeyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description='API key name')
    permissions: Optional[List[str]] = Field(None, description='Granted permissions')
    extra_metadata: Optional[Dict[str, Any]] = Field(None, description='Additional metadata')
    expires_at: Optional[datetime] = Field(None, description='Expiration date')
    @field_validator('name')
    @classmethod
    def normalize_name(cls, v: str) -> str:
        return v.strip()
class ApiKeyCreate(ApiKeyBase):
    user_id: uuid.UUID = Field(..., description='User who owns the key')
class ApiKeyUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description='API key name')
    is_active: Optional[bool] = Field(None, description='Whether the key is active')
    permissions: Optional[List[str]] = Field(None, description='Granted permissions')
    extra_metadata: Optional[Dict[str, Any]] = Field(None, description='Additional metadata')
    expires_at: Optional[datetime] = Field(None, description='Expiration date')
    @field_validator('name')
    @classmethod
    def normalize_name(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if v else v
class ApiKeyInDB(ApiKeyBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    user_id: uuid.UUID = Field(..., description='User who owns the key')
    key_id: str = Field(..., description='Public identifier for the API key')
    is_active: bool = Field(..., description='Whether the key is active')
    last_used_at: Optional[datetime] = Field(None, description='When the key was last used')
    created_at: datetime = Field(..., description='Creation timestamp')
    updated_at: datetime = Field(..., description='Last update timestamp')
    model_config = ConfigDict(from_attributes=True)
class ApiKey(ApiKeyInDB):
    pass
class ApiKeyWithSecret(ApiKey):
    secret: str = Field(..., description='Secret part of the API key')
class ApiKeyRevokeResponse(BaseModel):
    id: uuid.UUID = Field(..., description='ID of the revoked key')
    revoked: bool = Field(..., description='Whether the key was successfully revoked')
    message: str = Field(..., description='Response message')