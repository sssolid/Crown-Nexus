from __future__ import annotations

"""Model mapping schema definitions.

This module defines Pydantic schemas for vehicle model mapping objects,
which translate between different vehicle model naming systems.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ModelMappingBase(BaseModel):
    """Base schema for ModelMapping data.

    Attributes:
        pattern: Pattern to match in vehicle text.
        mapping: Mapping in format 'Make|VehicleCode|Model'.
        priority: Priority for mapping (higher values are processed first).
        active: Whether this mapping is active.
    """

    pattern: str = Field(..., description="Pattern to match in vehicle text")
    mapping: str = Field(..., description="Mapping in format 'Make|VehicleCode|Model'")
    priority: int = Field(
        0, description="Priority for mapping (higher values are processed first)"
    )
    active: bool = Field(True, description="Whether this mapping is active")

    @field_validator("mapping")
    @classmethod
    def validate_mapping_format(cls, v: str) -> str:
        """Validate mapping format.

        Args:
            v: The mapping string to validate.

        Returns:
            Validated mapping string.

        Raises:
            ValueError: If the mapping format is invalid.
        """
        parts = v.split("|")
        if len(parts) != 3:
            raise ValueError(
                "Mapping must be in format 'Make|VehicleCode|Model' with exactly 2 pipe separators"
            )

        if not any(parts):
            raise ValueError(
                "At least one of Make, VehicleCode, or Model must not be empty"
            )

        return v


class ModelMappingCreate(ModelMappingBase):
    """Schema for creating a new ModelMapping."""

    pass


class ModelMappingUpdate(BaseModel):
    """Schema for updating an existing ModelMapping.

    All fields are optional to allow partial updates.
    """

    pattern: Optional[str] = Field(None, description="Pattern to match in vehicle text")
    mapping: Optional[str] = Field(
        None, description="Mapping in format 'Make|VehicleCode|Model'"
    )
    priority: Optional[int] = Field(
        None, description="Priority for mapping (higher values are processed first)"
    )
    active: Optional[bool] = Field(None, description="Whether this mapping is active")

    @field_validator("mapping")
    @classmethod
    def validate_mapping_format(cls, v: Optional[str]) -> Optional[str]:
        """Validate mapping format if provided.

        Args:
            v: The mapping string to validate or None.

        Returns:
            Validated mapping string or None.

        Raises:
            ValueError: If the mapping format is invalid.
        """
        if v is None:
            return v

        parts = v.split("|")
        if len(parts) != 3:
            raise ValueError(
                "Mapping must be in format 'Make|VehicleCode|Model' with exactly 2 pipe separators"
            )

        if not any(parts):
            raise ValueError(
                "At least one of Make, VehicleCode, or Model must not be empty"
            )

        return v


class ModelMappingInDB(ModelMappingBase):
    """Schema for ModelMapping data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: int = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class ModelMapping(ModelMappingInDB):
    """Schema for complete ModelMapping data in API responses.

    Includes additional computed properties.
    """

    @property
    def make(self) -> str:
        """Get the make part of the mapping.

        Returns:
            The make value or empty string if not available.
        """
        parts = self.mapping.split("|")
        return parts[0] if len(parts) > 0 else ""

    @property
    def vehicle_code(self) -> str:
        """Get the vehicle code part of the mapping.

        Returns:
            The vehicle code value or empty string if not available.
        """
        parts = self.mapping.split("|")
        return parts[1] if len(parts) > 1 else ""

    @property
    def model(self) -> str:
        """Get the model part of the mapping.

        Returns:
            The model value or empty string if not available.
        """
        parts = self.mapping.split("|")
        return parts[2] if len(parts) > 2 else ""


class ModelMappingPaginatedResponse(BaseModel):
    """Schema for paginated model mapping data.

    Attributes:
        items: List of model mappings.
        total: Total number of items.
        page: Current page number.
        page_size: Number of items per page.
        pages: Total number of pages.
    """

    items: List[ModelMapping] = Field(..., description="List of model mappings")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    pages: int = Field(..., description="Total number of pages")


class VehicleMatchRequest(BaseModel):
    """Schema for vehicle matching request.

    Attributes:
        vehicle_string: Vehicle string to match against patterns.
    """

    vehicle_string: str = Field(..., description="Vehicle string to match")


class VehicleMatchResponse(BaseModel):
    """Schema for vehicle matching response.

    Attributes:
        matched: Whether a match was found.
        make: Make value if matched.
        code: Vehicle code value if matched.
        model: Model value if matched.
        pattern: Pattern that matched.
        mapping: Original mapping string.
    """

    matched: bool = Field(..., description="Whether a match was found")
    make: Optional[str] = Field(None, description="Make value if matched")
    code: Optional[str] = Field(None, description="Vehicle code value if matched")
    model: Optional[str] = Field(None, description="Model value if matched")
    pattern: Optional[str] = Field(None, description="Pattern that matched")
    mapping: Optional[str] = Field(None, description="Original mapping string")
