from __future__ import annotations
'Compliance schema definitions.\n\nThis module defines Pydantic schemas for compliance-related objects,\nincluding Prop65 chemicals, warnings, and hazardous materials.\n'
import uuid
from datetime import date, datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.domains.compliance.models import ChemicalType, ExposureScenario, ApprovalStatus, TransportRestriction
class Prop65ChemicalBase(BaseModel):
    name: str = Field(..., description='Chemical name')
    cas_number: str = Field(..., description='CAS Registry Number')
    type: ChemicalType = Field(..., description='Type of chemical hazard')
    exposure_limit: Optional[float] = Field(None, description='Safe harbor exposure limit')
class Prop65ChemicalCreate(Prop65ChemicalBase):
    pass
class Prop65ChemicalUpdate(BaseModel):
    name: Optional[str] = Field(None, description='Chemical name')
    cas_number: Optional[str] = Field(None, description='CAS Registry Number')
    type: Optional[ChemicalType] = Field(None, description='Type of chemical hazard')
    exposure_limit: Optional[float] = Field(None, description='Safe harbor exposure limit')
class Prop65ChemicalInDB(Prop65ChemicalBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    updated_at: datetime = Field(..., description='Last update timestamp')
    model_config = ConfigDict(from_attributes=True)
class Prop65Chemical(Prop65ChemicalInDB):
    pass
class WarningBase(BaseModel):
    product_id: uuid.UUID = Field(..., description='Product ID')
    chemical_id: uuid.UUID = Field(..., description='Chemical ID')
    warning_text: str = Field(..., description='Warning label text')
class WarningCreate(WarningBase):
    pass
class WarningUpdate(BaseModel):
    warning_text: Optional[str] = Field(None, description='Warning label text')
class WarningInDB(WarningBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    last_updated: datetime = Field(..., description='Last update timestamp')
    model_config = ConfigDict(from_attributes=True)
class Warning(WarningInDB):
    chemical: Optional[Prop65Chemical] = Field(None, description='Chemical details')
    product: Optional[Dict[str, Any]] = Field(None, description='Product details')
class ProductChemicalBase(BaseModel):
    product_id: uuid.UUID = Field(..., description='Product ID')
    chemical_id: uuid.UUID = Field(..., description='Chemical ID')
    exposure_scenario: ExposureScenario = Field(..., description='Type of exposure scenario')
    warning_required: bool = Field(False, description='Whether a warning label is required')
    warning_label: Optional[str] = Field(None, description='Warning label text if required')
class ProductChemicalCreate(ProductChemicalBase):
    pass
class ProductChemicalUpdate(BaseModel):
    exposure_scenario: Optional[ExposureScenario] = Field(None, description='Type of exposure scenario')
    warning_required: Optional[bool] = Field(None, description='Whether a warning label is required')
    warning_label: Optional[str] = Field(None, description='Warning label text if required')
class ProductChemicalInDB(ProductChemicalBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    model_config = ConfigDict(from_attributes=True)
class ProductChemical(ProductChemicalInDB):
    chemical: Optional[Prop65Chemical] = Field(None, description='Chemical details')
    product: Optional[Dict[str, Any]] = Field(None, description='Product details')
class ProductDOTApprovalBase(BaseModel):
    product_id: uuid.UUID = Field(..., description='Product ID')
    approval_status: ApprovalStatus = Field(..., description='Approval status')
    approval_number: Optional[str] = Field(None, description='DOT approval number')
    approved_by: Optional[str] = Field(None, description='Name of approver')
    approval_date: Optional[date] = Field(None, description='Date of approval')
    expiration_date: Optional[date] = Field(None, description='Expiration date')
    reason: Optional[str] = Field(None, description='Reason for status')
class ProductDOTApprovalCreate(ProductDOTApprovalBase):
    pass
class ProductDOTApprovalUpdate(BaseModel):
    approval_status: Optional[ApprovalStatus] = Field(None, description='Approval status')
    approval_number: Optional[str] = Field(None, description='DOT approval number')
    approved_by: Optional[str] = Field(None, description='Name of approver')
    approval_date: Optional[date] = Field(None, description='Date of approval')
    expiration_date: Optional[date] = Field(None, description='Expiration date')
    reason: Optional[str] = Field(None, description='Reason for status')
class ProductDOTApprovalInDB(ProductDOTApprovalBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    changed_by_id: Optional[uuid.UUID] = Field(None, description='User who changed the approval')
    changed_at: datetime = Field(..., description='When the approval was changed')
    model_config = ConfigDict(from_attributes=True)
class ProductDOTApproval(ProductDOTApprovalInDB):
    product: Optional[Dict[str, Any]] = Field(None, description='Product details')
    changed_by: Optional[Dict[str, Any]] = Field(None, description='User who changed the approval')
class HazardousMaterialBase(BaseModel):
    product_id: uuid.UUID = Field(..., description='Product ID')
    un_number: Optional[str] = Field(None, description='UN number')
    hazard_class: Optional[str] = Field(None, description='DOT hazard class')
    packing_group: Optional[str] = Field(None, description='Packing group')
    handling_instructions: Optional[str] = Field(None, description='Handling instructions')
    restricted_transport: TransportRestriction = Field(TransportRestriction.NONE, description='Transport restrictions')
class HazardousMaterialCreate(HazardousMaterialBase):
    pass
class HazardousMaterialUpdate(BaseModel):
    un_number: Optional[str] = Field(None, description='UN number')
    hazard_class: Optional[str] = Field(None, description='DOT hazard class')
    packing_group: Optional[str] = Field(None, description='Packing group')
    handling_instructions: Optional[str] = Field(None, description='Handling instructions')
    restricted_transport: Optional[TransportRestriction] = Field(None, description='Transport restrictions')
class HazardousMaterialInDB(HazardousMaterialBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    created_at: datetime = Field(..., description='Creation timestamp')
    model_config = ConfigDict(from_attributes=True)
class HazardousMaterial(HazardousMaterialInDB):
    product: Optional[Dict[str, Any]] = Field(None, description='Product details')