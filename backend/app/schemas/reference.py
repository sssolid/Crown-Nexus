from __future__ import annotations

"""Reference schema definitions.

This module defines Pydantic schemas for reference data objects,
including Color, ConstructionType, Texture, PackagingType, Hardware,
TariffCode, UnspscCode, and Warehouse.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ColorBase(BaseModel):
    """Base schema for Color data.

    Attributes:
        name: Color name.
        hex_code: Hexadecimal color code.
    """

    name: str = Field(..., description="Color name")
    hex_code: Optional[str] = Field(None, description="Hexadecimal color code")

    @field_validator("hex_code")
    @classmethod
    def validate_hex_code(cls, v: Optional[str]) -> Optional[str]:
        """Validate hex code format.

        Args:
            v: The hex code to validate or None.

        Returns:
            Validated hex code or None.

        Raises:
            ValueError: If the hex code format is invalid.
        """
        if v is None:
            return v

        # Add # if missing
        if not v.startswith("#"):
            v = f"#{v}"

        # Check if format is valid
        if not (
            len(v) == 7
            and v[0] == "#"
            and all(c in "0123456789ABCDEFabcdef" for c in v[1:])
        ):
            raise ValueError("Hex code must be in format #RRGGBB")

        return v.upper()


class ColorCreate(ColorBase):
    """Schema for creating a new Color."""

    pass


class ColorUpdate(BaseModel):
    """Schema for updating an existing Color.

    All fields are optional to allow partial updates.
    """

    name: Optional[str] = Field(None, description="Color name")
    hex_code: Optional[str] = Field(None, description="Hexadecimal color code")

    @field_validator("hex_code")
    @classmethod
    def validate_hex_code(cls, v: Optional[str]) -> Optional[str]:
        """Validate hex code format if provided.

        Args:
            v: The hex code to validate or None.

        Returns:
            Validated hex code or None.

        Raises:
            ValueError: If the hex code format is invalid.
        """
        if v is None:
            return v

        # Add # if missing
        if not v.startswith("#"):
            v = f"#{v}"

        # Check if format is valid
        if not (
            len(v) == 7
            and v[0] == "#"
            and all(c in "0123456789ABCDEFabcdef" for c in v[1:])
        ):
            raise ValueError("Hex code must be in format #RRGGBB")

        return v.upper()


class ColorInDB(ColorBase):
    """Schema for Color data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = ConfigDict(from_attributes=True)


class Color(ColorInDB):
    """Schema for complete Color data in API responses."""

    pass


class ConstructionTypeBase(BaseModel):
    """Base schema for ConstructionType data.

    Attributes:
        name: Construction type name.
        description: Description of the construction type.
    """

    name: str = Field(..., description="Construction type name")
    description: Optional[str] = Field(
        None, description="Construction type description"
    )


class ConstructionTypeCreate(ConstructionTypeBase):
    """Schema for creating a new ConstructionType."""

    pass


class ConstructionTypeUpdate(BaseModel):
    """Schema for updating an existing ConstructionType.

    All fields are optional to allow partial updates.
    """

    name: Optional[str] = Field(None, description="Construction type name")
    description: Optional[str] = Field(
        None, description="Construction type description"
    )


class ConstructionTypeInDB(ConstructionTypeBase):
    """Schema for ConstructionType data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = ConfigDict(from_attributes=True)


class ConstructionType(ConstructionTypeInDB):
    """Schema for complete ConstructionType data in API responses."""

    pass


class TextureBase(BaseModel):
    """Base schema for Texture data.

    Attributes:
        name: Texture name.
        description: Description of the texture.
    """

    name: str = Field(..., description="Texture name")
    description: Optional[str] = Field(None, description="Texture description")


class TextureCreate(TextureBase):
    """Schema for creating a new Texture."""

    pass


class TextureUpdate(BaseModel):
    """Schema for updating an existing Texture.

    All fields are optional to allow partial updates.
    """

    name: Optional[str] = Field(None, description="Texture name")
    description: Optional[str] = Field(None, description="Texture description")


class TextureInDB(TextureBase):
    """Schema for Texture data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = ConfigDict(from_attributes=True)


class Texture(TextureInDB):
    """Schema for complete Texture data in API responses."""

    pass


class PackagingTypeBase(BaseModel):
    """Base schema for PackagingType data.

    Attributes:
        name: Packaging type name.
        pies_code: PIES standard code.
        description: Description of the packaging type.
        source: Source of the packaging type data.
    """

    name: str = Field(..., description="Packaging type name")
    pies_code: Optional[str] = Field(None, description="PIES standard code")
    description: Optional[str] = Field(None, description="Packaging type description")
    source: str = Field("Custom", description="Source of the packaging type data")


class PackagingTypeCreate(PackagingTypeBase):
    """Schema for creating a new PackagingType."""

    pass


class PackagingTypeUpdate(BaseModel):
    """Schema for updating an existing PackagingType.

    All fields are optional to allow partial updates.
    """

    name: Optional[str] = Field(None, description="Packaging type name")
    pies_code: Optional[str] = Field(None, description="PIES standard code")
    description: Optional[str] = Field(None, description="Packaging type description")
    source: Optional[str] = Field(None, description="Source of the packaging type data")


