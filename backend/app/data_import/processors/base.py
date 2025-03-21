# app/data_import/processors/base.py
from __future__ import annotations

"""
Base interfaces for data processors.

This module defines protocol classes for data processors that transform and validate
raw data into structured formats suitable for importing into the application.
"""

from typing import Any, Dict, Generic, List, Protocol, TypeVar

T = TypeVar("T")


class Processor(Protocol[T]):
    """Protocol for data processors."""

    async def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process raw data into structured data.

        Args:
            data: List of raw data records

        Returns:
            List of processed records

        Raises:
            ValueError: If data cannot be processed
        """
        ...

    async def validate(self, data: List[Dict[str, Any]]) -> List[T]:
        """
        Validate processed data.

        Args:
            data: List of processed records

        Returns:
            List of validated records

        Raises:
            ValidationError: If data fails validation
        """
        ...
