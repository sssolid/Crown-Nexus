# app/domains/autocare/importers/qdb_importer.py
from __future__ import annotations

"""
Qdb (Qualifier Database) data importer.

This module provides a specialized importer for Qdb data from various formats,
mapping external data to the correct database models with proper transformations.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.autocare.importers.flexible_importer import FlexibleImporter, SourceFormat, detect_source_format
from app.domains.autocare.qdb.models import (
    QualifierType, Qualifier, Language,
    QualifierTranslation, GroupNumber,
    QualifierGroup, QdbVersion
)
from app.logging import get_logger

logger = get_logger("app.domains.autocare.importers.qdb_importer")


class QdbImporter(FlexibleImporter):
    """Importer for Qdb (Qualifier Database) data from various formats."""

    def __init__(
        self,
        db: AsyncSession,
        source_path: Path,
        source_format: Optional[SourceFormat] = None,
        batch_size: int = 1000
    ):
        """
        Initialize QdbImporter.

        Args:
            db: Database session
            source_path: Path to source files directory
            source_format: Format of the source data (auto-detected if None)
            batch_size: Batch size for imports
        """
        # Auto-detect format if not specified
        if source_format is None:
            source_format = detect_source_format(source_path)
            logger.info(f"Auto-detected source format: {source_format.value}")

        # Define file extensions based on source format
        file_ext = ".json" if source_format == SourceFormat.JSON else ".txt"

        # Define required files for minimal import
        required_sources = [
            f"Version{file_ext}",
            f"QualifierType{file_ext}",
            f"Qualifier{file_ext}",
        ]

        super().__init__(
            db=db,
            source_path=source_path,
            schema_name="qdb",
            required_sources=required_sources,
            version_class=QdbVersion,
            source_format=source_format,
            version_date_field="version_date",
            batch_size=batch_size,
        )

        # Register all table mappings
        self._register_mappings()

        # Define import order for referential integrity
        self.set_import_order([
            f"QualifierType{file_ext}",
            f"Qualifier{file_ext}",
            f"Language{file_ext}",
            f"QualifierTranslation{file_ext}",
            f"GroupNumber{file_ext}",
            f"QualifierGroup{file_ext}",
        ])

    def _register_mappings(self) -> None:
        """Register all table mappings for Qdb imports."""
        # Get the file extension based on source format
        file_ext = ".json" if self.source_format == SourceFormat.JSON else ".txt"

        # QualifierType
        self.register_table_mapping(
            source_name=f"QualifierType{file_ext}",
            model_class=QualifierType,
            field_mapping={
                "qualifier_type_id": "QualifierTypeId",
                "qualifier_type": "QualifierType",
            },
            primary_key="qualifier_type_id",
            transformers={
                "qualifier_type_id": lambda x: int(x) if x else None,
            },
        )

        # Qualifier
        self.register_table_mapping(
            source_name=f"Qualifier{file_ext}",
            model_class=Qualifier,
            field_mapping={
                "qualifier_id": "QualifierId",
                "qualifier_text": "QualifierText",
                "example_text": "ExampleText",
                "qualifier_type_id": "QualifierTypeId",
                "new_qualifier_id": "NewQualifierId",
                "when_modified": "WhenModified",
            },
            primary_key="qualifier_id",
            transformers={
                "qualifier_id": lambda x: int(x) if x else None,
                "qualifier_type_id": lambda x: int(x) if x else None,
                "new_qualifier_id": lambda x: int(x) if x and x.strip() else None,
                "when_modified": lambda x: datetime.strptime(x, "%Y%m%d%H%M%S") if x and x.strip() else datetime.now(),
            },
        )

        # Language
        self.register_table_mapping(
            source_name=f"Language{file_ext}",
            model_class=Language,
            field_mapping={
                "language_id": "LanguageId",
                "language_name": "LanguageName",
                "dialect_name": "DialectName",
            },
            primary_key="language_id",
            transformers={
                "language_id": lambda x: int(x) if x else None,
            },
        )

        # QualifierTranslation
        self.register_table_mapping(
            source_name=f"QualifierTranslation{file_ext}",
            model_class=QualifierTranslation,
            field_mapping={
                "qualifier_translation_id": "QualifierTranslationId",
                "qualifier_id": "QualifierId",
                "language_id": "LanguageId",
                "translation_text": "TranslationText",
            },
            primary_key="qualifier_translation_id",
            transformers={
                "qualifier_translation_id": lambda x: int(x) if x else None,
                "qualifier_id": lambda x: int(x) if x else None,
                "language_id": lambda x: int(x) if x else None,
            },
        )

        # GroupNumber
        self.register_table_mapping(
            source_name=f"GroupNumber{file_ext}",
            model_class=GroupNumber,
            field_mapping={
                "group_number_id": "GroupNumberId",
                "group_description": "GroupDescription",
            },
            primary_key="group_number_id",
            transformers={
                "group_number_id": lambda x: int(x) if x else None,
            },
        )

        # QualifierGroup
        self.register_table_mapping(
            source_name=f"QualifierGroup{file_ext}",
            model_class=QualifierGroup,
            field_mapping={
                "qualifier_group_id": "QualifierGroupId",
                "group_number_id": "GroupNumberId",
                "qualifier_id": "QualifierId",
            },
            primary_key="qualifier_group_id",
            transformers={
                "qualifier_group_id": lambda x: int(x) if x else None,
                "group_number_id": lambda x: int(x) if x else None,
                "qualifier_id": lambda x: int(x) if x else None,
            },
        )
