from __future__ import annotations

"""Fitment mapping schema definitions.

This module defines Pydantic schemas for fitment mapping objects.
"""

import uuid
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductInfo(BaseModel):
    """Schema for minimal product information."""

    id: str = Field(..., description="Product ID")
    part_number: str = Field(..., description="Product part number")
    application: Optional[str] = Field(None, description="Product application")

    model_config = ConfigDict(from_attributes=True)


class FitmentMapping(BaseModel):
    """Schema for fitment mapping data."""

    id: str = Field(..., description="Unique identifier")
    product: ProductInfo = Field(..., description="Product information")
    vehicle_id: Optional[int] = Field(None, description="Vehicle ID from VCdb")
    base_vehicle_id: Optional[int] = Field(
        None, description="Base vehicle ID from VCdb"
    )
    part_terminology_id: Optional[int] = Field(
        None, description="Part terminology ID from PCdb"
    )
    position_id: Optional[int] = Field(None, description="Position ID from PCdb")
    attributes: Dict[str, Any] = Field({}, description="Additional attributes")
    is_validated: bool = Field(..., description="Whether mapping is validated")
    is_manual: bool = Field(..., description="Whether mapping was created manually")

    model_config = ConfigDict(from_attributes=True)


class FitmentMappingDetail(FitmentMapping):
    """Schema for detailed fitment mapping data."""

    notes: Optional[str] = Field(None, description="Mapping notes")
    created_at: str = Field(..., description="Creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class FitmentMappingCreate(BaseModel):
    """Schema for creating a new fitment mapping."""

    product_id: uuid.UUID = Field(..., description="Product ID")
    vehicle_id: Optional[int] = Field(None, description="Vehicle ID from VCdb")
    base_vehicle_id: Optional[int] = Field(
        None, description="Base vehicle ID from VCdb"
    )
    part_terminology_id: Optional[int] = Field(
        None, description="Part terminology ID from PCdb"
    )
    position_id: Optional[int] = Field(None, description="Position ID from PCdb")
    attributes: Dict[str, Any] = Field({}, description="Additional attributes")
    is_validated: bool = Field(False, description="Whether mapping is validated")
    is_manual: bool = Field(False, description="Whether mapping is created manually")
    notes: Optional[str] = Field(None, description="Mapping notes")


class FitmentMappingUpdate(BaseModel):
    """Schema for updating an existing fitment mapping."""

    vehicle_id: Optional[int] = Field(None, description="Vehicle ID from VCdb")
    base_vehicle_id: Optional[int] = Field(
        None, description="Base vehicle ID from VCdb"
    )
    part_terminology_id: Optional[int] = Field(
        None, description="Part terminology ID from PCdb"
    )
    position_id: Optional[int] = Field(None, description="Position ID from PCdb")
    attributes: Optional[Dict[str, Any]] = Field(
        None, description="Additional attributes"
    )
    is_validated: Optional[bool] = Field(
        None, description="Whether mapping is validated"
    )
    is_manual: Optional[bool] = Field(
        None, description="Whether mapping is created manually"
    )
    notes: Optional[str] = Field(None, description="Mapping notes")


class FitmentMappingHistory(BaseModel):
    """Schema for fitment mapping history data."""

    id: str = Field(..., description="Unique identifier")
    change_type: str = Field(..., description="Type of change (CREATE, UPDATE, DELETE)")
    previous_values: Optional[Dict[str, Any]] = Field(
        None, description="Previous values"
    )
    new_values: Optional[Dict[str, Any]] = Field(None, description="New values")
    changed_at: str = Field(..., description="When the change was made")
    changed_by_id: Optional[str] = Field(
        None, description="ID of the user who made the change"
    )

    model_config = ConfigDict(from_attributes=True)


class FitmentSearchParameters(BaseModel):
    """Schema for fitment mapping search parameters."""

    product_query: Optional[str] = Field(
        None, description="Filter by product part number or name"
    )
    is_validated: Optional[bool] = Field(
        None, description="Filter by validation status"
    )
    is_manual: Optional[bool] = Field(None, description="Filter by manual entry status")
    page: int = Field(1, description="Page number", ge=1)
    page_size: int = Field(20, description="Page size", ge=1, le=100)


class FitmentMappingSearchResponse(BaseModel):
    """Schema for paginated fitment mapping search response."""

    items: List[FitmentMapping] = Field(..., description="List of fitment mappings")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    pages: int = Field(..., description="Total number of pages")


class FitmentMappingHistoryResponse(BaseModel):
    """Schema for paginated fitment mapping history response."""

    items: List[FitmentMappingHistory] = Field(
        ..., description="List of history records"
    )
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    pages: int = Field(..., description="Total number of pages")
