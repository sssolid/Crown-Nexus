# app/data_import/importers/base.py
from __future__ import annotations

"""
Base interfaces for data importers.

This module defines protocol classes for data importers that insert or update
data in the application database.
"""

from typing import Any, Dict, Generic, List, Protocol, TypeVar

T = TypeVar("T")

class Importer(Protocol[T]):
    """Protocol for data importers."""

    async def import_data(self, data: List[T]) -> Dict[str, Any]:
        """
        Import data into the target system.

        Args:
            data: List of records to import

        Returns:
            Dictionary with import statistics

        Raises:
            ValueError: If data cannot be imported
            DatabaseError: If database operations fail
        """
        ...
