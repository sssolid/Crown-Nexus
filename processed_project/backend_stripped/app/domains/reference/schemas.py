from __future__ import annotations
'Reference schema definitions.\n\nThis module defines Pydantic schemas for reference data objects,\nincluding Color, ConstructionType, Texture, PackagingType, Hardware,\nTariffCode, UnspscCode, and Warehouse.\n'
import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
class ColorBase(BaseModel):
    name: str = Field(..., description='Color name')
    hex_code: Optional[str] = Field(None, description='Hexadecimal color code')
    @field_validator('hex_code')
    @classmethod
    def validate_hex_code(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not v.startswith('#'):
            v = f'#{v}'
        if not (len(v) == 7 and v[0] == '#' and all((c in '0123456789ABCDEFabcdef' for c in v[1:]))):
            raise ValueError('Hex code must be in format #RRGGBB')
        return v.upper()
class ColorCreate(ColorBase):
    pass
class ColorUpdate(BaseModel):
    name: Optional[str] = Field(None, description='Color name')
    hex_code: Optional[str] = Field(None, description='Hexadecimal color code')
    @field_validator('hex_code')
    @classmethod
    def validate_hex_code(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not v.startswith('#'):
            v = f'#{v}'
        if not (len(v) == 7 and v[0] == '#' and all((c in '0123456789ABCDEFabcdef' for c in v[1:]))):
            raise ValueError('Hex code must be in format #RRGGBB')
        return v.upper()
class ColorInDB(ColorBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    created_at: datetime = Field(..., description='Creation timestamp')
    model_config = ConfigDict(from_attributes=True)
class Color(ColorInDB):
    pass
class ConstructionTypeBase(BaseModel):
    name: str = Field(..., description='Construction type name')
    description: Optional[str] = Field(None, description='Construction type description')
class ConstructionTypeCreate(ConstructionTypeBase):
    pass
class ConstructionTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, description='Construction type name')
    description: Optional[str] = Field(None, description='Construction type description')
class ConstructionTypeInDB(ConstructionTypeBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    created_at: datetime = Field(..., description='Creation timestamp')
    model_config = ConfigDict(from_attributes=True)
class ConstructionType(ConstructionTypeInDB):
    pass
class TextureBase(BaseModel):
    name: str = Field(..., description='Texture name')
    description: Optional[str] = Field(None, description='Texture description')
class TextureCreate(TextureBase):
    pass
class TextureUpdate(BaseModel):
    name: Optional[str] = Field(None, description='Texture name')
    description: Optional[str] = Field(None, description='Texture description')
class TextureInDB(TextureBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    created_at: datetime = Field(..., description='Creation timestamp')
    model_config = ConfigDict(from_attributes=True)
class Texture(TextureInDB):
    pass
class PackagingTypeBase(BaseModel):
    name: str = Field(..., description='Packaging type name')
    pies_code: Optional[str] = Field(None, description='PIES standard code')
    description: Optional[str] = Field(None, description='Packaging type description')
    source: str = Field('Custom', description='Source of the packaging type data')
class PackagingTypeCreate(PackagingTypeBase):
    pass
class PackagingTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, description='Packaging type name')
    pies_code: Optional[str] = Field(None, description='PIES standard code')
    description: Optional[str] = Field(None, description='Packaging type description')
    source: Optional[str] = Field(None, description='Source of the packaging type data')
class PackagingTypeInDB(PackagingTypeBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    created_at: datetime = Field(..., description='Creation timestamp')
    model_config = ConfigDict(from_attributes=True)
class PackagingType(PackagingTypeInDB):
    pass
class HardwareBase(BaseModel):
    name: str = Field(..., description='Hardware item name')
    description: Optional[str] = Field(None, description='Hardware item description')
    part_number: Optional[str] = Field(None, description='Manufacturer part number')
class HardwareCreate(HardwareBase):
    pass
class HardwareUpdate(BaseModel):
    name: Optional[str] = Field(None, description='Hardware item name')
    description: Optional[str] = Field(None, description='Hardware item description')
    part_number: Optional[str] = Field(None, description='Manufacturer part number')
class HardwareInDB(HardwareBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    created_at: datetime = Field(..., description='Creation timestamp')
    model_config = ConfigDict(from_attributes=True)
class Hardware(HardwareInDB):
    pass
class TariffCodeBase(BaseModel):
    code: str = Field(..., description='Tariff code number')
    description: str = Field(..., description='Tariff code description')
    country_id: Optional[uuid.UUID] = Field(None, description='Country ID')
class TariffCodeCreate(TariffCodeBase):
    pass
class TariffCodeUpdate(BaseModel):
    code: Optional[str] = Field(None, description='Tariff code number')
    description: Optional[str] = Field(None, description='Tariff code description')
    country_id: Optional[uuid.UUID] = Field(None, description='Country ID')
class TariffCodeInDB(TariffCodeBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    created_at: datetime = Field(..., description='Creation timestamp')
    model_config = ConfigDict(from_attributes=True)
class TariffCode(TariffCodeInDB):
    country: Optional[Dict[str, Any]] = Field(None, description='Country details')
class UnspscCodeBase(BaseModel):
    code: str = Field(..., description='UNSPSC code number')
    description: str = Field(..., description='UNSPSC code description')
    segment: Optional[str] = Field(None, description='Segment description')
    family: Optional[str] = Field(None, description='Family description')
    class_: Optional[str] = Field(None, description='Class description')
    commodity: Optional[str] = Field(None, description='Commodity description')
class UnspscCodeCreate(UnspscCodeBase):
    pass
class UnspscCodeUpdate(BaseModel):
    code: Optional[str] = Field(None, description='UNSPSC code number')
    description: Optional[str] = Field(None, description='UNSPSC code description')
    segment: Optional[str] = Field(None, description='Segment description')
    family: Optional[str] = Field(None, description='Family description')
    class_: Optional[str] = Field(None, description='Class description')
    commodity: Optional[str] = Field(None, description='Commodity description')
class UnspscCodeInDB(UnspscCodeBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    created_at: datetime = Field(..., description='Creation timestamp')
    model_config = ConfigDict(from_attributes=True)
class UnspscCode(UnspscCodeInDB):
    pass
class WarehouseBase(BaseModel):
    name: str = Field(..., description='Warehouse name')
    address_id: Optional[uuid.UUID] = Field(None, description='Address ID')
    is_active: bool = Field(True, description='Whether the warehouse is active')
class WarehouseCreate(WarehouseBase):
    pass
class WarehouseUpdate(BaseModel):
    name: Optional[str] = Field(None, description='Warehouse name')
    address_id: Optional[uuid.UUID] = Field(None, description='Address ID')
    is_active: Optional[bool] = Field(None, description='Whether the warehouse is active')
class WarehouseInDB(WarehouseBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    created_at: datetime = Field(..., description='Creation timestamp')
    model_config = ConfigDict(from_attributes=True)
class Warehouse(WarehouseInDB):
    address: Optional[Dict[str, Any]] = Field(None, description='Address details')