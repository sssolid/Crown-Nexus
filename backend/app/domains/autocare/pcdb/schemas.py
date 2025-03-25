from __future__ import annotations

"""PCdb schema definitions.

This module defines Pydantic schemas for part-related objects,
including categories, positions, and part details.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class Category(BaseModel):
    """Schema for part category data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    category_id: int = Field(..., description="Category ID from PCdb")
    category_name: str = Field(..., description="Category name")

    model_config = ConfigDict(from_attributes=True)


class SubCategory(BaseModel):
    """Schema for part subcategory data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    subcategory_id: int = Field(..., description="Subcategory ID from PCdb")
    subcategory_name: str = Field(..., description="Subcategory name")

    model_config = ConfigDict(from_attributes=True)


class Position(BaseModel):
    """Schema for part position data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    position_id: int = Field(..., description="Position ID from PCdb")
    position: str = Field(..., description="Position name")

    model_config = ConfigDict(from_attributes=True)


class Part(BaseModel):
    """Schema for part data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    part_terminology_id: int = Field(..., description="Part terminology ID from PCdb")
    part_terminology_name: str = Field(..., description="Part terminology name")
    parts_description_id: Optional[int] = Field(
        None, description="Parts description ID"
    )

    model_config = ConfigDict(from_attributes=True)


class PartDetail(Part):
    """Schema for detailed part data."""

    description: Optional[str] = Field(None, description="Part description")
    categories: List[Dict[str, Any]] = Field(
        [], description="Categories and subcategories"
    )
    positions: List[Dict[str, Any]] = Field([], description="Positions")
    superseded_by: List[Dict[str, Any]] = Field(
        [], description="Parts that supersede this one"
    )
    supersedes: List[Dict[str, Any]] = Field(
        [], description="Parts this one supersedes"
    )

    model_config = ConfigDict(from_attributes=True)


class PartSearchParameters(BaseModel):
    """Schema for part search parameters."""

    search_term: str = Field(..., description="Search term")
    categories: Optional[List[int]] = Field(None, description="Filter by category IDs")
    page: int = Field(1, description="Page number", ge=1)
    page_size: int = Field(20, description="Page size", ge=1, le=100)


class PartSearchResponse(BaseModel):
    """Schema for paginated part search response."""

    items: List[Part] = Field(..., description="List of parts")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    pages: int = Field(..., description="Total number of pages")