class PackagingTypeInDB(PackagingTypeBase):
    """Schema for PackagingType data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = ConfigDict(from_attributes=True)


class PackagingType(PackagingTypeInDB):
    """Schema for complete PackagingType data in API responses."""

    pass


class HardwareBase(BaseModel):
    """Base schema for Hardware data.

    Attributes:
        name: Hardware item name.
        description: Description of the hardware item.
        part_number: Manufacturer part number.
    """

    name: str = Field(..., description="Hardware item name")
    description: Optional[str] = Field(None, description="Hardware item description")
    part_number: Optional[str] = Field(None, description="Manufacturer part number")


class HardwareCreate(HardwareBase):
    """Schema for creating a new Hardware."""

    pass


class HardwareUpdate(BaseModel):
    """Schema for updating an existing Hardware.

    All fields are optional to allow partial updates.
    """

    name: Optional[str] = Field(None, description="Hardware item name")
    description: Optional[str] = Field(None, description="Hardware item description")
    part_number: Optional[str] = Field(None, description="Manufacturer part number")


class HardwareInDB(HardwareBase):
    """Schema for Hardware data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = ConfigDict(from_attributes=True)


class Hardware(HardwareInDB):
    """Schema for complete Hardware data in API responses."""

    pass


class TariffCodeBase(BaseModel):
    """Base schema for TariffCode data.

    Attributes:
        code: Tariff code number.
        description: Description of the tariff code.
        country_id: ID of the country this tariff applies to.
    """

    code: str = Field(..., description="Tariff code number")
    description: str = Field(..., description="Tariff code description")
    country_id: Optional[uuid.UUID] = Field(None, description="Country ID")


class TariffCodeCreate(TariffCodeBase):
    """Schema for creating a new TariffCode."""

    pass


class TariffCodeUpdate(BaseModel):
    """Schema for updating an existing TariffCode.

    All fields are optional to allow partial updates.
    """

    code: Optional[str] = Field(None, description="Tariff code number")
    description: Optional[str] = Field(None, description="Tariff code description")
    country_id: Optional[uuid.UUID] = Field(None, description="Country ID")


class TariffCodeInDB(TariffCodeBase):
    """Schema for TariffCode data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = ConfigDict(from_attributes=True)


class TariffCode(TariffCodeInDB):
    """Schema for complete TariffCode data in API responses.

    Includes related entities like country details.
    """

    country: Optional[Dict[str, Any]] = Field(None, description="Country details")


class UnspscCodeBase(BaseModel):
    """Base schema for UnspscCode data.

    Attributes:
        code: UNSPSC code number.
        description: Description of the code.
        segment: Segment description.
        family: Family description.
        class_: Class description.
        commodity: Commodity description.
    """

    code: str = Field(..., description="UNSPSC code number")
    description: str = Field(..., description="UNSPSC code description")
    segment: Optional[str] = Field(None, description="Segment description")
    family: Optional[str] = Field(None, description="Family description")
    class_: Optional[str] = Field(None, description="Class description")
    commodity: Optional[str] = Field(None, description="Commodity description")


class UnspscCodeCreate(UnspscCodeBase):
    """Schema for creating a new UnspscCode."""

    pass


class UnspscCodeUpdate(BaseModel):
    """Schema for updating an existing UnspscCode.

    All fields are optional to allow partial updates.
    """

    code: Optional[str] = Field(None, description="UNSPSC code number")
    description: Optional[str] = Field(None, description="UNSPSC code description")
    segment: Optional[str] = Field(None, description="Segment description")
    family: Optional[str] = Field(None, description="Family description")
    class_: Optional[str] = Field(None, description="Class description")
    commodity: Optional[str] = Field(None, description="Commodity description")


class UnspscCodeInDB(UnspscCodeBase):
    """Schema for UnspscCode data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = ConfigDict(from_attributes=True)


class UnspscCode(UnspscCodeInDB):
    """Schema for complete UnspscCode data in API responses."""

    pass


class WarehouseBase(BaseModel):
    """Base schema for Warehouse data.

    Attributes:
        name: Warehouse name.
        address_id: ID of the warehouse address.
        is_active: Whether the warehouse is active.
    """

    name: str = Field(..., description="Warehouse name")
    address_id: Optional[uuid.UUID] = Field(None, description="Address ID")
    is_active: bool = Field(True, description="Whether the warehouse is active")


class WarehouseCreate(WarehouseBase):
    """Schema for creating a new Warehouse."""

    pass


class WarehouseUpdate(BaseModel):
    """Schema for updating an existing Warehouse.

    All fields are optional to allow partial updates.
    """

    name: Optional[str] = Field(None, description="Warehouse name")
    address_id: Optional[uuid.UUID] = Field(None, description="Address ID")
    is_active: Optional[bool] = Field(
        None, description="Whether the warehouse is active"
    )


class WarehouseInDB(WarehouseBase):
    """Schema for Warehouse data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = ConfigDict(from_attributes=True)


class Warehouse(WarehouseInDB):
    """Schema for complete Warehouse data in API responses.

    Includes related entities like address details.
    """

    address: Optional[Dict[str, Any]] = Field(None, description="Address details")
