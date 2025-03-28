from __future__ import annotations
'\nAS400 connector for data import.\n\nThis module provides a secure connector for extracting data from AS400/iSeries\ndatabases while implementing strict security measures to protect sensitive data.\n'
import os
from typing import Any, Dict, List, Optional, Set
import pyodbc
from pydantic import BaseModel, Field, SecretStr, validator
from cryptography.fernet import Fernet
from app.core.exceptions import DatabaseException, SecurityException
from app.logging import get_logger
logger = get_logger('app.data_import.connectors.as400_connector')
class AS400ConnectionConfig(BaseModel):
    dsn: str = Field(..., description='ODBC Data Source Name')
    username: str = Field(..., description='AS400 username (read-only account)')
    password: SecretStr = Field(..., description='AS400 password')
    database: str = Field(..., description='AS400 database/library name')
    server: Optional[str] = Field(None, description='AS400 server address')
    port: Optional[int] = Field(None, description='AS400 server port')
    ssl: bool = Field(True, description='Use SSL for connection')
    allowed_tables: Optional[List[str]] = Field(None, description='Whitelist of allowed tables')
    allowed_schemas: Optional[List[str]] = Field(None, description='Whitelist of allowed schemas/libraries')
    connection_timeout: int = Field(30, description='Connection timeout in seconds')
    query_timeout: int = Field(60, description='Query timeout in seconds')
    encrypt_connection: bool = Field(True, description='Encrypt connection parameters')
    @validator('port')
    def validate_port(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and (v < 1 or v > 65535):
            raise ValueError('Port must be between 1 and 65535')
        return v
    @validator('allowed_tables', 'allowed_schemas')
    def validate_allowed_lists(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        if v is not None:
            return [item.upper() for item in v]
        return v
    class Config:
        validate_assignment = True
        extra = 'forbid'
class AS400Connector:
    def __init__(self, config: AS400ConnectionConfig) -> None:
        self.config = config
        self.connection = None
        self._encryption_key = self._get_encryption_key()
        self._accessed_tables: Set[str] = set()
        logger.debug(f"AS400Connector initialized for DSN: {config.dsn}, Server: {config.server or 'from DSN'}, Database: {config.database}")
    async def connect(self) -> None:
        try:
            connection_string = self._build_connection_string()
            logger.info(f'Connecting to AS400 database: {self.config.database} on DSN: {self.config.dsn}')
            try:
                self.connection = pyodbc.connect(connection_string)
            except pyodbc.Error as e:
                logger.debug(f'Connection attempt failed: {str(e)}, retrying with different parameters')
                self.connection = pyodbc.connect(connection_string)
            if self.connection:
                try:
                    self.connection.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
                    self.connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
                    self.connection.setencoding(encoding='utf-8')
                except (pyodbc.Error, AttributeError) as e:
                    logger.debug(f'Could not set encoding: {str(e)}')
                try:
                    if hasattr(self.connection, 'timeout'):
                        self.connection.timeout = self.config.query_timeout
                except (pyodbc.Error, AttributeError) as e:
                    logger.debug(f'Could not set timeout: {str(e)}')
            logger.info(f'Successfully connected to AS400 database: {self.config.database}')
        except pyodbc.Error as e:
            error_msg = str(e)
            sanitized_error = self._sanitize_error_message(error_msg)
            logger.error(f'Failed to connect to AS400: {sanitized_error}')
            if 'permission' in error_msg.lower() or 'access denied' in error_msg.lower():
                raise SecurityException(message=f'Security error connecting to AS400: {sanitized_error}', original_exception=e)
            else:
                raise DatabaseException(message=f'Failed to connect to AS400 database: {sanitized_error}', original_exception=e)
    async def extract(self, query: str, limit: Optional[int]=None, **params: Any) -> List[Dict[str, Any]]:
        if not self.connection:
            await self.connect()
        table_name = self._validate_and_prepare_query(query, limit)
        try:
            cursor = self.connection.cursor()
            sanitized_query = self._sanitize_sql_for_logging(query)
            logger.debug(f'Executing AS400 query: {sanitized_query}')
            if params:
                cursor.execute(query, tuple(params.values()))
            else:
                cursor.execute(query)
            if table_name:
                self._accessed_tables.add(table_name.upper())
            columns = [column[0] for column in cursor.description]
            results = []
            for row in cursor.fetchall():
                result_dict = dict(zip(columns, row))
                results.append(self._convert_as400_types(result_dict))
            logger.info(f"Successfully extracted {len(results)} records from AS400 {('table: ' + table_name if table_name else 'query')}")
            return results
        except pyodbc.Error as e:
            error_msg = str(e)
            sanitized_error = self._sanitize_error_message(error_msg)
            logger.error(f'Error extracting data from AS400: {sanitized_error}')
            if 'permission' in error_msg.lower() or 'access denied' in error_msg.lower():
                raise SecurityException(message=f'Security error accessing AS400 data: {sanitized_error}', original_exception=e)
            else:
                raise DatabaseException(message=f'Failed to extract data from AS400: {sanitized_error}', original_exception=e)
    async def close(self) -> None:
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
                logger.debug('AS400 connection closed')
                if self._accessed_tables:
                    logger.info(f"AS400 session accessed the following tables: {', '.join(sorted(self._accessed_tables))}")
            except pyodbc.Error as e:
                logger.error(f'Error closing AS400 connection: {str(e)}')
                raise DatabaseException(message=f'Failed to close AS400 connection: {str(e)}', original_exception=e)
    def _build_connection_string(self) -> str:
        connection_string = f'DSN={self.config.dsn};UID={self.config.username};PWD={self.config.password.get_secret_value()};DATABASE={self.config.database};'
        if self.config.server:
            connection_string += f'SYSTEM={self.config.server};'
        if self.config.port:
            connection_string += f'PORT={self.config.port};'
        if self.config.ssl and os.environ.get('AS400_ENABLE_SSL_PARAM', '').lower() == 'true':
            connection_string += 'SSLCONNECTION=TRUE;'
        if os.environ.get('AS400_ENABLE_READONLY_PARAM', '').lower() == 'true':
            connection_string += 'ReadOnly=True;'
        connection_string += 'ReadOnly=True;'
        return connection_string
    def _validate_and_prepare_query(self, query: str, limit: Optional[int]) -> Optional[str]:
        if ' ' not in query:
            table_name = query.strip()
            if self.config.allowed_tables:
                if table_name.upper() not in self.config.allowed_tables:
                    raise SecurityException(message=f"Access to table '{table_name}' is not allowed")
            limit_clause = f' FETCH FIRST {limit} ROWS ONLY' if limit is not None else ''
            query = f'SELECT * FROM "{table_name}"{limit_clause}'
            return table_name
        else:
            query_upper = query.upper()
            if any((write_op in query_upper for write_op in ['INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 'ALTER', 'TRUNCATE', 'GRANT', 'REVOKE', 'RENAME'])):
                raise SecurityException(message='Write operations are not allowed on AS400 connection')
            if limit is not None and 'LIMIT' not in query_upper and ('FETCH FIRST' not in query_upper):
                if ';' in query:
                    query = query.rstrip(';')
                query = f'{query} FETCH FIRST {limit} ROWS ONLY'
            return None
    def _convert_as400_types(self, row: Dict[str, Any]) -> Dict[str, Any]:
        result = {}
        for key, value in row.items():
            if hasattr(value, 'real') and (not isinstance(value, (int, float))):
                result[key] = float(value)
            elif hasattr(value, 'isoformat'):
                result[key] = value
            else:
                result[key] = value
        return result
    def _sanitize_sql_for_logging(self, query: str) -> str:
        return query.replace('\n', ' ').replace('\r', ' ')
    def _sanitize_error_message(self, error_message: str) -> str:
        sanitized = error_message.replace(self.config.password.get_secret_value(), '[REDACTED]')
        return sanitized
    def _get_encryption_key(self) -> bytes:
        key_env_var = 'AS400_ENCRYPTION_KEY'
        key = os.environ.get(key_env_var)
        if not key and self.config.encrypt_connection:
            key = Fernet.generate_key().decode()
            logger.warning(f'No encryption key found in environment variable {key_env_var}. Generated new key. For production, set this environment variable.')
        return key.encode() if key else b''