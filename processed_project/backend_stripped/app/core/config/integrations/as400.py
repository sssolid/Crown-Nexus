from __future__ import annotations
'\nAS400 integration configuration.\n\nThis module defines configuration settings and schemas for the AS400 integration,\ncentralizing all configuration in one secure location.\n'
import json
import logging
from typing import Any, Dict, List, Optional, Union
from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
_logger = logging.getLogger('app.core.config.as400')
class AS400Settings(BaseSettings):
    JT400_JAR_PATH: str
    AS400_USERNAME: str
    AS400_PASSWORD: SecretStr
    AS400_DATABASE: str
    AS400_SERVER: Optional[str] = None
    AS400_PORT: Optional[int] = None
    AS400_SSL: bool = True
    AS400_ALLOWED_TABLES: List[str] = []
    AS400_ALLOWED_SCHEMAS: List[str] = []
    AS400_CONNECTION_TIMEOUT: int = 30
    AS400_QUERY_TIMEOUT: int = 60
    AS400_ENCRYPT_CONNECTION: bool = True
    AS400_ENABLE_SSL_PARAM: bool = True
    AS400_ENABLE_READONLY_PARAM: bool = True
    AS400_SYNC_ENABLED: bool = True
    AS400_SYNC_INTERVAL: int = 86400
    AS400_SYNC_TABLES: Dict[str, str] = {}
    AS400_BATCH_SIZE: int = 1000
    AS400_MAX_WORKERS: int = 4
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True, extra='ignore', json_schema_extra={'AS400_ALLOWED_TABLES': {'env_mode': 'str'}, 'AS400_ALLOWED_SCHEMAS': {'env_mode': 'str'}, 'AS400_SYNC_TABLES': {'env_mode': 'str'}})
    @field_validator('AS400_ALLOWED_TABLES', 'AS400_ALLOWED_SCHEMAS', mode='before')
    @classmethod
    def parse_str_to_list(cls, v: Any) -> List[str]:
        if isinstance(v, str):
            if not v:
                return []
            if ',' in v:
                return [item.strip().upper() for item in v.split(',')]
            return [v.strip().upper()]
        return [item.upper() for item in v]
    @field_validator('AS400_PORT')
    @classmethod
    def validate_port(cls, v: Optional[Union[int, str]]) -> Optional[int]:
        if v is None:
            return None
        if isinstance(v, str):
            try:
                v = int(v)
            except ValueError:
                raise ValueError(f'Invalid port number: {v}')
        if v < 1 or v > 65535:
            raise ValueError(f'Port must be between 1 and 65535, got {v}')
        return v
    @field_validator('AS400_SYNC_INTERVAL')
    @classmethod
    def validate_interval(cls, v: Union[int, str]) -> int:
        if isinstance(v, str):
            try:
                v = int(v)
            except ValueError:
                raise ValueError(f'Invalid sync interval: {v}')
        if v < 300:
            _logger.warning(f'AS400_SYNC_INTERVAL too small ({v}s), setting to 300s minimum')
            return 300
        return v
    @field_validator('AS400_SYNC_TABLES', mode='before')
    @classmethod
    def parse_sync_tables(cls, v: Union[str, Dict[str, str]]) -> Dict[str, str]:
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
                _logger.error(f'Failed to parse AS400_SYNC_TABLES: {e}')
                raise ValueError(f'Invalid format in AS400_SYNC_TABLES: {e}')
        return v
    @field_validator('AS400_SSL', 'AS400_ENCRYPT_CONNECTION', 'AS400_SYNC_ENABLED', mode='before')
    @classmethod
    def parse_boolean(cls, v: Any) -> bool:
        if isinstance(v, str):
            if v.lower() in ('true', '1', 'yes', 'y', 't'):
                return True
            elif v.lower() in ('false', '0', 'no', 'n', 'f'):
                return False
            raise ValueError(f'Invalid boolean value: {v}')
        return v
as400_settings = AS400Settings()
def get_as400_connector_config() -> Dict[str, Any]:
    from app.logging import get_logger
    logger = get_logger('app.core.config.as400')
    logger.debug('Retrieving AS400 connector configuration')
    return {'jt400_jar_path': as400_settings.JT400_JAR_PATH, 'username': as400_settings.AS400_USERNAME, 'password': as400_settings.AS400_PASSWORD, 'database': as400_settings.AS400_DATABASE, 'server': as400_settings.AS400_SERVER, 'port': as400_settings.AS400_PORT, 'ssl': as400_settings.AS400_SSL, 'allowed_tables': as400_settings.AS400_ALLOWED_TABLES, 'allowed_schemas': as400_settings.AS400_ALLOWED_SCHEMAS, 'connection_timeout': as400_settings.AS400_CONNECTION_TIMEOUT, 'query_timeout': as400_settings.AS400_QUERY_TIMEOUT, 'encrypt_connection': as400_settings.AS400_ENCRYPT_CONNECTION}