# backend/app/data_import/__init__.py
from __future__ import annotations

"""
Data import package for the application.

This package provides functionality for importing data from external sources
into the application database, including connectors for different data sources,
processors for transforming data, and importers for loading data.
"""

from app.db.base import Base

from app.data_import.field_definitions import (
    ENTITY_FIELD_DEFINITIONS,
    COMPLEX_FIELD_MAPPINGS,
    EntityFieldDefinitions,
    FieldDefinition,
    FieldType,
)
from app.data_import.processors.processor_factory import (
    create_processor,
    ProcessorFactory,
    EntityType,
    SourceType,
)

__all__ = [
    "ENTITY_FIELD_DEFINITIONS",
    "COMPLEX_FIELD_MAPPINGS",
    "EntityFieldDefinitions",
    "FieldDefinition",
    "FieldType",
    "create_processor",
    "ProcessorFactory",
    "EntityType",
    "SourceType",
]
