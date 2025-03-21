# app/data_import/connectors/base.py
from __future__ import annotations

"""
Base interfaces for data source connectors.

This module defines protocol classes for data source connectors that extract
data from various sources like databases, files, and APIs.
"""

from typing import Any, Dict, List, Protocol, TypeVar

T = TypeVar("T")


class Connector(Protocol):
    """Protocol for data source connectors."""

    async def connect(self) -> None:
        """
        Establish connection to the data source.

        Raises:
            ConnectionError: If connection cannot be established
        """
        ...

    async def extract(
        self, query: str, limit: Optional[int] = None, **params: Any
    ) -> List[Dict[str, Any]]:
        """
        Extract data from the source.

        Args:
            query: Query string or identifier for the data to extract
            limit: Maximum number of records to retrieve
            params: Additional parameters for the query

        Returns:
            List of records as dictionaries

        Raises:
            ValueError: If query is invalid
            ConnectionError: If connection issues occur during extraction
        """
        ...

    async def close(self) -> None:
        """
        Close the connection.

        Raises:
            ConnectionError: If closing the connection fails
        """
        ...
