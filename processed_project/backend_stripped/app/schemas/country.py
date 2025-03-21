from __future__ import annotations
'Country schema definitions.\n\nThis module defines Pydantic schemas for Country objects,\nincluding creation, update, and response models.\n'
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
class CountryBase(BaseModel):
    name: str = Field(..., description='Country name')
    iso_alpha_2: str = Field(..., min_length=2, max_length=2, description='ISO 3166-1 alpha-2 code')
    iso_alpha_3: str = Field(..., min_length=3, max_length=3, description='ISO 3166-1 alpha-3 code')
    iso_numeric: Optional[str] = Field(None, min_length=1, max_length=3, description='ISO 3166-1 numeric code')
    region: Optional[str] = Field(None, description='Geographic region')
    subregion: Optional[str] = Field(None, description='Geographic subregion')
    currency: Optional[str] = Field(None, min_length=3, max_length=3, description='ISO 4217 currency code')
    @field_validator('iso_alpha_2', 'iso_alpha_3', mode='before')
    @classmethod
    def uppercase_codes(cls, v: str) -> str:
        return v.upper() if v else v
class CountryCreate(CountryBase):
    pass
class CountryUpdate(BaseModel):
    name: Optional[str] = Field(None, description='Country name')
    iso_alpha_2: Optional[str] = Field(None, min_length=2, max_length=2, description='ISO 3166-1 alpha-2 code')
    iso_alpha_3: Optional[str] = Field(None, min_length=3, max_length=3, description='ISO 3166-1 alpha-3 code')
    iso_numeric: Optional[str] = Field(None, min_length=1, max_length=3, description='ISO 3166-1 numeric code')
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