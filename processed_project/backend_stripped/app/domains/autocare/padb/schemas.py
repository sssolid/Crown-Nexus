from __future__ import annotations
'PAdb schema definitions.\n\nThis module defines Pydantic schemas for part attribute-related objects,\nincluding attributes, metadata, and value constraints.\n'
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
class PartAttribute(BaseModel):
    id: uuid.UUID = Field(..., description='Unique identifier')
    pa_id: int = Field(..., description='Part attribute ID from PAdb')
    pa_name: Optional[str] = Field(None, description='Attribute name')
    pa_descr: Optional[str] = Field(None, description='Attribute description')
    model_config = ConfigDict(from_attributes=True)
class MetaData(BaseModel):
    id: uuid.UUID = Field(..., description='Unique identifier')
    meta_id: int = Field(..., description='Metadata ID from PAdb')
    meta_name: Optional[str] = Field(None, description='Metadata name')
    meta_descr: Optional[str] = Field(None, description='Metadata description')
    meta_format: Optional[str] = Field(None, description='Metadata format')
    data_type: Optional[str] = Field(None, description='Data type')
    min_length: Optional[int] = Field(None, description='Minimum length')
    max_length: Optional[int] = Field(None, description='Maximum length')
    model_config = ConfigDict(from_attributes=True)
class MeasurementGroup(BaseModel):
    id: uuid.UUID = Field(..., description='Unique identifier')
    measurement_group_id: int = Field(..., description='Measurement group ID from PAdb')
    measurement_group_name: Optional[str] = Field(None, description='Measurement group name')
    model_config = ConfigDict(from_attributes=True)
class MetaUOMCode(BaseModel):
    id: uuid.UUID = Field(..., description='Unique identifier')
    meta_uom_id: int = Field(..., description='UOM code ID from PAdb')
    uom_code: Optional[str] = Field(None, description='UOM code')
    uom_description: Optional[str] = Field(None, description='UOM description')
    uom_label: Optional[str] = Field(None, description='UOM label')
    measurement_group_id: int = Field(..., description='Measurement group ID')
    model_config = ConfigDict(from_attributes=True)
class ValidValue(BaseModel):
    id: uuid.UUID = Field(..., description='Unique identifier')
    valid_value_id: int = Field(..., description='Valid value ID from PAdb')
    valid_value: str = Field(..., description='Valid value text')
    model_config = ConfigDict(from_attributes=True)
class PartAttributeAssignment(BaseModel):
    id: uuid.UUID = Field(..., description='Unique identifier')
    papt_id: int = Field(..., description='Assignment ID from PAdb')
    part_terminology_id: int = Field(..., description='Part terminology ID')
    pa_id: int = Field(..., description='Part attribute ID')
    meta_id: int = Field(..., description='Metadata ID')
    attribute: Optional[PartAttribute] = Field(None, description='Attribute details')
    metadata: Optional[MetaData] = Field(None, description='Metadata details')
    model_config = ConfigDict(from_attributes=True)
class AttributeWithMetadata(BaseModel):
    assignment_id: int = Field(..., description='Assignment ID')
    attribute: Dict[str, Any] = Field(..., description='Attribute details')
    metadata: Dict[str, Any] = Field(..., description='Metadata details')
    valid_values: List[Dict[str, Any]] = Field([], description='Valid values')
    uom_codes: List[Dict[str, Any]] = Field([], description='UOM codes')
    model_config = ConfigDict(from_attributes=True)
class PartAttributeDetail(BaseModel):
    id: uuid.UUID = Field(..., description='Unique identifier')
    pa_id: int = Field(..., description='Part attribute ID from PAdb')
    name: Optional[str] = Field(None, description='Attribute name')
    description: Optional[str] = Field(None, description='Attribute description')
    metadata_assignments: List[Dict[str, Any]] = Field([], description='Metadata assignments')
    model_config = ConfigDict(from_attributes=True)
class PartAttributesResponse(BaseModel):
    part_terminology_id: int = Field(..., description='Part terminology ID')
    attributes: List[AttributeWithMetadata] = Field([], description='Attributes with metadata')
    model_config = ConfigDict(from_attributes=True)
class AttributeSearchParameters(BaseModel):
    search_term: str = Field(..., description='Search term')
    page: int = Field(1, description='Page number', ge=1)
    page_size: int = Field(20, description='Page size', ge=1, le=100)
class AttributeSearchResponse(BaseModel):
    items: List[PartAttribute] = Field(..., description='List of attributes')
    total: int = Field(..., description='Total number of items')
    page: int = Field(..., description='Current page number')
    page_size: int = Field(..., description='Number of items per page')
    pages: int = Field(..., description='Total number of pages')