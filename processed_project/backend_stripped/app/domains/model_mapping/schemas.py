from __future__ import annotations
'Model mapping schema definitions.\n\nThis module defines Pydantic schemas for vehicle model mapping objects,\nwhich translate between different vehicle model naming systems.\n'
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
class ModelMappingBase(BaseModel):
    pattern: str = Field(..., description='Pattern to match in vehicle text')
    mapping: str = Field(..., description="Mapping in format 'Make|VehicleCode|Model'")
    priority: int = Field(0, description='Priority for mapping (higher values are processed first)')
    active: bool = Field(True, description='Whether this mapping is active')
    @field_validator('mapping')
    @classmethod
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
    pattern: Optional[str] = Field(None, description='Pattern to match in vehicle text')
    mapping: Optional[str] = Field(None, description="Mapping in format 'Make|VehicleCode|Model'")
    priority: Optional[int] = Field(None, description='Priority for mapping (higher values are processed first)')
    active: Optional[bool] = Field(None, description='Whether this mapping is active')
    @field_validator('mapping')
    @classmethod
    def validate_mapping_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        parts = v.split('|')
        if len(parts) != 3:
            raise ValueError("Mapping must be in format 'Make|VehicleCode|Model' with exactly 2 pipe separators")
        if not any(parts):
            raise ValueError('At least one of Make, VehicleCode, or Model must not be empty')
        return v
class ModelMappingInDB(ModelMappingBase):
    id: int = Field(..., description='Unique identifier')
    created_at: datetime = Field(..., description='Creation timestamp')
    updated_at: datetime = Field(..., description='Last update timestamp')
    model_config = ConfigDict(from_attributes=True)
class ModelMapping(ModelMappingInDB):
    @property
    def make(self) -> str:
        parts = self.mapping.split('|')
        return parts[0] if len(parts) > 0 else ''
    @property
    def vehicle_code(self) -> str:
        parts = self.mapping.split('|')
        return parts[1] if len(parts) > 1 else ''
    @property
    def model(self) -> str:
        parts = self.mapping.split('|')
        return parts[2] if len(parts) > 2 else ''
class ModelMappingPaginatedResponse(BaseModel):
    items: List[ModelMapping] = Field(..., description='List of model mappings')
    total: int = Field(..., description='Total number of items')
    page: int = Field(..., description='Current page number')
    page_size: int = Field(..., description='Number of items per page')
    pages: int = Field(..., description='Total number of pages')
class VehicleMatchRequest(BaseModel):
    vehicle_string: str = Field(..., description='Vehicle string to match')
class VehicleMatchResponse(BaseModel):
    matched: bool = Field(..., description='Whether a match was found')
    make: Optional[str] = Field(None, description='Make value if matched')
    code: Optional[str] = Field(None, description='Vehicle code value if matched')
    model: Optional[str] = Field(None, description='Model value if matched')
    pattern: Optional[str] = Field(None, description='Pattern that matched')
    mapping: Optional[str] = Field(None, description='Original mapping string')