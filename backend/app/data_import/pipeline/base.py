# app/data_import/pipeline/base.py
from __future__ import annotations

"""
Base interfaces for data import pipelines.

This module defines protocol classes for data import pipelines that orchestrate
the extract, transform, and load process.
"""

from typing import Any, Dict, Generic, List, Protocol, TypeVar, Union

from app.data_import.connectors.base import Connector
from app.data_import.connectors.file_connector import FileConnector
from app.data_import.connectors.filemaker_connector import FileMakerConnector
from app.data_import.importers.base import Importer
from app.data_import.processors.base import Processor

T = TypeVar("T")


class Pipeline(Protocol[T]):
    """Protocol for data import pipelines."""

    connector: Union[Connector, FileMakerConnector, FileConnector]
    processor: Processor[T]
    importer: Importer[T]

    async def run(self, query: str, **params: Any) -> Dict[str, Any]:
        """
        Run the complete ETL pipeline.

        Args:
            query: Query string or identifier for the data to extract
            params: Additional parameters for the query

        Returns:
            Dictionary with pipeline execution statistics

        Raises:
            Exception: If any stage of the pipeline fails
        """
        ...
