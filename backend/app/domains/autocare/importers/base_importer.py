# app/domains/autocare/importers/base_importer.py
from __future__ import annotations

"""
Base importer interface for AutoCare data.

This module defines the base protocol for all data importers used to import
AutoCare standard data from various sources into the application database.
"""

import abc
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol, TypeVar, Set

from sqlalchemy.ext.asyncio import AsyncSession

from app.logging import get_logger

logger = get_logger("app.domains.autocare.importers.base_importer")

T = TypeVar("T")


class BaseImporter(Protocol):
    """Base protocol for all data importers."""

    db: AsyncSession
    source_path: Path

    async def validate_source(self) -> bool:
        """
        Validate that the source data is valid.

        Returns:
            bool: True if valid, False otherwise
        """
        ...

    async def import_data(self) -> Dict[str, Any]:
        """
        Import data from source to database.

        Returns:
            Dict[str, Any]: Dictionary with import results
        """
        ...
