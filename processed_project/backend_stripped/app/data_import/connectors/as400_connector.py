from __future__ import annotations
'\nAS400 connector for data import.\n\nThis module provides a secure connector for extracting data from AS400/iSeries\ndatabases using the JTOpen (JT400) Java library via JPype while implementing\nstrict security measures to protect sensitive data.\n'
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
from app.core.exceptions import DatabaseException, SecurityException, ConfigurationException
from app.logging import get_logger
logger = get_logger('app.data_import.connectors.as400_connector')
class AS400ConnectionConfig(BaseModel):
    jt400_jar_path: str = Field(..., description='Path to the jt400.jar file for Java connection')
    server: str = Field(..., description='AS400 server address')
    username: str = Field(..., description='AS400 username (read-only account)')
    password: SecretStr = Field(..., description='AS400 password')
    database: str = Field(..., description='AS400 database/library name')
    port: Optional[int] = Field(None, description='AS400 server port (default: 446)')
    ssl: bool = Field(True, description='Use SSL for connection')
    allowed_tables: Optional[List[str]] = Field(None, description='Whitelist of allowed tables')
    allowed_schemas: Optional[List[str]] = Field(None, description='Whitelist of allowed schemas/libraries')
    connection_timeout: int = Field(30, description='Connection timeout in seconds')
    query_timeout: int = Field(60, description='Query timeout in seconds')
    encrypt_connection: bool = Field(True, description='Encrypt connection parameters')
    @validator('jt400_jar_path')
    def validate_jar_path(cls, v: str) -> str:
        jar_path = Path(v)
        if not jar_path.exists() or not jar_path.is_file():
            raise ValueError(f'jt400.jar file not found at: {v}')
        return v
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
class ColumnMetadata(TypedDict):
    name: str
    type_name: str
    type_code: int
    precision: int
    scale: int
    nullable: bool
@dataclass
class AS400Connection:
    connection: Any
    jdbc_url: str
    properties: Dict[str, str] = field(default_factory=dict)
    accessed_tables: Set[str] = field(default_factory=set)
