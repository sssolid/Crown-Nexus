"""
Model mapping schemas for API input/output.

This module defines the Pydantic schemas for model mappings
to be used in API input validation and response serialization.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class ModelMappingBase(BaseModel):
    """Base model mapping schema."""
    pattern: str = Field(..., description="Pattern to match in vehicle text")
    mapping: str = Field(..., description="Mapping in format 'Make|VehicleCode|Model'")
    priority: int = Field(0, description="Priority for mapping (higher values are processed first)")
    active: bool = Field(True, description="Whether this mapping is active")

    @field_validator('mapping')
    def validate_mapping_format(cls, v: str) -> str:
        """Validate that mapping is in the correct format."""
        parts = v.split('|')
        if len(parts) != 3:
            raise ValueError("Mapping must be in format 'Make|VehicleCode|Model'")

        if not all(parts):
            raise ValueError("Make, VehicleCode, and Model must not be empty")

        return v


class ModelMappingCreate(ModelMappingBase):
    """Schema for creating a new model mapping."""
    pass


class ModelMappingUpdate(BaseModel):
    """Schema for updating an existing model mapping."""
    pattern: Optional[str] = None
    mapping: Optional[str] = None
    priority: Optional[int] = None
    active: Optional[bool] = None

    @field_validator('mapping')
    def validate_mapping_format(cls, v: Optional[str]) -> Optional[str]:
        """Validate that mapping is in the correct format if provided."""
        if v is None:
            return v

        parts = v.split('|')
        if len(parts) != 3:
            raise ValueError("Mapping must be in format 'Make|VehicleCode|Model'")

        if not all(parts):
            raise ValueError("Make, VehicleCode, and Model must not be empty")

        return v


class ModelMapping(ModelMappingBase):
    """Schema for a model mapping response."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class ModelMappingList(BaseModel):
    """Schema for a list of model mappings."""
    items: List[ModelMapping]
    total: int
