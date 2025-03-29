from __future__ import annotations
'Autocare domain schemas.\n\nThis module defines Pydantic schemas for the main Autocare domain functionality.\nThese schemas are used for validation and serialization across the autocare sub-domains.\n'
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator
class FileFormat(str, Enum):
    ACES_XML = 'aces_xml'
    PIES_XML = 'pies_xml'
    CSV = 'csv'
    EXCEL = 'excel'
    JSON = 'json'
class ImportMode(str, Enum):
    REPLACE = 'replace'
    MERGE = 'merge'
    UPDATE = 'update'
    INSERT = 'insert'
class DataType(str, Enum):
    VEHICLES = 'vehicles'
    PARTS = 'parts'
    FITMENTS = 'fitments'
    ALL = 'all'
class AutocareImportParams(BaseModel):
    file_path: str = Field(..., description='Path to the import file')
    format: FileFormat = Field(..., description='Format of the import file')
    mode: ImportMode = Field(ImportMode.MERGE, description='Import mode')
    data_type: DataType = Field(DataType.ALL, description='Type of data to import')
    validate: bool = Field(True, description='Whether to validate data before import')
    options: Optional[Dict[str, Any]] = Field(None, description='Additional import options')
class AutocareExportParams(BaseModel):
    file_path: str = Field(..., description='Path to the export file')
    format: FileFormat = Field(..., description='Format of the export file')
    data_type: DataType = Field(DataType.ALL, description='Type of data to export')
    filters: Optional[Dict[str, Any]] = Field(None, description='Filters to apply to the data')
    options: Optional[Dict[str, Any]] = Field(None, description='Additional export options')
class FitmentSearchParams(BaseModel):
    year: Optional[int] = Field(None, description='Vehicle year')
    make: Optional[str] = Field(None, description='Vehicle make')
    model: Optional[str] = Field(None, description='Vehicle model')
    submodel: Optional[str] = Field(None, description='Vehicle submodel')
    part_number: Optional[str] = Field(None, description='Part number')
    part_type: Optional[str] = Field(None, description='Part type')
    brand: Optional[str] = Field(None, description='Brand')
    page: int = Field(1, description='Page number', ge=1)
    page_size: int = Field(20, description='Page size', ge=1, le=100)
    @model_validator(mode='after')
    def validate_search_criteria(self) -> 'FitmentSearchParams':
        criteria = [self.year, self.make, self.model, self.submodel, self.part_number, self.part_type, self.brand]
        if not any(criteria):
            raise ValueError('At least one search criterion must be provided')
        return self
class PaginatedResponse(BaseModel):
    items: List[Any] = Field(..., description='List of items')
    total: int = Field(..., description='Total number of items')
    page: int = Field(..., description='Current page number')
    page_size: int = Field(..., description='Number of items per page')
    pages: int = Field(..., description='Total number of pages')
    model_config = ConfigDict(from_attributes=True)