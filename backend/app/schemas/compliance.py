from __future__ import annotations

"""Compliance schema definitions.

This module defines Pydantic schemas for compliance-related objects,
including Prop65 chemicals, warnings, and hazardous materials.
"""

import uuid
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.compliance import (
    ChemicalType,
    ExposureScenario,
    ApprovalStatus,
    TransportRestriction,
)


class Prop65ChemicalBase(BaseModel):
    """Base schema for Prop65Chemical data.

    Attributes:
        name: Chemical name.
        cas_number: CAS Registry Number (unique chemical identifier).
        type: Type of chemical hazard.
        exposure_limit: Safe harbor exposure limit if applicable.
    """

    name: str = Field(..., description="Chemical name")
    cas_number: str = Field(..., description="CAS Registry Number")
    type: ChemicalType = Field(..., description="Type of chemical hazard")
    exposure_limit: Optional[float] = Field(
        None, description="Safe harbor exposure limit"
    )


class Prop65ChemicalCreate(Prop65ChemicalBase):
    """Schema for creating a new Prop65Chemical."""

    pass


class Prop65ChemicalUpdate(BaseModel):
    """Schema for updating an existing Prop65Chemical.

    All fields are optional to allow partial updates.
    """

    name: Optional[str] = Field(None, description="Chemical name")
    cas_number: Optional[str] = Field(None, description="CAS Registry Number")
    type: Optional[ChemicalType] = Field(None, description="Type of chemical hazard")
    exposure_limit: Optional[float] = Field(
        None, description="Safe harbor exposure limit"
    )


class Prop65ChemicalInDB(Prop65ChemicalBase):
    """Schema for Prop65Chemical data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class Prop65Chemical(Prop65ChemicalInDB):
    """Schema for complete Prop65Chemical data in API responses."""

    pass


class WarningBase(BaseModel):
    """Base schema for Warning data.

    Attributes:
        product_id: ID of the product requiring the warning.
        chemical_id: ID of the chemical in the warning.
        warning_text: Text of the warning label.
    """

    product_id: uuid.UUID = Field(..., description="Product ID")
    chemical_id: uuid.UUID = Field(..., description="Chemical ID")
    warning_text: str = Field(..., description="Warning label text")


class WarningCreate(WarningBase):
    """Schema for creating a new Warning."""

    pass


class WarningUpdate(BaseModel):
    """Schema for updating an existing Warning.

    All fields are optional to allow partial updates.
    """

    warning_text: Optional[str] = Field(None, description="Warning label text")


class WarningInDB(WarningBase):
    """Schema for Warning data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    last_updated: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class Warning(WarningInDB):
    """Schema for complete Warning data in API responses.

    Includes related entities like chemical and product details.
    """

    chemical: Optional[Prop65Chemical] = Field(None, description="Chemical details")
    product: Optional[Dict[str, Any]] = Field(None, description="Product details")


class ProductChemicalBase(BaseModel):
    """Base schema for ProductChemical data.

    Attributes:
        product_id: ID of the product containing the chemical.
        chemical_id: ID of the chemical in the product.
        exposure_scenario: Type of exposure scenario.
        warning_required: Whether a warning label is required.
        warning_label: Text of the required warning label if applicable.
    """

    product_id: uuid.UUID = Field(..., description="Product ID")
    chemical_id: uuid.UUID = Field(..., description="Chemical ID")
    exposure_scenario: ExposureScenario = Field(
        ..., description="Type of exposure scenario"
    )
    warning_required: bool = Field(
        False, description="Whether a warning label is required"
    )
    warning_label: Optional[str] = Field(
        None, description="Warning label text if required"
    )


class ProductChemicalCreate(ProductChemicalBase):
    """Schema for creating a new ProductChemical."""

    pass


class ProductChemicalUpdate(BaseModel):
    """Schema for updating an existing ProductChemical.

    All fields are optional to allow partial updates.
    """

    exposure_scenario: Optional[ExposureScenario] = Field(
        None, description="Type of exposure scenario"
    )
    warning_required: Optional[bool] = Field(
        None, description="Whether a warning label is required"
    )
    warning_label: Optional[str] = Field(
        None, description="Warning label text if required"
    )


