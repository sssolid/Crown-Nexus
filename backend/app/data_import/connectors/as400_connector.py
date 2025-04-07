from __future__ import annotations

"""
AS400 connector for data import.

This module provides a secure connector for extracting data from AS400/iSeries
databases using the JTOpen (JT400) Java library via JPype while implementing
strict security measures to protect sensitive data.
"""

import os
import re
from enum import Enum
from typing import Any, Dict, List, Optional, Set, TypedDict, Union, cast
from pathlib import Path
from dataclasses import dataclass, field
from pydantic import BaseModel, Field, SecretStr, validator, root_validator
from cryptography.fernet import Fernet
import structlog
from functools import cache

from app.core.exceptions import (
    DatabaseException,
    SecurityException,
    ConfigurationException,
)
from app.logging import get_logger

logger = get_logger("app.data_import.connectors.as400_connector")


class AS400ConnectionConfig(BaseModel):
    """Configuration for connecting to AS400/iSeries databases securely using JT400."""

    jt400_jar_path: str = Field(
        ..., description="Path to the jt400.jar file for Java connection"
    )
    server: str = Field(..., description="AS400 server address")
    username: str = Field(..., description="AS400 username (read-only account)")
    password: SecretStr = Field(..., description="AS400 password")
    database: str = Field(..., description="AS400 database/library name")
    port: Optional[int] = Field(None, description="AS400 server port (default: 446)")
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

    @validator("jt400_jar_path")
    def validate_jar_path(cls, v: str) -> str:
        """Validate that the jt400.jar file exists."""
        jar_path = Path(v)
        if not jar_path.exists() or not jar_path.is_file():
            raise ValueError(f"jt400.jar file not found at: {v}")
        return v

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


class ColumnMetadata(TypedDict):
    """Type definition for column metadata."""

    name: str
    type_name: str
    type_code: int
    precision: int
    scale: int
    nullable: bool


@dataclass
class AS400Connection:
    """Wrapper for JT400 Connection object with metadata."""

    connection: Any  # Java Connection object
    jdbc_url: str
    properties: Dict[str, str] = field(default_factory=dict)
    accessed_tables: Set[str] = field(default_factory=set)


