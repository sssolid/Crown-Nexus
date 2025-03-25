from __future__ import annotations

"""Qdb schema definitions.

This module defines Pydantic schemas for qualifier-related objects,
including qualifiers, translations, and groupings.
"""

import uuid
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class QualifierType(BaseModel):
    """Schema for qualifier type data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    qualifier_type_id: int = Field(..., description="Qualifier type ID from Qdb")
    qualifier_type: Optional[str] = Field(None, description="Qualifier type name")

    model_config = ConfigDict(from_attributes=True)


class Language(BaseModel):
    """Schema for language data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    language_id: int = Field(..., description="Language ID from Qdb")
    language_name: Optional[str] = Field(None, description="Language name")
    dialect_name: Optional[str] = Field(None, description="Dialect name")

    model_config = ConfigDict(from_attributes=True)


class QualifierTranslation(BaseModel):
    """Schema for qualifier translation data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    qualifier_translation_id: int = Field(..., description="Translation ID from Qdb")
    qualifier_id: int = Field(..., description="Qualifier ID")
    language_id: int = Field(..., description="Language ID")
    translation_text: str = Field(..., description="Translation text")

    language: Optional[Dict[str, Any]] = Field(None, description="Language details")

    model_config = ConfigDict(from_attributes=True)


class GroupNumber(BaseModel):
    """Schema for group number data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    group_number_id: int = Field(..., description="Group number ID from Qdb")
    group_description: str = Field(..., description="Group description")

    model_config = ConfigDict(from_attributes=True)


class QualifierGroup(BaseModel):
    """Schema for qualifier group data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    qualifier_group_id: int = Field(..., description="Qualifier group ID from Qdb")
    group_number_id: int = Field(..., description="Group number ID")
    qualifier_id: int = Field(..., description="Qualifier ID")

    number: Optional[Dict[str, Any]] = Field(None, description="Group number details")

    model_config = ConfigDict(from_attributes=True)


class Qualifier(BaseModel):
    """Schema for qualifier data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    qualifier_id: int = Field(..., description="Qualifier ID from Qdb")
    qualifier_text: Optional[str] = Field(None, description="Qualifier text")
    example_text: Optional[str] = Field(None, description="Example text")
    qualifier_type_id: int = Field(..., description="Qualifier type ID")
    new_qualifier_id: Optional[int] = Field(
        None, description="ID of superseding qualifier"
    )

    model_config = ConfigDict(from_attributes=True)


class QualifierDetail(Qualifier):
    """Schema for detailed qualifier data."""

    type: Dict[str, Any] = Field(..., description="Qualifier type details")
    translations: List[Dict[str, Any]] = Field([], description="Translations")
    groups: List[Dict[str, Any]] = Field([], description="Group assignments")
    superseded_by: Optional[Dict[str, Any]] = Field(
        None, description="Superseding qualifier details"
    )
    when_modified: str = Field(..., description="Modification timestamp")

    model_config = ConfigDict(from_attributes=True)


class QualifierSearchParameters(BaseModel):
    """Schema for qualifier search parameters."""

    search_term: str = Field(..., description="Search term")
    qualifier_type_id: Optional[int] = Field(
        None, description="Filter by qualifier type ID"
    )
    language_id: Optional[int] = Field(
        None, description="Search in translations for this language"
    )
    page: int = Field(1, description="Page number", ge=1)
    page_size: int = Field(20, description="Page size", ge=1, le=100)


class QualifierSearchResponse(BaseModel):
    """Schema for paginated qualifier search response."""

    items: List[Qualifier] = Field(..., description="List of qualifiers")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    pages: int = Field(..., description="Total number of pages")
