from __future__ import annotations
'\nFilemaker integration configuration.\n\nThis module defines configuration settings and schemas for the Filemaker integration\nvia ODBC, centralizing all configuration in one secure location.\n'
import json
import logging
from typing import Any, Dict, List, Optional, Union
from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
_logger = logging.getLogger('app.core.config.filemaker')
class FilemakerSettings(BaseSettings):
    FILEMAKER_DSN: str
    FILEMAKER_USERNAME: str
    FILEMAKER_PASSWORD: SecretStr
    FILEMAKER_DATABASE: str
    FILEMAKER_SERVER: Optional[str] = None
    FILEMAKER_PORT: int = 2399
    FILEMAKER_SSL: bool = True
    FILEMAKER_DRIVER_PATH: Optional[str] = None
    FILEMAKER_ODBC_DRIVER_NAME: str = 'Filemaker ODBC'
    FILEMAKER_ALLOWED_TABLES: List[str] = []
    FILEMAKER_ALLOWED_LAYOUTS: List[str] = []
    FILEMAKER_CONNECTION_TIMEOUT: int = 30
    FILEMAKER_QUERY_TIMEOUT: int = 60
    FILEMAKER_ENCRYPT_CONNECTION: bool = True
    FILEMAKER_USE_EXTENDED_STATEMENTS: bool = False
    FILEMAKER_SYNC_ENABLED: bool = True
    FILEMAKER_SYNC_INTERVAL: int = 86400
    FILEMAKER_SYNC_LAYOUTS: Dict[str, str] = {}
    FILEMAKER_BATCH_SIZE: int = 1000
    FILEMAKER_MAX_WORKERS: int = 4
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True, extra='ignore', json_schema_extra={'FILEMAKER_ALLOWED_TABLES': {'env_mode': 'str'}, 'FILEMAKER_ALLOWED_LAYOUTS': {'env_mode': 'str'}, 'FILEMAKER_SYNC_LAYOUTS': {'env_mode': 'str'}})
    @field_validator('FILEMAKER_ALLOWED_TABLES', 'FILEMAKER_ALLOWED_LAYOUTS', mode='before')
    @classmethod
    def parse_str_to_list(cls, v: Any) -> List[str]:
        if isinstance(v, str):
            if not v:
                return []
            if ',' in v:
                return [item.strip() for item in v.split(',')]
            return [v.strip()]
        return v
    @field_validator('FILEMAKER_PORT')
    @classmethod
    def validate_port(cls, v: Optional[Union[int, str]]) -> Optional[int]:
        if v is None:
            return 2399
        if isinstance(v, str):
            try:
                v = int(v)
            except ValueError:
                raise ValueError(f'Invalid port number: {v}')
        if v < 1 or v > 65535:
            raise ValueError(f'Port must be between 1 and 65535, got {v}')
        return v
    @field_validator('FILEMAKER_SYNC_INTERVAL')
    @classmethod
    def validate_interval(cls, v: Union[int, str]) -> int:
        if isinstance(v, str):
            try:
                v = int(v)
            except ValueError:
                raise ValueError(f'Invalid sync interval: {v}')
        if v < 300:
            _logger.warning(f'FILEMAKER_SYNC_INTERVAL too small ({v}s), setting to 300s minimum')
            return 300
        return v
    @field_validator('FILEMAKER_SYNC_LAYOUTS', mode='before')
    @classmethod
    def parse_sync_layouts(cls, v: Union[str, Dict[str, str]]) -> Dict[str, str]:
        if isinstance(v, str):
            if not v:
                return {}
            try:
                return json.loads(v)
            except json.JSONDecodeError as e:
                if ':' in v and ',' in v:
                    result = {}
                    pairs = v.split(',')
                    for pair in pairs:
                        if ':' in pair:
                            key, value = pair.split(':', 1)
                            result[key.strip()] = value.strip()
                    return result
                _logger.error(f'Failed to parse FILEMAKER_SYNC_LAYOUTS: {e}')
                raise ValueError(f'Invalid format in FILEMAKER_SYNC_LAYOUTS: {e}')
        return v
    @field_validator('FILEMAKER_SSL', 'FILEMAKER_ENCRYPT_CONNECTION', 'FILEMAKER_SYNC_ENABLED', 'FILEMAKER_USE_EXTENDED_STATEMENTS', mode='before')
    @classmethod
    def parse_boolean(cls, v: Any) -> bool:
        if isinstance(v, str):
            if v.lower() in ('true', '1', 'yes', 'y', 't'):
                return True
            elif v.lower() in ('false', '0', 'no', 'n', 'f'):
                return False
            raise ValueError(f'Invalid boolean value: {v}')
        return v
filemaker_settings = FilemakerSettings()
def get_filemaker_connector_config() -> Dict[str, Any]:
    from app.logging import get_logger
    logger = get_logger('app.core.config.filemaker')
    logger.debug('Retrieving Filemaker connector configuration')
    return {'dsn': filemaker_settings.FILEMAKER_DSN, 'username': filemaker_settings.FILEMAKER_USERNAME, 'password': filemaker_settings.FILEMAKER_PASSWORD, 'database': filemaker_settings.FILEMAKER_DATABASE, 'server': filemaker_settings.FILEMAKER_SERVER, 'port': filemaker_settings.FILEMAKER_PORT, 'ssl': filemaker_settings.FILEMAKER_SSL, 'driver_path': filemaker_settings.FILEMAKER_DRIVER_PATH, 'driver_name': filemaker_settings.FILEMAKER_ODBC_DRIVER_NAME, 'allowed_tables': filemaker_settings.FILEMAKER_ALLOWED_TABLES, 'allowed_layouts': filemaker_settings.FILEMAKER_ALLOWED_LAYOUTS, 'connection_timeout': filemaker_settings.FILEMAKER_CONNECTION_TIMEOUT, 'query_timeout': filemaker_settings.FILEMAKER_QUERY_TIMEOUT, 'encrypt_connection': filemaker_settings.FILEMAKER_ENCRYPT_CONNECTION, 'use_extended_statements': filemaker_settings.FILEMAKER_USE_EXTENDED_STATEMENTS}