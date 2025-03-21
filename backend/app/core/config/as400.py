from __future__ import annotations

"""
AS400 integration configuration.

This module defines configuration settings and schemas for the AS400 integration,
centralizing all configuration in one secure location.
"""

import os
from typing import Dict, List, Optional, Set
from pydantic import BaseSettings, Field, SecretStr, validator

from app.core.logging import get_logger

logger = get_logger("app.core.config.as400")


class AS400Settings(BaseSettings):
    """
    AS400 connection and synchronization settings.

    All sensitive settings can be provided via environment variables
    for enhanced security.
    """

    # Connection settings
    AS400_DSN: str = Field(..., description="ODBC Data Source Name for AS400")
    AS400_USERNAME: str = Field(..., description="AS400 username")
    AS400_PASSWORD: SecretStr = Field(..., description="AS400 password")
    AS400_DATABASE: str = Field(..., description="AS400 database/library")
    AS400_SERVER: Optional[str] = Field(None, description="AS400 server hostname")
    AS400_PORT: Optional[int] = Field(None, description="AS400 server port")
    AS400_SSL: bool = Field(True, description="Use SSL for connection")

    # Security settings
    AS400_ALLOWED_TABLES: List[str] = Field(
        [], description="Whitelist of allowed tables"
    )
    AS400_ALLOWED_SCHEMAS: List[str] = Field(
        [], description="Whitelist of allowed schemas/libraries"
    )
    AS400_CONNECTION_TIMEOUT: int = Field(
        30, description="Connection timeout in seconds"
    )
    AS400_QUERY_TIMEOUT: int = Field(
        60, description="Query timeout in seconds"
    )
    AS400_ENCRYPT_CONNECTION: bool = Field(
        True, description="Encrypt connection parameters"
    )

    # Sync settings
    AS400_SYNC_ENABLED: bool = Field(
        True, description="Enable AS400 synchronization"
    )
    AS400_SYNC_INTERVAL: int = Field(
        86400, description="Sync interval in seconds (default: daily)"
    )
    AS400_SYNC_TABLES: Dict[str, str] = Field(
        {}, description="Mapping of AS400 tables to local models"
    )
    AS400_BATCH_SIZE: int = Field(
        1000, description="Batch size for processing records"
    )
    AS400_MAX_WORKERS: int = Field(
        4, description="Maximum number of sync workers"
    )

    @validator("AS400_ALLOWED_TABLES", "AS400_ALLOWED_SCHEMAS")
    def uppercase_tables_schemas(cls, v: List[str]) -> List[str]:
        """Convert table and schema names to uppercase for consistency."""
        return [x.upper() for x in v]

    @validator("AS400_PORT")
    def validate_port(cls, v: Optional[int]) -> Optional[int]:
        """Validate port is within allowed range."""
        if v is not None and (v < 1 or v > 65535):
            raise ValueError("Port must be between 1 and 65535")
        return v

    @validator("AS400_SYNC_INTERVAL")
    def validate_interval(cls, v: int) -> int:
        """Validate sync interval is reasonable."""
        if v < 300:  # 5 minutes minimum
            logger.warning(
                f"AS400_SYNC_INTERVAL too small ({v}s), setting to 300s minimum"
            )
            return 300
        return v

    class Config:
        """Pydantic config for AS400 settings."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Load settings from environment variables
as400_settings = AS400Settings()


def get_as400_connector_config() -> Dict[str, any]:
    """
    Get AS400 connector configuration from settings.

    Returns:
        Dictionary with AS400 connector configuration
    """
    return {
        "dsn": as400_settings.AS400_DSN,
        "username": as400_settings.AS400_USERNAME,
        "password": as400_settings.AS400_PASSWORD,
        "database": as400_settings.AS400_DATABASE,
        "server": as400_settings.AS400_SERVER,
        "port": as400_settings.AS400_PORT,
        "ssl": as400_settings.AS400_SSL,
        "allowed_tables": as400_settings.AS400_ALLOWED_TABLES,
        "allowed_schemas": as400_settings.AS400_ALLOWED_SCHEMAS,
        "connection_timeout": as400_settings.AS400_CONNECTION_TIMEOUT,
        "query_timeout": as400_settings.AS400_QUERY_TIMEOUT,
        "encrypt_connection": as400_settings.AS400_ENCRYPT_CONNECTION,
    }
