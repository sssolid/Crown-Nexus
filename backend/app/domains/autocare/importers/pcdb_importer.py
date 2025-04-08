# app/domains/autocare/importers/pcdb_importer.py
from __future__ import annotations

"""
PCdb (Product Component Database) data importer.

This module provides a specialized importer for PCdb data from various formats,
mapping external data to the correct database models with proper transformations.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.autocare.importers.flexible_importer import (
    FlexibleImporter,
    SourceFormat,
    detect_source_format,
)
from app.domains.autocare.pcdb.models import (
    Alias,
    Category,
    CodeMaster,
    Parts,
    PartsDescription,
    PartCategory,
    PartPosition,
    PartsSupersession,
    PCdbVersion,
    Position,
    SubCategory,
    parts_to_alias,
    parts_to_use,
    Use,
)
from app.logging import get_logger

logger = get_logger("app.domains.autocare.importers.pcdb_importer")


class PCdbImporter(FlexibleImporter):
    """Importer for PCdb (Product Component Database) data from various formats."""

    def __init__(
        self,
        db: AsyncSession,
        source_path: Path,
        source_format: Optional[SourceFormat] = None,
        batch_size: int = 1000,
    ):
        """
        Initialize PCdbImporter.

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
            f"Parts{file_ext}",
            f"PartsDescription{file_ext}",
            f"Categories{file_ext}",
            f"Subcategories{file_ext}",
            f"Positions{file_ext}",
            f"PartCategory{file_ext}",
            f"PartPosition{file_ext}",
        ]

        super().__init__(
            db=db,
            source_path=source_path,
            schema_name="pcdb",
            required_sources=required_sources,
            version_class=PCdbVersion,
            source_format=source_format,
            version_date_field="version_date",
            batch_size=batch_size,
        )

        # Register all table mappings
        self._register_mappings()

        # Define import order for referential integrity
        self.set_import_order(
            [
                f"Categories{file_ext}",
                f"Subcategories{file_ext}",
                f"Positions{file_ext}",
                f"PartsDescription{file_ext}",
                f"Parts{file_ext}",
                f"PartCategory{file_ext}",
                f"PartPosition{file_ext}",
                f"PartsSupersession{file_ext}",
                f"Alias{file_ext}",
                f"Use{file_ext}",
                f"PartsToAlias{file_ext}",
                f"PartsToUse{file_ext}",
                f"CodeMaster{file_ext}",
            ]
        )

    def _register_mappings(self) -> None:
        """Register all table mappings for PCdb imports."""
        # Get the file extension based on source format
        file_ext = ".json" if self.source_format == SourceFormat.JSON else ".txt"

        # Categories
        self.register_table_mapping(
            source_name=f"Categories{file_ext}",
            model_class=Category,
            field_mapping={
                "category_id": "CategoryID",
                "category_name": "CategoryName",
            },
            primary_key="category_id",
            transformers={
                "category_id": lambda x: int(x) if x else None,
            },
        )

        # Subcategories
        self.register_table_mapping(
            source_name=f"Subcategories{file_ext}",
            model_class=SubCategory,
            field_mapping={
                "subcategory_id": "SubCategoryID",
                "subcategory_name": "SubCategoryName",
            },
            primary_key="subcategory_id",
            transformers={
                "subcategory_id": lambda x: int(x) if x else None,
            },
        )

        # Positions
        self.register_table_mapping(
            source_name=f"Positions{file_ext}",
            model_class=Position,
            field_mapping={
                "position_id": "PositionID",
                "position": "Position",
            },
            primary_key="position_id",
            transformers={
                "position_id": lambda x: int(x) if x else None,
            },
        )

        # Parts Description
        self.register_table_mapping(
            source_name=f"PartsDescription{file_ext}",
            model_class=PartsDescription,
            field_mapping={
                "parts_description_id": "PartsDescriptionID",
                "parts_description": "PartsDescription",
            },
            primary_key="parts_description_id",
            transformers={
                "parts_description_id": lambda x: int(x) if x else None,
            },
        )

        # Parts
        self.register_table_mapping(
            source_name=f"Parts{file_ext}",
            model_class=Parts,
            field_mapping={
                "part_terminology_id": "PartTerminologyID",
                "part_terminology_name": "PartTerminologyName",
                "parts_description_id": "PartsDescriptionID",
                "rev_date": "RevDate",
            },
            primary_key="part_terminology_id",
            transformers={
                "part_terminology_id": lambda x: int(x) if x else None,
                "parts_description_id": lambda x: int(x) if x else None,
                "rev_date": lambda x: (
                    datetime.strptime(x, "%Y-%m-%d").date() if x and x.strip() else None
                ),
            },
            validators={
                "part_terminology_id": lambda x: (
                    x is not None,
                    "Part terminology ID is required",
                ),
                "part_terminology_name": lambda x: (
                    bool(x and x.strip()),
                    "Part terminology name is required",
                ),
            },
        )

        # Part Category
        self.register_table_mapping(
            source_name=f"PartCategory{file_ext}",
            model_class=PartCategory,
            field_mapping={
                "part_category_id": "PartCategoryID",
                "part_terminology_id": "PartTerminologyID",
                "subcategory_id": "SubCategoryID",
                "category_id": "CategoryID",
            },
            primary_key="part_category_id",
            transformers={
                "part_category_id": lambda x: int(x) if x else None,
                "part_terminology_id": lambda x: int(x) if x else None,
                "subcategory_id": lambda x: int(x) if x else None,
                "category_id": lambda x: int(x) if x else None,
            },
        )

        # Part Position
        self.register_table_mapping(
            source_name=f"PartPosition{file_ext}",
            model_class=PartPosition,
            field_mapping={
                "part_position_id": "PartPositionID",
                "part_terminology_id": "PartTerminologyID",
                "position_id": "PositionID",
                "rev_date": "RevDate",
            },
            primary_key="part_position_id",
            transformers={
                "part_position_id": lambda x: int(x) if x else None,
                "part_terminology_id": lambda x: int(x) if x else None,
                "position_id": lambda x: int(x) if x else None,
                "rev_date": lambda x: (
                    datetime.strptime(x, "%Y-%m-%d").date() if x and x.strip() else None
                ),
            },
        )

        # Parts Supersession
        self.register_table_mapping(
            source_name=f"PartsSupersession{file_ext}",
            model_class=PartsSupersession,
            field_mapping={
                "parts_supersession_id": "PartsSupersessionId",
                "old_part_terminology_id": "OldPartTerminologyID",
                "old_part_terminology_name": "OldPartTerminologyName",
                "new_part_terminology_id": "NewPartTerminologyID",
                "new_part_terminology_name": "NewPartTerminologyName",
                "rev_date": "RevDate",
                "note": "Note",
            },
            primary_key="parts_supersession_id",
            transformers={
                "parts_supersession_id": lambda x: int(x) if x else None,
                "old_part_terminology_id": lambda x: int(x) if x else None,
                "new_part_terminology_id": lambda x: int(x) if x else None,
                "rev_date": lambda x: (
                    datetime.strptime(x, "%Y-%m-%d").date() if x and x.strip() else None
                ),
            },
        )

        # Alias
        self.register_table_mapping(
            source_name=f"Alias{file_ext}",
            model_class=Alias,
            field_mapping={
                "alias_id": "AliasID",
                "alias_name": "AliasName",
            },
            primary_key="alias_id",
            transformers={
                "alias_id": lambda x: int(x) if x else None,
            },
        )

        # Use
        self.register_table_mapping(
            source_name=f"Use{file_ext}",
            model_class=Use,
            field_mapping={
                "use_id": "UseID",
                "use_description": "UseDescription",
            },
            primary_key="use_id",
            transformers={
                "use_id": lambda x: int(x) if x else None,
            },
        )

        # Many-to-many: Parts to Alias
        self.register_many_to_many_table(
            source_name=f"PartsToAlias{file_ext}",
            table_name="parts_to_alias",
            field_mapping={
                "part_terminology_id": "PartTerminologyID",
                "alias_id": "AliasID",
            },
            transformers={
                "part_terminology_id": lambda x: int(x) if x else None,
                "alias_id": lambda x: int(x) if x else None,
            },
        )

        # Many-to-many: Parts to Use
        self.register_many_to_many_table(
            source_name=f"PartsToUse{file_ext}",
            table_name="parts_to_use",
            field_mapping={
                "part_terminology_id": "PartTerminologyID",
                "use_id": "UseID",
            },
            transformers={
                "part_terminology_id": lambda x: int(x) if x else None,
                "use_id": lambda x: int(x) if x else None,
            },
        )

        # CodeMaster is a more complex table that combines data from other tables
        self.register_table_mapping(
            source_name=f"CodeMaster{file_ext}",
            model_class=CodeMaster,
            field_mapping={
                "code_master_id": "CodeMasterID",
                "part_terminology_id": "PartTerminologyID",
                "category_id": "CategoryID",
                "subcategory_id": "SubCategoryID",
                "position_id": "PositionID",
                "rev_date": "RevDate",
            },
            primary_key="code_master_id",
            transformers={
                "code_master_id": lambda x: int(x) if x else None,
                "part_terminology_id": lambda x: int(x) if x else None,
                "category_id": lambda x: int(x) if x else None,
                "subcategory_id": lambda x: int(x) if x else None,
                "position_id": lambda x: int(x) if x else None,
                "rev_date": lambda x: (
                    datetime.strptime(x, "%Y-%m-%d").date() if x and x.strip() else None
                ),
            },
        )