class ProductChemicalInDB(ProductChemicalBase):
    """Schema for ProductChemical data as stored in the database.

    Includes database-specific fields like ID.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")

    model_config = ConfigDict(from_attributes=True)


class ProductChemical(ProductChemicalInDB):
    """Schema for complete ProductChemical data in API responses.

    Includes related entities like chemical and product details.
    """

    chemical: Optional[Prop65Chemical] = Field(None, description="Chemical details")
    product: Optional[Dict[str, Any]] = Field(None, description="Product details")


class ProductDOTApprovalBase(BaseModel):
    """Base schema for ProductDOTApproval data.

    Attributes:
        product_id: ID of the approved product.
        approval_status: Status of the approval.
        approval_number: DOT approval number if applicable.
        approved_by: Name of the approver.
        approval_date: Date of approval.
        expiration_date: Expiration date of the approval.
        reason: Reason for the approval status.
    """

    product_id: uuid.UUID = Field(..., description="Product ID")
    approval_status: ApprovalStatus = Field(..., description="Approval status")
    approval_number: Optional[str] = Field(None, description="DOT approval number")
    approved_by: Optional[str] = Field(None, description="Name of approver")
    approval_date: Optional[date] = Field(None, description="Date of approval")
    expiration_date: Optional[date] = Field(None, description="Expiration date")
    reason: Optional[str] = Field(None, description="Reason for status")


class ProductDOTApprovalCreate(ProductDOTApprovalBase):
    """Schema for creating a new ProductDOTApproval."""

    pass


class ProductDOTApprovalUpdate(BaseModel):
    """Schema for updating an existing ProductDOTApproval.

    All fields are optional to allow partial updates.
    """

    approval_status: Optional[ApprovalStatus] = Field(
        None, description="Approval status"
    )
    approval_number: Optional[str] = Field(None, description="DOT approval number")
    approved_by: Optional[str] = Field(None, description="Name of approver")
    approval_date: Optional[date] = Field(None, description="Date of approval")
    expiration_date: Optional[date] = Field(None, description="Expiration date")
    reason: Optional[str] = Field(None, description="Reason for status")


class ProductDOTApprovalInDB(ProductDOTApprovalBase):
    """Schema for ProductDOTApproval data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    changed_by_id: Optional[uuid.UUID] = Field(
        None, description="User who changed the approval"
    )
    changed_at: datetime = Field(..., description="When the approval was changed")

    model_config = ConfigDict(from_attributes=True)


class ProductDOTApproval(ProductDOTApprovalInDB):
    """Schema for complete ProductDOTApproval data in API responses.

    Includes related entities like product and user details.
    """

    product: Optional[Dict[str, Any]] = Field(None, description="Product details")
    changed_by: Optional[Dict[str, Any]] = Field(
        None, description="User who changed the approval"
    )


class HazardousMaterialBase(BaseModel):
    """Base schema for HazardousMaterial data.

    Attributes:
        product_id: ID of the hazardous product.
        un_number: UN number for hazardous material.
        hazard_class: DOT hazard class.
        packing_group: Packing group (I, II, III).
        handling_instructions: Special handling instructions.
        restricted_transport: Transport restrictions.
    """

    product_id: uuid.UUID = Field(..., description="Product ID")
    un_number: Optional[str] = Field(None, description="UN number")
    hazard_class: Optional[str] = Field(None, description="DOT hazard class")
    packing_group: Optional[str] = Field(None, description="Packing group")
    handling_instructions: Optional[str] = Field(
        None, description="Handling instructions"
    )
    restricted_transport: TransportRestriction = Field(
        TransportRestriction.NONE, description="Transport restrictions"
    )


class HazardousMaterialCreate(HazardousMaterialBase):
    """Schema for creating a new HazardousMaterial."""

    pass


class HazardousMaterialUpdate(BaseModel):
    """Schema for updating an existing HazardousMaterial.

    All fields are optional to allow partial updates.
    """

    un_number: Optional[str] = Field(None, description="UN number")
    hazard_class: Optional[str] = Field(None, description="DOT hazard class")
    packing_group: Optional[str] = Field(None, description="Packing group")
    handling_instructions: Optional[str] = Field(
        None, description="Handling instructions"
    )
    restricted_transport: Optional[TransportRestriction] = Field(
        None, description="Transport restrictions"
    )


class HazardousMaterialInDB(HazardousMaterialBase):
    """Schema for HazardousMaterial data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = ConfigDict(from_attributes=True)


class HazardousMaterial(HazardousMaterialInDB):
    """Schema for complete HazardousMaterial data in API responses.

    Includes related entities like product details.
    """

    product: Optional[Dict[str, Any]] = Field(None, description="Product details")
