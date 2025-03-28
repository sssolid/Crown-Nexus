from __future__ import annotations
'\nBase application configuration settings.\n\nThis module defines fundamental settings for the application including\nenvironment, logging configuration, and basic application information.\n'
from enum import Enum
from pathlib import Path
from typing import Any, List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
class Environment(str, Enum):
    DEVELOPMENT = 'development'
    STAGING = 'staging'
    PRODUCTION = 'production'
class LogLevel(str, Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'
class BaseAppSettings(BaseSettings):
    PROJECT_NAME: str = 'Crown Nexus'
    DESCRIPTION: str = 'B2B platform for automotive aftermarket industry'
    VERSION: str = '0.1.0'
    API_V1_STR: str = '/api/v1'
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent
    DEFAULT_LOCALE: str = 'en'
    AVAILABLE_LOCALES: Union[List[str], str] = ['en', 'es', 'fr', 'de']
    LOG_LEVEL: LogLevel = LogLevel.INFO
    LOG_FORMAT: str = 'text'
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True, extra='ignore', json_schema_extra={'AVAILABLE_LOCALES': {'env_mode': 'str'}})
    @field_validator('AVAILABLE_LOCALES', mode='before')
    @classmethod
    def parse_str_to_list(cls, v: Any) -> List[str]:
        if isinstance(v, str):
            if not v:
                return []
            if ',' in v:
                return [item.strip() for item in v.split(',')]
            return [v.strip()]
        return v