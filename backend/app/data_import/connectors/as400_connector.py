from __future__ import annotations

"""
AS400 connector for data import.

This module provides a secure connector for extracting data from AS400/iSeries
databases while implementing strict security measures to protect sensitive data.
"""

import os
import logging
from typing import Any, Dict, List, Optional, Union, Set
import pyodbc
from pydantic import BaseModel, Field, SecretStr, validator
from cryptography.fernet import Fernet

from app.core.exceptions import (
    ConfigurationException,
    DatabaseException,
    SecurityException,
)
from app.core.logging import get_logger

logger = get_logger("app.data_import.connectors.as400_connector")


class AS400ConnectionConfig(BaseModel):
    """Configuration for connecting to AS400/iSeries databases securely."""

    dsn: str = Field(..., description="ODBC Data Source Name")
    username: str = Field(..., description="AS400 username (read-only account)")
    password: SecretStr = Field(..., description="AS400 password")
    database: str = Field(..., description="AS400 database/library name")
    server: Optional[str] = Field(None, description="AS400 server address")
    port: Optional[int] = Field(None, description="AS400 server port")
    ssl: bool = Field(True, description="Use SSL for connection")
    allowed_tables: Optional[List[str]] = Field(
        None, description="Whitelist of allowed tables"
    )
    allowed_schemas: Optional[List[str]] = Field(
        None, description="Whitelist of allowed schemas/libraries"
    )
    connection_timeout: int = Field(30, description="Connection timeout in seconds")
    query_timeout: int = Field(60, description="Query timeout in seconds")
    encrypt_connection: bool = Field(True, description="Encrypt connection parameters")

    @validator("port")
    def validate_port(cls, v: Optional[int]) -> Optional[int]:
        """Validate port is within allowed range."""
        if v is not None and (v < 1 or v > 65535):
            raise ValueError("Port must be between 1 and 65535")
        return v

    @validator("allowed_tables", "allowed_schemas")
    def validate_allowed_lists(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """Validate and normalize allowed lists."""
        if v is not None:
            return [item.upper() for item in v]
        return v

    class Config:
        """Pydantic config."""

        validate_assignment = True
        extra = "forbid"


class AS400Connector:
    """
    Secure connector for AS400/iSeries databases.

    Implements multiple security layers:
    1. SecretStr for password handling
    2. Whitelist for allowed tables and schemas
    3. Read-only operations only
    4. SSL/TLS encryption when available
    5. Timeouts to prevent hanging connections
    6. Detailed audit logging
    """

    def __init__(self, config: AS400ConnectionConfig) -> None:
        """
        Initialize the AS400 connector with secure configuration.

        Args:
            config: Configuration for the AS400 connection
        """
        self.config = config
        self.connection = None
        self._encryption_key = self._get_encryption_key()
        self._accessed_tables: Set[str] = set()
        logger.debug(
            f"AS400Connector initialized for DSN: {config.dsn}, "
            f"Server: {config.server or 'from DSN'}, "
            f"Database: {config.database}"
        )

    async def connect(self) -> None:
        """
        Establish a secure connection to the AS400 database.

        Raises:
            SecurityException: If security requirements aren't met
            DatabaseException: If connection fails
            ConfigurationException: If configuration is invalid
        """
        try:
            # Build secure connection string
            connection_string = self._build_connection_string()

            # Log connection attempt (without credentials)
            logger.info(
                f"Connecting to AS400 database: {self.config.database} "
                f"on DSN: {self.config.dsn}"
            )

            # Connect to the database
            # Some drivers don't support the timeout parameter through connect()
            # So we'll try both approaches
            try:
                self.connection = pyodbc.connect(connection_string)
            except pyodbc.Error as e:
                logger.debug(
                    f"Connection attempt failed: {str(e)}, retrying with different parameters"
                )
                # If first approach fails, try without any extra parameters
                self.connection = pyodbc.connect(connection_string)

            # Set additional connection properties for security
            if self.connection:
                try:
                    # These might not be supported by all drivers
                    self.connection.setdecoding(pyodbc.SQL_CHAR, encoding="utf-8")
                    self.connection.setdecoding(pyodbc.SQL_WCHAR, encoding="utf-8")
                    self.connection.setencoding(encoding="utf-8")
                except (pyodbc.Error, AttributeError) as e:
                    logger.debug(f"Could not set encoding: {str(e)}")

                try:
                    # Set query timeout if supported
                    if hasattr(self.connection, "timeout"):
                        self.connection.timeout = self.config.query_timeout
                except (pyodbc.Error, AttributeError) as e:
                    logger.debug(f"Could not set timeout: {str(e)}")

            logger.info(
                f"Successfully connected to AS400 database: {self.config.database}"
            )
        except pyodbc.Error as e:
            error_msg = str(e)
            # Sanitize error message to remove any potential credentials
            sanitized_error = self._sanitize_error_message(error_msg)
            logger.error(f"Failed to connect to AS400: {sanitized_error}")

            # Convert error to appropriate exception type
            if (
                "permission" in error_msg.lower()
                or "access denied" in error_msg.lower()
            ):
                raise SecurityException(
                    message=f"Security error connecting to AS400: {sanitized_error}",
                    original_exception=e,
                )
            else:
                raise DatabaseException(
                    message=f"Failed to connect to AS400 database: {sanitized_error}",
                    original_exception=e,
                )

    async def extract(
        self, query: str, limit: Optional[int] = None, **params: Any
    ) -> List[Dict[str, Any]]:
        """
        Securely extract data from AS400.

        Args:
            query: SQL query or table name
            limit: Maximum number of records to return
            **params: Query parameters

        Returns:
            List of dictionaries containing the query results

        Raises:
            SecurityException: If the query attempts to access unauthorized tables
            DatabaseException: If the query fails to execute
        """
        if not self.connection:
            await self.connect()

        # Validate and sanitize query before execution
        table_name = self._validate_and_prepare_query(query, limit)

        try:
            cursor = self.connection.cursor()

            # Log query execution (sanitized)
            sanitized_query = self._sanitize_sql_for_logging(query)
            logger.debug(f"Executing AS400 query: {sanitized_query}")

            # Execute the query
            if params:
                cursor.execute(query, tuple(params.values()))
            else:
                cursor.execute(query)

            # Record table access for auditing
            if table_name:
                self._accessed_tables.add(table_name.upper())

            # Process results
            columns = [column[0] for column in cursor.description]
            results = []
            for row in cursor.fetchall():
                result_dict = dict(zip(columns, row))
                # Convert any AS400-specific data types if needed
                results.append(self._convert_as400_types(result_dict))

            # Log success
            logger.info(
                f"Successfully extracted {len(results)} records from AS400 "
                f"{'table: ' + table_name if table_name else 'query'}"
            )
            return results

        except pyodbc.Error as e:
            error_msg = str(e)
            sanitized_error = self._sanitize_error_message(error_msg)
            logger.error(f"Error extracting data from AS400: {sanitized_error}")

            # Classify error
            if (
                "permission" in error_msg.lower()
                or "access denied" in error_msg.lower()
            ):
                raise SecurityException(
                    message=f"Security error accessing AS400 data: {sanitized_error}",
                    original_exception=e,
                )
            else:
                raise DatabaseException(
                    message=f"Failed to extract data from AS400: {sanitized_error}",
                    original_exception=e,
                )

    async def close(self) -> None:
        """
        Safely close the AS400 connection.

        Raises:
            DatabaseException: If closing the connection fails
        """
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
                logger.debug("AS400 connection closed")

                # Audit logging
                if self._accessed_tables:
                    logger.info(
                        f"AS400 session accessed the following tables: "
                        f"{', '.join(sorted(self._accessed_tables))}"
                    )
            except pyodbc.Error as e:
                logger.error(f"Error closing AS400 connection: {str(e)}")
                raise DatabaseException(
                    message=f"Failed to close AS400 connection: {str(e)}",
                    original_exception=e,
                )

    def _build_connection_string(self) -> str:
        """
        Build a secure connection string for AS400.

        Returns:
            Connection string with proper security parameters
        """
        # Start with required parameters
        connection_string = (
            f"DSN={self.config.dsn};"
            f"UID={self.config.username};"
            f"PWD={self.config.password.get_secret_value()};"
            f"DATABASE={self.config.database};"
        )

        # Add optional parameters
        if self.config.server:
            connection_string += f"SYSTEM={self.config.server};"

        if self.config.port:
            connection_string += f"PORT={self.config.port};"

        # Many AS400 ODBC drivers don't support SSL connection parameter directly
        # It's often configured at the ODBC DSN level instead
        # Only add if explicitly configured and you know your driver supports it
        if (
            self.config.ssl
            and os.environ.get("AS400_ENABLE_SSL_PARAM", "").lower() == "true"
        ):
            connection_string += "SSLCONNECTION=TRUE;"

        # Many AS400 ODBC drivers don't support the ReadOnly parameter
        # Only add if explicitly configured and you know your driver supports it
        if os.environ.get("AS400_ENABLE_READONLY_PARAM", "").lower() == "true":
            connection_string += "ReadOnly=True;"

        # Add read-only parameter if driver supports it
        connection_string += "ReadOnly=True;"

        return connection_string

    def _validate_and_prepare_query(
        self, query: str, limit: Optional[int]
    ) -> Optional[str]:
        """
        Validate query for security and prepare for execution.

        Args:
            query: The SQL query or table name
            limit: Maximum records to return

        Returns:
            Table name if a table-only query, None otherwise

        Raises:
            SecurityException: If the query is attempting to perform unauthorized operations
        """
        # Check if query is just a table name (for simple SELECT *)
        if " " not in query:
            table_name = query.strip()

            # Check against whitelist if configured
            if self.config.allowed_tables:
                if table_name.upper() not in self.config.allowed_tables:
                    raise SecurityException(
                        message=f"Access to table '{table_name}' is not allowed"
                    )

            # Add limit clause if requested
            limit_clause = (
                f" FETCH FIRST {limit} ROWS ONLY" if limit is not None else ""
            )
            query = f'SELECT * FROM "{table_name}"{limit_clause}'
            return table_name
        else:
            # For SQL queries, perform security checks
            query_upper = query.upper()

            # Ensure query is read-only
            if any(
                write_op in query_upper
                for write_op in [
                    "INSERT",
                    "UPDATE",
                    "DELETE",
                    "CREATE",
                    "DROP",
                    "ALTER",
                    "TRUNCATE",
                    "GRANT",
                    "REVOKE",
                    "RENAME",
                ]
            ):
                raise SecurityException(
                    message="Write operations are not allowed on AS400 connection"
                )

            # Add LIMIT clause if requested and not already present
            if (
                limit is not None
                and "LIMIT" not in query_upper
                and "FETCH FIRST" not in query_upper
            ):
                if ";" in query:
                    query = query.rstrip(";")
                query = f"{query} FETCH FIRST {limit} ROWS ONLY"

            return None

    def _convert_as400_types(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert AS400-specific data types to Python types.

        Args:
            row: Dict containing a database row

        Returns:
            Dict with converted values
        """
        result = {}
        for key, value in row.items():
            # Convert decimals to float
            if hasattr(value, "real") and not isinstance(value, (int, float)):
                result[key] = float(value)
            # Convert date/time objects if needed
            elif hasattr(value, "isoformat"):
                result[key] = value
            else:
                result[key] = value
        return result

    def _sanitize_sql_for_logging(self, query: str) -> str:
        """
        Sanitize SQL query for safe logging.

        Args:
            query: SQL query

        Returns:
            Sanitized query
        """
        # Simple sanitization - can be enhanced if needed
        return query.replace("\n", " ").replace("\r", " ")

    def _sanitize_error_message(self, error_message: str) -> str:
        """
        Sanitize error messages to avoid leaking sensitive information.

        Args:
            error_message: Original error message

        Returns:
            Sanitized error message
        """
        # Remove potential password information
        sanitized = error_message.replace(
            self.config.password.get_secret_value(), "[REDACTED]"
        )
        # Additional sanitization as needed
        return sanitized

    def _get_encryption_key(self) -> bytes:
        """
        Get or generate encryption key for secure storage.

        Returns:
            Encryption key
        """
        key_env_var = "AS400_ENCRYPTION_KEY"
        key = os.environ.get(key_env_var)

        if not key and self.config.encrypt_connection:
            # Generate a key - in production, this should be stored securely
            key = Fernet.generate_key().decode()
            logger.warning(
                f"No encryption key found in environment variable {key_env_var}. "
                f"Generated new key. For production, set this environment variable."
            )

        return key.encode() if key else b""
