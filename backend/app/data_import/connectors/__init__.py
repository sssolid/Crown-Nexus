# app/data_import/connectors/__init__.py
from __future__ import annotations

"""
Data source connectors for data import.

This package provides connectors for extracting data from various sources,
including AS400, FileMaker databases and files.
"""

from app.data_import.connectors.base import Connector
from app.data_import.connectors.file_connector import (
    FileConnector,
    FileConnectionConfig,
)
from app.data_import.connectors.filemaker_connector import (
    FileMakerConnector,
    FileMakerConnectionConfig,
)
from app.data_import.connectors.as400_connector import (
    AS400Connector,
    AS400ConnectionConfig,
)

__all__ = [
    "Connector",
    "FileConnector",
    "FileConnectionConfig",
    "FileMakerConnector",
    "FileMakerConnectionConfig",
    "AS400Connector",
    "AS400ConnectionConfig",
]
