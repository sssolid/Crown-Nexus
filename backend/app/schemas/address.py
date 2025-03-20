from __future__ import annotations

"""Address schema definitions.

This module defines Pydantic schemas for Address objects,
including creation, update, and response models.
"""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AddressBase(BaseModel):
    """Base schema for address data.

    Attributes:
        street: Street address including number and name.
        city: City name.
        state: State or province name.
        postal_code: Postal or ZIP code.
        country_id: ID of the associated country.
    """

    street: str = Field(..., description="Street address")
    city: str = Field(..., description="City name")
    state: Optional[str] = Field(None, description="State or province")
    postal_code: str = Field(..., description="Postal or ZIP code")
    country_id: uuid.UUID = Field(..., description="ID of associated country")


class AddressCreate(AddressBase):
    """Schema for creating a new address."""

    latitude: Optional[float] = Field(None, description="Latitude coordinate")
    longitude: Optional[float] = Field(None, description="Longitude coordinate")


class AddressUpdate(BaseModel):
    """Schema for updating an existing address.

    All fields are optional to allow partial updates.
    """

    street: Optional[str] = Field(None, description="Street address")
    city: Optional[str] = Field(None, description="City name")
    state: Optional[str] = Field(None, description="State or province")
    postal_code: Optional[str] = Field(None, description="Postal or ZIP code")
    country_id: Optional[uuid.UUID] = Field(
        None, description="ID of associated country"
    )
    latitude: Optional[float] = Field(None, description="Latitude coordinate")
    longitude: Optional[float] = Field(None, description="Longitude coordinate")


class AddressInDB(AddressBase):
    """Schema for address data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    latitude: Optional[float] = Field(None, description="Latitude coordinate")
    longitude: Optional[float] = Field(None, description="Longitude coordinate")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = ConfigDict(from_attributes=True)


class Address(AddressInDB):
    """Schema for complete address data in API responses.

    Includes related entities like country details.
    """

    country: Optional["Country"] = Field(None, description="Country details")


# Forward reference for Country which will be imported elsewhere
from app.schemas.country import Country

Address.model_rebuild()
