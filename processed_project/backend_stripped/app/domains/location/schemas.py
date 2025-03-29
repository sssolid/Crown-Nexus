from __future__ import annotations
'Location schema definitions.\n\nThis module defines Pydantic schemas for location-related objects,\nincluding countries and addresses.\n'
import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
class CountryBase(BaseModel):
    name: str = Field(..., description='Country name')
    iso_alpha_2: str = Field(..., min_length=2, max_length=2, description='ISO 3166-1 alpha-2 code')
    iso_alpha_3: str = Field(..., min_length=3, max_length=3, description='ISO 3166-1 alpha-3 code')
    iso_numeric: Optional[str] = Field(None, max_length=3, description='ISO 3166-1 numeric code')
    region: Optional[str] = Field(None, description='Geographic region')
    subregion: Optional[str] = Field(None, description='Geographic subregion')
    currency: Optional[str] = Field(None, min_length=3, max_length=3, description='ISO 4217 currency code')
    @field_validator('iso_alpha_2', 'iso_alpha_3', 'currency', mode='before')
    @classmethod
    def uppercase_codes(cls, v: Optional[str]) -> Optional[str]:
        return v.upper() if v else v
class CountryCreate(CountryBase):
    pass
class CountryUpdate(BaseModel):
    name: Optional[str] = Field(None, description='Country name')
    iso_alpha_2: Optional[str] = Field(None, min_length=2, max_length=2, description='ISO 3166-1 alpha-2 code')
    iso_alpha_3: Optional[str] = Field(None, min_length=3, max_length=3, description='ISO 3166-1 alpha-3 code')
    iso_numeric: Optional[str] = Field(None, max_length=3, description='ISO 3166-1 numeric code')
    region: Optional[str] = Field(None, description='Geographic region')
    subregion: Optional[str] = Field(None, description='Geographic subregion')
    currency: Optional[str] = Field(None, min_length=3, max_length=3, description='ISO 4217 currency code')
    @field_validator('iso_alpha_2', 'iso_alpha_3', 'currency', mode='before')
    @classmethod
    def uppercase_codes(cls, v: Optional[str]) -> Optional[str]:
        return v.upper() if v else v
class CountryInDB(CountryBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    created_at: datetime = Field(..., description='Creation timestamp')
    model_config = ConfigDict(from_attributes=True)
class Country(CountryInDB):
    pass
class AddressBase(BaseModel):
    street: str = Field(..., description='Street address')
    city: str = Field(..., description='City name')
    state: Optional[str] = Field(None, description='State or province')
    postal_code: str = Field(..., description='Postal or ZIP code')
    country_id: uuid.UUID = Field(..., description='Associated country ID')
    latitude: Optional[float] = Field(None, description='Geographic latitude')
    longitude: Optional[float] = Field(None, description='Geographic longitude')
    @field_validator('latitude')
    @classmethod
    def validate_latitude(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and (v < -90 or v > 90):
            raise ValueError('Latitude must be between -90 and 90')
        return v
    @field_validator('longitude')
    @classmethod
    def validate_longitude(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and (v < -180 or v > 180):
            raise ValueError('Longitude must be between -180 and 180')
        return v
class AddressCreate(AddressBase):
    pass
class AddressUpdate(BaseModel):
    street: Optional[str] = Field(None, description='Street address')
    city: Optional[str] = Field(None, description='City name')
    state: Optional[str] = Field(None, description='State or province')
    postal_code: Optional[str] = Field(None, description='Postal or ZIP code')
    country_id: Optional[uuid.UUID] = Field(None, description='Associated country ID')
    latitude: Optional[float] = Field(None, description='Geographic latitude')
    longitude: Optional[float] = Field(None, description='Geographic longitude')
    @field_validator('latitude')
    @classmethod
    def validate_latitude(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and (v < -90 or v > 90):
            raise ValueError('Latitude must be between -90 and 90')
        return v
    @field_validator('longitude')
    @classmethod
    def validate_longitude(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and (v < -180 or v > 180):
            raise ValueError('Longitude must be between -180 and 180')
        return v
class AddressInDB(AddressBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    created_at: datetime = Field(..., description='Creation timestamp')
    model_config = ConfigDict(from_attributes=True)
class Address(AddressInDB):
    country: Optional[Country] = Field(None, description='Country details')
class GeocodeRequest(BaseModel):
    address: Optional[str] = Field(None, description='Full address string')
    street: Optional[str] = Field(None, description='Street address')
    city: Optional[str] = Field(None, description='City')
    state: Optional[str] = Field(None, description='State or province')
    postal_code: Optional[str] = Field(None, description='Postal or ZIP code')
    country: Optional[str] = Field(None, description='Country')
class GeocodeResult(BaseModel):
    latitude: float = Field(..., description='Geographic latitude')
    longitude: float = Field(..., description='Geographic longitude')
    formatted_address: str = Field(..., description='Formatted address')
    confidence: int = Field(..., ge=0, le=100, description='Confidence score (0-100)')
    components: Dict[str, Any] = Field(..., description='Address components')