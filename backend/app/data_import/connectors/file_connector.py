# app/data_import/connectors/file_connector.py
from __future__ import annotations

"""
File connector for data import.

This module provides a connector for extracting data from files such as
CSV and JSON.
"""

import csv
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field, validator

from app.core.exceptions import ConfigurationException
from app.logging import get_logger

logger = get_logger("app.data_import.connectors.file_connector")


class FileConnectionConfig(BaseModel):
    """Configuration for file connections."""

    file_path: str = Field(..., description="Path to the file")
    file_type: Literal["csv", "json"] = Field(..., description="Type of file")
    encoding: str = Field("utf-8", description="File encoding")
    csv_delimiter: str = Field(",", description="CSV delimiter character")
    csv_quotechar: str = Field('"', description="CSV quote character")

    @validator("file_path")
    def validate_file_path(cls, v: str) -> str:
        if not os.path.exists(v):
            raise ValueError(f"File does not exist: {v}")
        return v

    @validator("file_type")
    def validate_file_type(cls, v: str, values: Dict[str, Any]) -> str:
        file_path = values.get("file_path", "")
        if v == "csv" and not file_path.endswith(".csv"):
            raise ValueError(
                f"File with extension {Path(file_path).suffix} is not a CSV file"
            )
        if v == "json" and not file_path.endswith(".json"):
            raise ValueError(
                f"File with extension {Path(file_path).suffix} is not a JSON file"
            )
        return v


class FileConnector:
    """Connector for file-based data sources (CSV, JSON)."""

    def __init__(self, config: FileConnectionConfig) -> None:
        """
        Initialize the File connector.

        Args:
            config: File connection configuration
        """
        self.config = config
        self.file_data: Optional[List[Dict[str, Any]]] = None
        logger.debug(f"FileConnector initialized for file: {config.file_path}")

    async def connect(self) -> None:
        """
        Establish connection to the file.

        This method loads the file data into memory.

        Raises:
            ConfigurationException: If the file cannot be loaded
        """
        try:
            logger.debug(f"Loading file: {self.config.file_path}")

            if self.config.file_type == "csv":
                with open(
                    self.config.file_path, "r", encoding=self.config.encoding
                ) as file:
                    reader = csv.DictReader(
                        file,
                        delimiter=self.config.csv_delimiter,
                        quotechar=self.config.csv_quotechar,
                    )
                    self.file_data = list(reader)

            elif self.config.file_type == "json":
                with open(
                    self.config.file_path, "r", encoding=self.config.encoding
                ) as file:
                    data = json.load(file)
                    # Ensure the data is a list of dictionaries
                    if isinstance(data, dict):
                        # If it's a dictionary with a records key, use that
                        if "records" in data and isinstance(data["records"], list):
                            self.file_data = data["records"]
                        # Otherwise, convert to a list with a single item
                        else:
                            self.file_data = [data]
                    else:
                        self.file_data = data

            logger.info(f"Loaded {len(self.file_data or [])} records from file")

        except Exception as e:
            logger.error(f"Failed to load file {self.config.file_path}: {str(e)}")
            raise ConfigurationException(
                message=f"Failed to load file: {str(e)}",
                component="FileConnector",
                original_exception=e,
            ) from e

    async def extract(
        self, query: str = "", limit: Optional[int] = None, **params: Any
    ) -> List[Dict[str, Any]]:
        """
        Extract data from the file.

        The query parameter is optional for file connectors and can be used
        to filter the data based on specific criteria.

        Args:
            query: Optional filter criteria
            limit: Maximum number of records to retrieve
            params: Additional parameters

        Returns:
            List of records as dictionaries

        Raises:
            ConfigurationException: If extraction fails
        """
        if self.file_data is None:
            await self.connect()

        try:
            # If no query is provided, return all data
            if not query:
                data = self.file_data or []
                # Apply limit if specified
                if limit is not None:
                    data = data[:limit]
                return data

            # Simple filtering based on field values
            # Format: field1=value1,field2=value2
            if "," in query and "=" in query:
                conditions = [condition.strip() for condition in query.split(",")]
                field_values = {}

                for condition in conditions:
                    field, value = condition.split("=", 1)
                    field_values[field.strip()] = value.strip()

                filtered_data = []
                for item in self.file_data or []:
                    match = True
                    for field, value in field_values.items():
                        if field not in item or str(item[field]) != value:
                            match = False
                            break
                    if match:
                        filtered_data.append(item)

                logger.debug(f"Filtered data to {len(filtered_data)} records")

                # Apply limit if specified
                if limit is not None:
                    filtered_data = filtered_data[:limit]

                return filtered_data

            # Otherwise, assume query is a list index or slice
            try:
                index = int(query)
                return [self.file_data[index]] if self.file_data else []
            except (ValueError, IndexError, TypeError):
                logger.warning(f"Invalid query for file connector: {query}")
                data = self.file_data or []

                # Apply limit if specified
                if limit is not None:
                    data = data[:limit]

                return data

        except Exception as e:
            logger.error(f"Error extracting data from file: {str(e)}")
            raise ConfigurationException(
                message=f"Failed to extract data from file: {str(e)}",
                component="FileConnector",
                original_exception=e,
            ) from e

    async def close(self) -> None:
        """Close the connection (clear file data from memory)."""
        self.file_data = None
        logger.debug("File connection closed")
