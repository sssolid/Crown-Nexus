from __future__ import annotations

"""Location schema definitions.

This module defines Pydantic schemas for location-related objects,
including countries and addresses.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CountryBase(BaseModel):
    """Base schema for Country data.

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
        None, max_length=3, description="ISO 3166-1 numeric code"
    )
    region: Optional[str] = Field(None, description="Geographic region")
    subregion: Optional[str] = Field(None, description="Geographic subregion")
    currency: Optional[str] = Field(
        None, min_length=3, max_length=3, description="ISO 4217 currency code"
    )

    @field_validator("iso_alpha_2", "iso_alpha_3", "currency", mode="before")
    @classmethod
    def uppercase_codes(cls, v: Optional[str]) -> Optional[str]:
        """Convert codes to uppercase if provided.

        Args:
            v: The code to convert or None.

        Returns:
            Uppercase code or None.
        """
        return v.upper() if v else v


class CountryCreate(CountryBase):
    """Schema for creating a new Country."""

    pass


class CountryUpdate(BaseModel):
    """Schema for updating an existing Country.

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
        None, max_length=3, description="ISO 3166-1 numeric code"
    )
    region: Optional[str] = Field(None, description="Geographic region")
    subregion: Optional[str] = Field(None, description="Geographic subregion")
    currency: Optional[str] = Field(
        None, min_length=3, max_length=3, description="ISO 4217 currency code"
    )

    @field_validator("iso_alpha_2", "iso_alpha_3", "currency", mode="before")
    @classmethod
    def uppercase_codes(cls, v: Optional[str]) -> Optional[str]:
        """Convert codes to uppercase if provided.

        Args:
            v: The code to convert or None.

        Returns:
            Uppercase code or None.
        """
        return v.upper() if v else v


class CountryInDB(CountryBase):
    """Schema for Country data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = ConfigDict(from_attributes=True)


class Country(CountryInDB):
    """Schema for complete Country data in API responses."""

    pass


class AddressBase(BaseModel):
    """Base schema for Address data.

    Attributes:
        street: Street address.
        city: City name.
        state: State or province.
        postal_code: Postal or ZIP code.
        country_id: ID of the associated country.
        latitude: Geographic latitude.
        longitude: Geographic longitude.
    """

    street: str = Field(..., description="Street address")
    city: str = Field(..., description="City name")
    state: Optional[str] = Field(None, description="State or province")
    postal_code: str = Field(..., description="Postal or ZIP code")
    country_id: uuid.UUID = Field(..., description="Associated country ID")
    latitude: Optional[float] = Field(None, description="Geographic latitude")
    longitude: Optional[float] = Field(None, description="Geographic longitude")

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, v: Optional[float]) -> Optional[float]:
        """Validate latitude value if provided.

        Args:
            v: The latitude to validate or None.

        Returns:
            Validated latitude or None.

        Raises:
            ValueError: If the latitude is outside valid range.
        """
        if v is not None and (v < -90 or v > 90):
            raise ValueError("Latitude must be between -90 and 90")
        return v

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, v: Optional[float]) -> Optional[float]:
        """Validate longitude value if provided.

        Args:
            v: The longitude to validate or None.

        Returns:
            Validated longitude or None.

        Raises:
            ValueError: If the longitude is outside valid range.
        """
        if v is not None and (v < -180 or v > 180):
            raise ValueError("Longitude must be between -180 and 180")
        return v


class AddressCreate(AddressBase):
    """Schema for creating a new Address."""

    pass


class AddressUpdate(BaseModel):
    """Schema for updating an existing Address.

    All fields are optional to allow partial updates.
    """

    street: Optional[str] = Field(None, description="Street address")
    city: Optional[str] = Field(None, description="City name")
    state: Optional[str] = Field(None, description="State or province")
    postal_code: Optional[str] = Field(None, description="Postal or ZIP code")
    country_id: Optional[uuid.UUID] = Field(None, description="Associated country ID")
    latitude: Optional[float] = Field(None, description="Geographic latitude")
    longitude: Optional[float] = Field(None, description="Geographic longitude")

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, v: Optional[float]) -> Optional[float]:
        """Validate latitude value if provided.

        Args:
            v: The latitude to validate or None.

        Returns:
            Validated latitude or None.

        Raises:
            ValueError: If the latitude is outside valid range.
        """
        if v is not None and (v < -90 or v > 90):
            raise ValueError("Latitude must be between -90 and 90")
        return v

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, v: Optional[float]) -> Optional[float]:
        """Validate longitude value if provided.

        Args:
            v: The longitude to validate or None.

        Returns:
            Validated longitude or None.

        Raises:
            ValueError: If the longitude is outside valid range.
        """
        if v is not None and (v < -180 or v > 180):
            raise ValueError("Longitude must be between -180 and 180")
        return v


class AddressInDB(AddressBase):
    """Schema for Address data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = ConfigDict(from_attributes=True)


class Address(AddressInDB):
    """Schema for complete Address data in API responses.

    Includes related entities like country details.
    """

    country: Optional[Country] = Field(None, description="Country details")


class GeocodeRequest(BaseModel):
    """Schema for geocoding request.

    Attributes:
        address: Full address string to geocode.
        street: Street address component.
        city: City component.
        state: State or province component.
        postal_code: Postal or ZIP code component.
        country: Country component.
    """

    address: Optional[str] = Field(None, description="Full address string")
    street: Optional[str] = Field(None, description="Street address")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State or province")
    postal_code: Optional[str] = Field(None, description="Postal or ZIP code")
    country: Optional[str] = Field(None, description="Country")


class GeocodeResult(BaseModel):
    """Schema for geocoding result.

    Attributes:
        latitude: Geographic latitude.
        longitude: Geographic longitude.
        formatted_address: Formatted address string.
        confidence: Confidence score (0-100).
        components: Address components.
    """

    latitude: float = Field(..., description="Geographic latitude")
    longitude: float = Field(..., description="Geographic longitude")
    formatted_address: str = Field(..., description="Formatted address")
    confidence: int = Field(..., ge=0, le=100, description="Confidence score (0-100)")
    components: Dict[str, Any] = Field(..., description="Address components")
