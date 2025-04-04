from __future__ import annotations
'Company schema definitions.\n\nThis module defines Pydantic schemas for Company objects,\nincluding creation, update, and response models.\n'
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.domains.location.schemas import Address
class CompanyBase(BaseModel):
    name: str = Field(..., description='Name of the company')
    account_number: Optional[str] = Field(None, description='Unique account identifier')
    account_type: str = Field(..., description='Type of account (client, supplier, etc)')
    industry: Optional[str] = Field(None, description='Industry sector')
    is_active: bool = Field(True, description='Whether the company is active')
class CompanyCreate(CompanyBase):
    pass
class CompanyUpdate(BaseModel):
    name: Optional[str] = Field(None, description='Name of the company')
    account_number: Optional[str] = Field(None, description='Unique account identifier')
    account_type: Optional[str] = Field(None, description='Type of account')
    industry: Optional[str] = Field(None, description='Industry sector')
    is_active: Optional[bool] = Field(None, description='Whether the company is active')
    headquarters_address_id: Optional[uuid.UUID] = Field(None, description='ID of headquarters address')
    billing_address_id: Optional[uuid.UUID] = Field(None, description='ID of billing address')
    shipping_address_id: Optional[uuid.UUID] = Field(None, description='ID of shipping address')
class CompanyInDB(CompanyBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    created_at: datetime = Field(..., description='Creation timestamp')
    updated_at: datetime = Field(..., description='Last update timestamp')
    headquarters_address_id: Optional[uuid.UUID] = Field(None, description='ID of headquarters address')
    billing_address_id: Optional[uuid.UUID] = Field(None, description='ID of billing address')
    shipping_address_id: Optional[uuid.UUID] = Field(None, description='ID of shipping address')
    model_config = ConfigDict(from_attributes=True)
class Company(CompanyInDB):
    headquarters_address: Optional[Address] = Field(None, description='Headquarters address details')
    billing_address: Optional[Address] = Field(None, description='Billing address details')
    shipping_address: Optional[Address] = Field(None, description='Shipping address details')