# app/data_import/connectors/filemaker_connector.py
from __future__ import annotations

"""
FileMaker connector for data import.

This module provides a connector for extracting data from FileMaker databases
using ODBC connections.
"""

from typing import Any, Dict, List, Optional

import pyodbc
from pydantic import BaseModel, Field, validator

from app.core.exceptions import DatabaseException
from app.core.logging import get_logger

logger = get_logger("app.data_import.connectors.filemaker_connector")


class FileMakerConnectionConfig(BaseModel):
    """Configuration for FileMaker ODBC connection."""

    dsn: str = Field(..., description="ODBC Data Source Name")
    username: str = Field(..., description="FileMaker username")
    password: str = Field(..., description="FileMaker password")
    database: Optional[str] = Field(
        None, description="FileMaker database name (often included in DSN)"
    )
    server: Optional[str] = Field(None, description="FileMaker server address")
    port: Optional[int] = Field(None, description="FileMaker server port")
    disable_ssl_verification: bool = Field(
        False, description="Disable SSL certificate verification"
    )

    @validator("port")
    def validate_port(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and (v < 1 or v > 65535):
            raise ValueError("Port must be between 1 and 65535")
        return v


class FileMakerConnector:
    """Connector for FileMaker databases using ODBC."""

    def __init__(self, config: FileMakerConnectionConfig) -> None:
        """
        Initialize the FileMaker connector.

        Args:
            config: FileMaker connection configuration
        """
        self.config = config
        self.connection = None
        logger.debug(f"FileMakerConnector initialized with DSN: {config.dsn}")

    async def connect(self) -> None:
        """
        Establish connection to the FileMaker database.

        Raises:
            DatabaseException: If connection fails
        """
        try:
            # Build the connection string with only required parameters
            connection_string = f"DSN={self.config.dsn};UID={self.config.username};PWD={self.config.password}"

            # Add optional parameters only if specified
            if self.config.database:
                connection_string += f";Database={self.config.database}"

            if self.config.server:
                connection_string += f";Server={self.config.server}"

            if self.config.port:
                connection_string += f";Port={self.config.port}"

            # Handle SSL verification settings
            if self.config.disable_ssl_verification:
                # For typical ODBC drivers
                connection_string += ";SSLVerifyServerCert=0"

                # Some environments require setting environment variables
                # to disable SSL verification globally
                import os

                os.environ["PYTHONHTTPSVERIFY"] = "0"

                logger.warning(
                    "SSL certificate verification disabled for FileMaker connection"
                )

            logger.debug(f"Connecting to FileMaker with DSN: {self.config.dsn}")

            # Note: pyodbc is synchronous, but we wrap it in an async API
            # In a production system, you might want to use asyncio.to_thread()
            self.connection = pyodbc.connect(connection_string)

            db_name = self.config.database or "default database"
            logger.info(f"Connected to FileMaker database: {db_name}")
        except pyodbc.Error as e:
            logger.error(f"Failed to connect to FileMaker: {str(e)}")
            raise DatabaseException(
                message=f"Failed to connect to FileMaker database: {str(e)}",
                original_exception=e,
            ) from e

    async def extract(
        self, query: str, limit: Optional[int] = None, **params: Any
    ) -> List[Dict[str, Any]]:
        """
        Extract data from FileMaker.

        Args:
            query: SQL query or table/layout name
            limit: Maximum number of records to retrieve
            params: Parameters for the query

        Returns:
            List of records as dictionaries

        Raises:
            DatabaseException: If extraction fails
        """
        if not self.connection:
            await self.connect()

        try:
            cursor = self.connection.cursor()

            # If query is a table name rather than a SQL query
            if " " not in query:
                # Add LIMIT clause if specified
                limit_clause = (
                    f" FETCH FIRST {limit} ROWS ONLY" if limit is not None else ""
                )
                query = f'SELECT * FROM "{query}"{limit_clause}'
                logger.debug(f"Using table query: {query}")

                # Execute without parameters when just querying a table
                cursor.execute(query)
            else:
                # If it's a custom SQL query with limit
                if limit is not None and "LIMIT" not in query.upper():
                    query = f"{query} LIMIT {limit}"

                logger.debug(f"Using custom SQL query with params: {params}")
                cursor.execute(query, tuple(params.values()) if params else None)

            # Get column names
            columns = [column[0] for column in cursor.description]

            # Fetch all rows and convert to dictionaries
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))

            logger.debug(f"Extracted {len(results)} records from FileMaker")
            return results

        except pyodbc.Error as e:
            logger.error(f"Error extracting data from FileMaker: {str(e)}")
            raise DatabaseException(
                message=f"Failed to extract data from FileMaker: {str(e)}",
                original_exception=e,
            ) from e

    async def close(self) -> None:
        """
        Close the connection to FileMaker.

        Raises:
            DatabaseException: If closing the connection fails
        """
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
                logger.debug("FileMaker connection closed")
            except pyodbc.Error as e:
                logger.error(f"Error closing FileMaker connection: {str(e)}")
                raise DatabaseException(
                    message=f"Failed to close FileMaker connection: {str(e)}",
                    original_exception=e,
                ) from e
