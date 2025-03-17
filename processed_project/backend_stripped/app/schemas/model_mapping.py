from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
class ModelMappingBase(BaseModel):
    pattern: str = Field(..., description='Pattern to match in vehicle text')
    mapping: str = Field(..., description="Mapping in format 'Make|VehicleCode|Model'")
    priority: int = Field(0, description='Priority for mapping (higher values are processed first)')
    active: bool = Field(True, description='Whether this mapping is active')
    @field_validator('mapping')
    def validate_mapping_format(cls, v: str) -> str:
        parts = v.split('|')
        if len(parts) != 3:
            raise ValueError("Mapping must be in format 'Make|VehicleCode|Model' with exactly 2 pipe separators")
        if not any(parts):
            raise ValueError('At least one of Make, VehicleCode, or Model must not be empty')
        return v
class ModelMappingCreate(ModelMappingBase):
    pass
class ModelMappingUpdate(BaseModel):
    pattern: Optional[str] = None
    mapping: Optional[str] = None
    priority: Optional[int] = None
    active: Optional[bool] = None
    @field_validator('mapping')
    def validate_mapping_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        parts = v.split('|')
        if len(parts) != 3:
            raise ValueError("Mapping must be in format 'Make|VehicleCode|Model' with exactly 2 pipe separators")
        if not any(parts):
            raise ValueError('At least one of Make, VehicleCode, or Model must not be empty')
        return v
class ModelMapping(ModelMappingBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
class ModelMappingList(BaseModel):
    items: List[ModelMapping]
    total: int