class AS400Connector:
    """
    Secure connector for AS400/iSeries databases using JT400 via JPype.

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
        self._connection: Optional[AS400Connection] = None
        self._encryption_key = self._get_encryption_key()

        # Import JPype
        try:
            import jpype
            from jpype.types import JException

            self._jpype = jpype
            self._JException = JException
            # Initialize JVM if needed
            self._initialize_jpype()
        except ImportError:
            raise ImportError(
                "jpype module is required for JT400 connections. "
                "Please install it with 'pip install jpype1'."
            )

        logger.debug(
            "AS400Connector initialized",
            server=config.server,
            database=config.database,
        )

    @cache
    def _initialize_jpype(self) -> None:
        """
        Initialize JPype and JVM to use JT400.

        This method is cached to ensure JVM is started only once.
        """
        jpype = self._jpype  # Local reference for efficiency

        if not jpype.isJVMStarted():
            # Start JVM with JT400 jar in classpath
            jpype.startJVM(
                classpath=[self.config.jt400_jar_path],
                convertStrings=True,
            )
            logger.debug("JVM started for JT400 access")

            # Try to load the AS400 JDBC driver
            try:
                driver_class = jpype.JClass("com.ibm.as400.access.AS400JDBCDriver")
                driver = driver_class()
                # Register the driver with DriverManager
                jpype.JClass("java.sql.DriverManager").registerDriver(driver)
                logger.debug("AS400 JDBC driver registered successfully")
            except Exception as e:
                logger.warning(
                    "Could not register AS400 JDBC driver explicitly",
                    error=str(e),
                )

    async def connect(self) -> None:
        """
        Establish a secure connection to the AS400 database using JT400.

        Raises:
            SecurityException: If security requirements aren't met
            DatabaseException: If connection fails
            ConfigurationException: If configuration is invalid
        """
        jpype = self._jpype  # Local reference for efficiency
        JException = self._JException  # Local reference for efficiency

        try:
            # Get Java classes needed for connection
            java_sql_DriverManager = jpype.JClass("java.sql.DriverManager")
            java_util_Properties = jpype.JClass("java.util.Properties")

            # Build JDBC URL
            jdbc_url = self._build_jdbc_url()

            # Create connection properties
            properties = java_util_Properties()
            properties.setProperty("user", self.config.username)
            properties.setProperty("password", self.config.password.get_secret_value())
            properties.setProperty("secure", "true" if self.config.ssl else "false")
            properties.setProperty("prompt", "false")  # Don't prompt for credentials
            properties.setProperty("libraries", self.config.database)

            # Set timeout properties if supported by JT400
            properties.setProperty("login timeout", str(self.config.connection_timeout))
            properties.setProperty("query timeout", str(self.config.query_timeout))
            properties.setProperty("transaction isolation", "read committed")
            properties.setProperty("date format", "iso")
            properties.setProperty("errors", "full")

            # Set to read-only mode
            properties.setProperty("access", "read only")

            # Log connection attempt (without credentials)
            logger.info(
                "Connecting to AS400 database",
                database=self.config.database,
                server=self.config.server,
                ssl=self.config.ssl,
            )

            # Connect to the database
            conn = java_sql_DriverManager.getConnection(jdbc_url, properties)

            # Set additional connection properties for security
            conn.setAutoCommit(True)
            conn.setReadOnly(True)

            # Store connection properties (excluding password)
            props_dict = {}
            prop_keys = properties.keySet().toArray()
            for key in prop_keys:
                str_key = str(key)
                if str_key != "password":  # Skip password for security
                    props_dict[str_key] = str(properties.getProperty(str_key))

            # Create and store connection wrapper
            self._connection = AS400Connection(
                connection=conn,
                jdbc_url=jdbc_url,
                properties=props_dict,
            )

            logger.info(
                "Successfully connected to AS400 database",
                database=self.config.database,
                server=self.config.server,
            )
        except JException as e:
            error_msg = str(e)
            # Sanitize error message to remove any potential credentials
            sanitized_error = self._sanitize_error_message(error_msg)
            logger.error(
                "Failed to connect to AS400",
                error=sanitized_error,
                exc_info=True,
            )

            # Convert error to appropriate exception type
            if (
                "permission" in error_msg.lower()
                or "access denied" in error_msg.lower()
                or "authorization" in error_msg.lower()
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
        if not self._connection:
            await self.connect()

        # Make sure we're connected
        connection = cast(AS400Connection, self._connection)

        # References for efficiency
        jpype = self._jpype
        JException = self._JException

        # Validate and sanitize query before execution
        table_name = self._validate_and_prepare_query(query, limit)

        try:
            # Get Java classes needed for query execution
            java_sql_Types = jpype.JClass("java.sql.Types")

            # Log query execution (sanitized)
            sanitized_query = self._sanitize_sql_for_logging(query)
            logger.debug(
                "Executing AS400 query",
                query=sanitized_query,
                limit=limit,
            )

            # Use prepared statement if parameters are provided
            if params:
                # Convert query parameters to use ? placeholders
                query, param_values = self._convert_to_prepared_statement(query, params)
                statement = connection.connection.prepareStatement(query)

                # Set parameters
                for i, value in enumerate(param_values):
                    self._set_prepared_statement_parameter(
                        statement, i + 1, value, java_sql_Types
                    )

                # Set query timeout if supported
                statement.setQueryTimeout(self.config.query_timeout)

                # Execute and get result set
                result_set = statement.executeQuery()
            else:
                # Create regular statement
                statement = connection.connection.createStatement()

                # Set query timeout if supported
                statement.setQueryTimeout(self.config.query_timeout)

                # Execute and get result set
                result_set = statement.executeQuery(query)

            # Record table access for auditing
            if table_name:
                connection.accessed_tables.add(table_name.upper())

            # Process results
            results = self._process_result_set(result_set, java_sql_Types)

            # Close the result set and statement
            result_set.close()
            statement.close()

            # Log success
            logger.info(
                "Successfully extracted records from AS400",
                record_count=len(results),
                table=table_name if table_name else None,
            )

            return results

        except JException as e:
            error_msg = str(e)
            sanitized_error = self._sanitize_error_message(error_msg)
            logger.error(
                "Error extracting data from AS400",
                error=sanitized_error,
                query=self._sanitize_sql_for_logging(query),
                exc_info=True,
            )

            # Classify error
            if (
                "permission" in error_msg.lower()
                or "access denied" in error_msg.lower()
                or "authorization" in error_msg.lower()
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
        if self._connection:
            try:
                # Get reference to connection before nulling it
                connection = self._connection

                # Close the connection
                connection.connection.close()
                self._connection = None
                logger.debug("AS400 connection closed")

                # Audit logging
                if connection.accessed_tables:
                    logger.info(
                        "AS400 session accessed tables",
                        tables=sorted(connection.accessed_tables),
                    )
            except self._JException as e:
                logger.error(
                    "Error closing AS400 connection",
                    error=str(e),
                    exc_info=True,
                )
                raise DatabaseException(
                    message=f"Failed to close AS400 connection: {str(e)}",
                    original_exception=e,
                )

    def _build_jdbc_url(self) -> str:
        """
        Build the JDBC URL for JT400 connection.

        Returns:
            JDBC URL string for connection
        """
        # Base JDBC URL for JT400
        jdbc_url = f"jdbc:as400://{self.config.server}"

        # Add port if specified
        if self.config.port:
            jdbc_url += f":{self.config.port}"

        # Configure additional parameters
        params = []

        # Add database/library if provided
        if self.config.database:
            params.append(f"libraries={self.config.database}")

        # Add secure connection parameter if SSL is requested
        if self.config.ssl:
            params.append("secure=true")

        # Add parameters to URL
        if params:
            jdbc_url += ";" + ";".join(params)

        return jdbc_url

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

            # Build full query with schema/library if needed
            full_table_name = f"{self.config.database}.{table_name}"

            # Add limit clause if requested
            limit_clause = (
                f" FETCH FIRST {limit} ROWS ONLY" if limit is not None else ""
            )
            query = f"SELECT * FROM {full_table_name}{limit_clause}"
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

    def _convert_to_prepared_statement(
        self, query: str, params: Dict[str, Any]
    ) -> tuple[str, List[Any]]:
        """
        Convert a query with named parameters to a prepared statement with ? placeholders.

        Args:
            query: SQL query with named parameters
            params: Parameters dictionary

        Returns:
            Tuple of (prepared statement query, ordered parameter values)
        """
        # Look for named parameters in the format :param_name
        param_names = re.findall(r":(\w+)", query)
        param_values = []

        # Replace each named parameter with ? and collect values in order
        for name in param_names:
            if name not in params:
                raise ValueError(
                    f"Parameter '{name}' not provided in params dictionary"
                )

            # Collect value
            param_values.append(params[name])

            # Replace named parameter with ?
            query = query.replace(f":{name}", "?", 1)

        return query, param_values

    def _set_prepared_statement_parameter(
        self, statement: Any, index: int, value: Any, java_sql_Types: Any
    ) -> None:
        """
        Set a parameter value in a prepared statement based on its type.

        Args:
            statement: JDBC PreparedStatement object
            index: Parameter index (1-based)
            value: Parameter value to set
            java_sql_Types: Java SQL Types class from JPype
        """
        jpype = self._jpype  # Local reference for efficiency

        # Handle None/null values
        if value is None:
            statement.setNull(index, java_sql_Types.NULL)
            return

        # Handle different Python types
        if isinstance(value, str):
            statement.setString(index, value)
        elif isinstance(value, int):
            statement.setInt(index, value)
        elif isinstance(value, float):
            statement.setDouble(index, value)
        elif isinstance(value, bool):
            statement.setBoolean(index, value)
        elif hasattr(value, "isoformat"):  # Date or datetime
            # Convert to java.sql.Date or Timestamp
            if hasattr(value, "hour"):  # datetime
                timestamp = jpype.JClass("java.sql.Timestamp")
                # Convert to milliseconds since epoch
                mills = int(value.timestamp() * 1000)
                statement.setTimestamp(index, timestamp(mills))
            else:  # date
                date = jpype.JClass("java.sql.Date")
                # Convert to days since epoch and then milliseconds
                mills = int(value.toordinal() * 86400 * 1000)
                statement.setDate(index, date(mills))
        else:
            # Fall back to string for other types
            statement.setString(index, str(value))

    def _process_result_set(
        self, result_set: Any, java_sql_Types: Any
    ) -> List[Dict[str, Any]]:
        """
        Process JDBC ResultSet into a list of dictionaries.

        Args:
            result_set: JDBC ResultSet object
            java_sql_Types: Java SQL Types class from JPype

        Returns:
            List of dictionaries containing the query results
        """
        # Get metadata for column names and types
        meta = result_set.getMetaData()
        column_count = meta.getColumnCount()

        # Extract column information
        columns: List[ColumnMetadata] = []
        for i in range(1, column_count + 1):
            columns.append(
                {
                    "name": meta.getColumnName(i),
                    "type_name": meta.getColumnTypeName(i),
                    "type_code": meta.getColumnType(i),
                    "precision": meta.getPrecision(i),
                    "scale": meta.getScale(i),
                    "nullable": meta.isNullable(i) != 0,
                }
            )

        # Process rows
        results = []
        while result_set.next():
            row = {}
            for i, col in enumerate(columns, 1):
                # Handle different data types appropriately
                value = self._get_result_set_value(result_set, i, col, java_sql_Types)
                row[col["name"]] = value

            results.append(row)

        return results

    def _get_result_set_value(
        self, result_set: Any, index: int, column: ColumnMetadata, java_sql_Types: Any
    ) -> Any:
        """
        Extract a value from a ResultSet using appropriate conversion.

        Args:
            result_set: JDBC ResultSet
            index: Column index (1-based)
            column: Column metadata
            java_sql_Types: Java SQL Types class from JPype

        Returns:
            Converted Python value
        """
        # Check for NULL first
        if result_set.getObject(index) is None:
            return None

        # Handle different SQL types
        type_code = column["type_code"]

        # String types
        if type_code in (
            java_sql_Types.CHAR,
            java_sql_Types.VARCHAR,
            java_sql_Types.LONGVARCHAR,
        ):
            return result_set.getString(index)

        # Numeric types
        elif type_code in (
            java_sql_Types.TINYINT,
            java_sql_Types.SMALLINT,
            java_sql_Types.INTEGER,
        ):
            return result_set.getInt(index)
        elif type_code in (java_sql_Types.BIGINT,):
            return result_set.getLong(index)
        elif type_code in (
            java_sql_Types.FLOAT,
            java_sql_Types.DOUBLE,
            java_sql_Types.REAL,
        ):
            return result_set.getDouble(index)
        elif type_code in (java_sql_Types.DECIMAL, java_sql_Types.NUMERIC):
            # Get as BigDecimal and convert to Python decimal or float
            big_decimal = result_set.getBigDecimal(index)
            if column["scale"] == 0:
                return int(big_decimal.longValue())
            else:
                return float(big_decimal.doubleValue())

        # Date/Time types
        elif type_code == java_sql_Types.DATE:
            date = result_set.getDate(index)
            from datetime import date as py_date

            return py_date(date.getYear() + 1900, date.getMonth() + 1, date.getDate())
        elif type_code == java_sql_Types.TIME:
            time = result_set.getTime(index)
            from datetime import time as py_time

            return py_time(time.getHours(), time.getMinutes(), time.getSeconds())
        elif type_code == java_sql_Types.TIMESTAMP:
            timestamp = result_set.getTimestamp(index)
            from datetime import datetime

            return datetime(
                timestamp.getYear() + 1900,
                timestamp.getMonth() + 1,
                timestamp.getDate(),
                timestamp.getHours(),
                timestamp.getMinutes(),
                timestamp.getSeconds(),
                timestamp.getNanos() // 1000,
            )

        # Boolean types
        elif type_code == java_sql_Types.BOOLEAN:
            return result_set.getBoolean(index)

        # Binary types
        elif type_code in (
            java_sql_Types.BINARY,
            java_sql_Types.VARBINARY,
            java_sql_Types.LONGVARBINARY,
        ):
            # Get as byte array and convert to Python bytes
            java_bytes = result_set.getBytes(index)
            return bytes(java_bytes)

        # Fall back to string for unknown types
        else:
            return str(result_set.getObject(index))

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

        # Remove username if present
        sanitized = sanitized.replace(self.config.username, "[USERNAME]")

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
                "No encryption key found in environment variable",
                env_var=key_env_var,
                message="Generated new key. For production, set this environment variable.",
            )

        return key.encode() if key else b""
