from __future__ import annotations

"""Country schema definitions.

This module defines Pydantic schemas for Country objects,
including creation, update, and response models.
"""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CountryBase(BaseModel):
    """Base schema for country data.

    Attributes:
        name: Country name.
        iso_alpha_2: ISO 3166-1 alpha-2 code (2 letters).
        iso_alpha_3: ISO 3166-1 alpha-3 code (3 letters).
        iso_numeric: ISO 3166-1 numeric code (3 digits).
        region: Geographic region.
        subregion: Geographic subregion.
        currency: ISO 4217 currency code.
    """

    name: str = Field(..., description="Country name")
    iso_alpha_2: str = Field(
        ..., min_length=2, max_length=2, description="ISO 3166-1 alpha-2 code"
    )
    iso_alpha_3: str = Field(
        ..., min_length=3, max_length=3, description="ISO 3166-1 alpha-3 code"
    )
    iso_numeric: Optional[str] = Field(
        None, min_length=1, max_length=3, description="ISO 3166-1 numeric code"
    )
    region: Optional[str] = Field(None, description="Geographic region")
    subregion: Optional[str] = Field(None, description="Geographic subregion")
    currency: Optional[str] = Field(
        None, min_length=3, max_length=3, description="ISO 4217 currency code"
    )

    @field_validator("iso_alpha_2", "iso_alpha_3", mode="before")
    @classmethod
    def uppercase_codes(cls, v: str) -> str:
        """Ensure ISO codes are uppercase.

        Args:
            v: The code value to validate.

        Returns:
            Uppercase version of the code.
        """
        return v.upper() if v else v


class CountryCreate(CountryBase):
    """Schema for creating a new country."""

    pass


class CountryUpdate(BaseModel):
    """Schema for updating an existing country.

    All fields are optional to allow partial updates.
    """

    name: Optional[str] = Field(None, description="Country name")
    iso_alpha_2: Optional[str] = Field(
        None, min_length=2, max_length=2, description="ISO 3166-1 alpha-2 code"
    )
    iso_alpha_3: Optional[str] = Field(
        None, min_length=3, max_length=3, description="ISO 3166-1 alpha-3 code"
    )
    iso_numeric: Optional[str] = Field(
        None, min_length=1, max_length=3, description="ISO 3166-1 numeric code"
    )
    region: Optional[str] = Field(None, description="Geographic region")
    subregion: Optional[str] = Field(None, description="Geographic subregion")
    currency: Optional[str] = Field(
        None, min_length=3, max_length=3, description="ISO 4217 currency code"
    )

    @field_validator("iso_alpha_2", "iso_alpha_3", "currency", mode="before")
    @classmethod
    def uppercase_codes(cls, v: Optional[str]) -> Optional[str]:
        """Ensure ISO codes are uppercase.

        Args:
            v: The code value to validate.

        Returns:
            Uppercase version of the code or None if not provided.
        """
        return v.upper() if v else v


class CountryInDB(CountryBase):
    """Schema for country data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = ConfigDict(from_attributes=True)


class Country(CountryInDB):
    """Schema for complete country data in API responses."""

    pass