class AS400Connector:
    def __init__(self, config: AS400ConnectionConfig) -> None:
        self.config = config
        self._connection: Optional[AS400Connection] = None
        self._encryption_key = self._get_encryption_key()
        try:
            import jpype
            from jpype.types import JException
            self._jpype = jpype
            self._JException = JException
            self._initialize_jpype()
        except ImportError:
            raise ImportError("jpype module is required for JT400 connections. Please install it with 'pip install jpype1'.")
        logger.debug('AS400Connector initialized', server=config.server, database=config.database)
    @cache
    def _initialize_jpype(self) -> None:
        jpype = self._jpype
        if not jpype.isJVMStarted():
            jpype.startJVM(classpath=[self.config.jt400_jar_path], convertStrings=True)
            logger.debug('JVM started for JT400 access')
            try:
                driver_class = jpype.JClass('com.ibm.as400.access.AS400JDBCDriver')
                driver = driver_class()
                jpype.JClass('java.sql.DriverManager').registerDriver(driver)
                logger.debug('AS400 JDBC driver registered successfully')
            except Exception as e:
                logger.warning('Could not register AS400 JDBC driver explicitly', error=str(e))
    async def connect(self) -> None:
        jpype = self._jpype
        JException = self._JException
        try:
            java_sql_DriverManager = jpype.JClass('java.sql.DriverManager')
            java_util_Properties = jpype.JClass('java.util.Properties')
            jdbc_url = self._build_jdbc_url()
            properties = java_util_Properties()
            properties.setProperty('user', self.config.username)
            properties.setProperty('password', self.config.password.get_secret_value())
            properties.setProperty('secure', 'true' if self.config.ssl else 'false')
            properties.setProperty('prompt', 'false')
            properties.setProperty('libraries', self.config.database)
            properties.setProperty('login timeout', str(self.config.connection_timeout))
            properties.setProperty('query timeout', str(self.config.query_timeout))
            properties.setProperty('transaction isolation', 'read committed')
            properties.setProperty('date format', 'iso')
            properties.setProperty('errors', 'full')
            properties.setProperty('access', 'read only')
            logger.info('Connecting to AS400 database', database=self.config.database, server=self.config.server, ssl=self.config.ssl)
            conn = java_sql_DriverManager.getConnection(jdbc_url, properties)
            conn.setAutoCommit(True)
            conn.setReadOnly(True)
            props_dict = {}
            prop_keys = properties.keySet().toArray()
            for key in prop_keys:
                str_key = str(key)
                if str_key != 'password':
                    props_dict[str_key] = str(properties.getProperty(str_key))
            self._connection = AS400Connection(connection=conn, jdbc_url=jdbc_url, properties=props_dict)
            logger.info('Successfully connected to AS400 database', database=self.config.database, server=self.config.server)
        except JException as e:
            error_msg = str(e)
            sanitized_error = self._sanitize_error_message(error_msg)
            logger.error('Failed to connect to AS400', error=sanitized_error, exc_info=True)
            if 'permission' in error_msg.lower() or 'access denied' in error_msg.lower() or 'authorization' in error_msg.lower():
                raise SecurityException(message=f'Security error connecting to AS400: {sanitized_error}', original_exception=e)
            else:
                raise DatabaseException(message=f'Failed to connect to AS400 database: {sanitized_error}', original_exception=e)
    async def extract(self, query: str, limit: Optional[int]=None, **params: Any) -> List[Dict[str, Any]]:
        if not self._connection:
            await self.connect()
        connection = cast(AS400Connection, self._connection)
        jpype = self._jpype
        JException = self._JException
        table_name = self._validate_and_prepare_query(query, limit)
        try:
            java_sql_Types = jpype.JClass('java.sql.Types')
            sanitized_query = self._sanitize_sql_for_logging(query)
            logger.debug('Executing AS400 query', query=sanitized_query, limit=limit)
            if params:
                query, param_values = self._convert_to_prepared_statement(query, params)
                statement = connection.connection.prepareStatement(query)
                for i, value in enumerate(param_values):
                    self._set_prepared_statement_parameter(statement, i + 1, value, java_sql_Types)
                statement.setQueryTimeout(self.config.query_timeout)
                result_set = statement.executeQuery()
            else:
                statement = connection.connection.createStatement()
                statement.setQueryTimeout(self.config.query_timeout)
                result_set = statement.executeQuery(query)
            if table_name:
                connection.accessed_tables.add(table_name.upper())
            results = self._process_result_set(result_set, java_sql_Types)
            result_set.close()
            statement.close()
            logger.info('Successfully extracted records from AS400', record_count=len(results), table=table_name if table_name else None)
            return results
        except JException as e:
            error_msg = str(e)
            sanitized_error = self._sanitize_error_message(error_msg)
            logger.error('Error extracting data from AS400', error=sanitized_error, query=self._sanitize_sql_for_logging(query), exc_info=True)
            if 'permission' in error_msg.lower() or 'access denied' in error_msg.lower() or 'authorization' in error_msg.lower():
                raise SecurityException(message=f'Security error accessing AS400 data: {sanitized_error}', original_exception=e)
            else:
                raise DatabaseException(message=f'Failed to extract data from AS400: {sanitized_error}', original_exception=e)
    async def close(self) -> None:
        if self._connection:
            try:
                connection = self._connection
                connection.connection.close()
                self._connection = None
                logger.debug('AS400 connection closed')
                if connection.accessed_tables:
                    logger.info('AS400 session accessed tables', tables=sorted(connection.accessed_tables))
            except self._JException as e:
                logger.error('Error closing AS400 connection', error=str(e), exc_info=True)
                raise DatabaseException(message=f'Failed to close AS400 connection: {str(e)}', original_exception=e)
    def _build_jdbc_url(self) -> str:
        jdbc_url = f'jdbc:as400://{self.config.server}'
        if self.config.port:
            jdbc_url += f':{self.config.port}'
        params = []
        if self.config.database:
            params.append(f'libraries={self.config.database}')
        if self.config.ssl:
            params.append('secure=true')
        if params:
            jdbc_url += ';' + ';'.join(params)
        return jdbc_url
    def _validate_and_prepare_query(self, query: str, limit: Optional[int]) -> Optional[str]:
        if ' ' not in query:
            table_name = query.strip()
            if self.config.allowed_tables:
                if table_name.upper() not in self.config.allowed_tables:
                    raise SecurityException(message=f"Access to table '{table_name}' is not allowed")
            full_table_name = f'{self.config.database}.{table_name}'
            limit_clause = f' FETCH FIRST {limit} ROWS ONLY' if limit is not None else ''
            query = f'SELECT * FROM {full_table_name}{limit_clause}'
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
    def _convert_to_prepared_statement(self, query: str, params: Dict[str, Any]) -> tuple[str, List[Any]]:
        param_names = re.findall(':(\\w+)', query)
        param_values = []
        for name in param_names:
            if name not in params:
                raise ValueError(f"Parameter '{name}' not provided in params dictionary")
            param_values.append(params[name])
            query = query.replace(f':{name}', '?', 1)
        return (query, param_values)
    def _set_prepared_statement_parameter(self, statement: Any, index: int, value: Any, java_sql_Types: Any) -> None:
        jpype = self._jpype
        if value is None:
            statement.setNull(index, java_sql_Types.NULL)
            return
        if isinstance(value, str):
            statement.setString(index, value)
        elif isinstance(value, int):
            statement.setInt(index, value)
        elif isinstance(value, float):
            statement.setDouble(index, value)
        elif isinstance(value, bool):
            statement.setBoolean(index, value)
        elif hasattr(value, 'isoformat'):
            if hasattr(value, 'hour'):
                timestamp = jpype.JClass('java.sql.Timestamp')
                mills = int(value.timestamp() * 1000)
                statement.setTimestamp(index, timestamp(mills))
            else:
                date = jpype.JClass('java.sql.Date')
                mills = int(value.toordinal() * 86400 * 1000)
                statement.setDate(index, date(mills))
        else:
            statement.setString(index, str(value))
    def _process_result_set(self, result_set: Any, java_sql_Types: Any) -> List[Dict[str, Any]]:
        meta = result_set.getMetaData()
        column_count = meta.getColumnCount()
        columns: List[ColumnMetadata] = []
        for i in range(1, column_count + 1):
            columns.append({'name': meta.getColumnName(i), 'type_name': meta.getColumnTypeName(i), 'type_code': meta.getColumnType(i), 'precision': meta.getPrecision(i), 'scale': meta.getScale(i), 'nullable': meta.isNullable(i) != 0})
        results = []
        while result_set.next():
            row = {}
            for i, col in enumerate(columns, 1):
                value = self._get_result_set_value(result_set, i, col, java_sql_Types)
                row[col['name']] = value
            results.append(row)
        return results
    def _get_result_set_value(self, result_set: Any, index: int, column: ColumnMetadata, java_sql_Types: Any) -> Any:
        if result_set.getObject(index) is None:
            return None
        type_code = column['type_code']
        if type_code in (java_sql_Types.CHAR, java_sql_Types.VARCHAR, java_sql_Types.LONGVARCHAR):
            return result_set.getString(index)
        elif type_code in (java_sql_Types.TINYINT, java_sql_Types.SMALLINT, java_sql_Types.INTEGER):
            return result_set.getInt(index)
        elif type_code in (java_sql_Types.BIGINT,):
            return result_set.getLong(index)
        elif type_code in (java_sql_Types.FLOAT, java_sql_Types.DOUBLE, java_sql_Types.REAL):
            return result_set.getDouble(index)
        elif type_code in (java_sql_Types.DECIMAL, java_sql_Types.NUMERIC):
            big_decimal = result_set.getBigDecimal(index)
            if column['scale'] == 0:
                return int(big_decimal.longValue())
            else:
                return float(big_decimal.doubleValue())
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
            return datetime(timestamp.getYear() + 1900, timestamp.getMonth() + 1, timestamp.getDate(), timestamp.getHours(), timestamp.getMinutes(), timestamp.getSeconds(), timestamp.getNanos() // 1000)
        elif type_code == java_sql_Types.BOOLEAN:
            return result_set.getBoolean(index)
        elif type_code in (java_sql_Types.BINARY, java_sql_Types.VARBINARY, java_sql_Types.LONGVARBINARY):
            java_bytes = result_set.getBytes(index)
            return bytes(java_bytes)
        else:
            return str(result_set.getObject(index))
    def _sanitize_sql_for_logging(self, query: str) -> str:
        return query.replace('\n', ' ').replace('\r', ' ')
    def _sanitize_error_message(self, error_message: str) -> str:
        sanitized = error_message.replace(self.config.password.get_secret_value(), '[REDACTED]')
        sanitized = sanitized.replace(self.config.username, '[USERNAME]')
        return sanitized
    def _get_encryption_key(self) -> bytes:
        key_env_var = 'AS400_ENCRYPTION_KEY'
        key = os.environ.get(key_env_var)
        if not key and self.config.encrypt_connection:
            key = Fernet.generate_key().decode()
            logger.warning('No encryption key found in environment variable', env_var=key_env_var, message='Generated new key. For production, set this environment variable.')
        return key.encode() if key else b''