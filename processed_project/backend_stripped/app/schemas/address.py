from __future__ import annotations
'Address schema definitions.\n\nThis module defines Pydantic schemas for Address objects,\nincluding creation, update, and response models.\n'
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
class AddressBase(BaseModel):
    street: str = Field(..., description='Street address')
    city: str = Field(..., description='City name')
    state: Optional[str] = Field(None, description='State or province')
    postal_code: str = Field(..., description='Postal or ZIP code')
    country_id: uuid.UUID = Field(..., description='ID of associated country')
class AddressCreate(AddressBase):
    latitude: Optional[float] = Field(None, description='Latitude coordinate')
    longitude: Optional[float] = Field(None, description='Longitude coordinate')
class AddressUpdate(BaseModel):
    street: Optional[str] = Field(None, description='Street address')
    city: Optional[str] = Field(None, description='City name')
    state: Optional[str] = Field(None, description='State or province')
    postal_code: Optional[str] = Field(None, description='Postal or ZIP code')
    country_id: Optional[uuid.UUID] = Field(None, description='ID of associated country')
    latitude: Optional[float] = Field(None, description='Latitude coordinate')
    longitude: Optional[float] = Field(None, description='Longitude coordinate')
class AddressInDB(AddressBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    latitude: Optional[float] = Field(None, description='Latitude coordinate')
    longitude: Optional[float] = Field(None, description='Longitude coordinate')
    created_at: datetime = Field(..., description='Creation timestamp')
    model_config = ConfigDict(from_attributes=True)
class Address(AddressInDB):
    country: Optional['Country'] = Field(None, description='Country details')
from app.schemas.country import Country
Address.model_rebuild()