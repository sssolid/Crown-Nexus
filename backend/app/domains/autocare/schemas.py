from __future__ import annotations

"""Autocare domain schemas.

This module defines Pydantic schemas for the main Autocare domain functionality.
These schemas are used for validation and serialization across the autocare sub-domains.
"""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FileFormat(str, Enum):
    """File formats for import and export operations.

    Attributes:
        ACES_XML: ACES XML format
        PIES_XML: PIES XML format
        CSV: Comma-separated values
        EXCEL: Microsoft Excel format
        JSON: JSON format
    """

    ACES_XML = "aces_xml"
    PIES_XML = "pies_xml"
    CSV = "csv"
    EXCEL = "excel"
    JSON = "json"


class ImportMode(str, Enum):
    """Import modes for data ingestion.

    Attributes:
        REPLACE: Replace existing data
        MERGE: Merge with existing data
        UPDATE: Update existing data only
        INSERT: Insert new data only
    """

    REPLACE = "replace"
    MERGE = "merge"
    UPDATE = "update"
    INSERT = "insert"


class DataType(str, Enum):
    """Types of data to import or export.

    Attributes:
        VEHICLES: Vehicle data
        PARTS: Part data
        FITMENTS: Fitment mapping data
        ALL: All data types
    """

    VEHICLES = "vehicles"
    PARTS = "parts"
    FITMENTS = "fitments"
    ALL = "all"


class AutocareImportParams(BaseModel):
    """Parameters for importing data.

    Attributes:
        file_path: Path to the import file
        format: Format of the import file
        mode: Import mode
        data_type: Type of data to import
        validate: Whether to validate data before import
        options: Additional import options
    """

    file_path: str = Field(..., description="Path to the import file")
    format: FileFormat = Field(..., description="Format of the import file")
    mode: ImportMode = Field(ImportMode.MERGE, description="Import mode")
    data_type: DataType = Field(DataType.ALL, description="Type of data to import")
    validate: bool = Field(True, description="Whether to validate data before import")
    options: Optional[Dict[str, Any]] = Field(
        None, description="Additional import options"
    )


class AutocareExportParams(BaseModel):
    """Parameters for exporting data.

    Attributes:
        file_path: Path to the export file
        format: Format of the export file
        data_type: Type of data to export
        filters: Filters to apply to the data
        options: Additional export options
    """

    file_path: str = Field(..., description="Path to the export file")
    format: FileFormat = Field(..., description="Format of the export file")
    data_type: DataType = Field(DataType.ALL, description="Type of data to export")
    filters: Optional[Dict[str, Any]] = Field(
        None, description="Filters to apply to the data"
    )
    options: Optional[Dict[str, Any]] = Field(
        None, description="Additional export options"
    )


class FitmentSearchParams(BaseModel):
    """Parameters for searching fitment data.

    Attributes:
        year: Vehicle year
        make: Vehicle make
        model: Vehicle model
        submodel: Vehicle submodel
        part_number: Part number
        part_type: Part type
        brand: Brand
        page: Page number
        page_size: Page size
    """

    year: Optional[int] = Field(None, description="Vehicle year")
    make: Optional[str] = Field(None, description="Vehicle make")
    model: Optional[str] = Field(None, description="Vehicle model")
    submodel: Optional[str] = Field(None, description="Vehicle submodel")
    part_number: Optional[str] = Field(None, description="Part number")
    part_type: Optional[str] = Field(None, description="Part type")
    brand: Optional[str] = Field(None, description="Brand")
    page: int = Field(1, description="Page number", ge=1)
    page_size: int = Field(20, description="Page size", ge=1, le=100)

    @model_validator(mode="after")
    def validate_search_criteria(self) -> "FitmentSearchParams":
        """Validate that at least one search criterion is provided.

        Returns:
            The validated model

        Raises:
            ValueError: If no search criteria are provided
        """
        criteria = [
            self.year,
            self.make,
            self.model,
            self.submodel,
            self.part_number,
            self.part_type,
            self.brand,
        ]

        if not any(criteria):
            raise ValueError("At least one search criterion must be provided")

        return self


class PaginatedResponse(BaseModel):
    """Base schema for paginated responses.

    Attributes:
        items: List of items
        total: Total number of items
        page: Current page number
        page_size: Number of items per page
        pages: Total number of pages
    """

    items: List[Any] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    pages: int = Field(..., description="Total number of pages")

    model_config = ConfigDict(from_attributes=True)
