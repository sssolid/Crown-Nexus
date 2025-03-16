from __future__ import annotations
import os
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from pydantic import AnyHttpUrl, DirectoryPath, PostgresDsn, validator
from pydantic_settings import BaseSettings
class Environment(str, Enum):
    DEVELOPMENT = 'development'
    STAGING = 'staging'
    PRODUCTION = 'production'
class Settings(BaseSettings):
    PROJECT_NAME: str = 'Crown Nexus'
    DESCRIPTION: str = 'B2B platform for automotive aftermarket industry'
    VERSION: str = '0.1.0'
    API_V1_STR: str = '/api/v1'
    SECRET_KEY: str = 'your-secret-key-change-in-production'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    @validator('BACKEND_CORS_ORIGINS', pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and (not v.startswith('[')):
            return [i.strip() for i in v.split(',')]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    POSTGRES_SERVER: str = 'localhost'
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'postgres'
    POSTGRES_DB: str = 'crown_nexus'
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    @validator('SQLALCHEMY_DATABASE_URI', pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        user = values.get('POSTGRES_USER', '')
        password = values.get('POSTGRES_PASSWORD', '')
        server = values.get('POSTGRES_SERVER', '')
        db = values.get('POSTGRES_DB', '')
        if not all([user, password, server, db]):
            return None
        return f'postgresql+asyncpg://{user}:{password}@{server}/{db}'
    ELASTICSEARCH_HOST: str = 'localhost'
    ELASTICSEARCH_PORT: int = 9200
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    DEFAULT_LOCALE: str = 'en'
    AVAILABLE_LOCALES: List[str] = ['en', 'es', 'fr', 'de']
    CHAT_ENCRYPTION_SALT: str = ''
    CHAT_MESSAGE_LIMIT: int = 50
    CHAT_RATE_LIMIT_PER_MINUTE: int = 60
    CHAT_WEBSOCKET_KEEPALIVE: int = 30
    CHAT_MAX_MESSAGE_LENGTH: int = 5000
    EXCHANGE_RATE_API_KEY: str = ''
    EXCHANGE_RATE_UPDATE_FREQUENCY: int = 24
    STORE_INVERSE_RATES: bool = True
    VCDB_PATH: str = 'data/vcdb.accdb'
    PCDB_PATH: str = 'data/pcdb.accdb'
    MODEL_MAPPINGS_PATH: Optional[str] = None
    FITMENT_DB_URL: Optional[str] = None
    FITMENT_LOG_LEVEL: str = 'INFO'
    FITMENT_CACHE_SIZE: int = 100
    MEDIA_ROOT: DirectoryPath = 'media'
    MEDIA_URL: str = '/media/'
    MEDIA_STORAGE_TYPE: str = 'local'
    MEDIA_CDN_URL: Optional[str] = None
    @validator('MEDIA_ROOT', pre=True)
    def create_media_directories(cls, v: str) -> str:
        os.makedirs(v, exist_ok=True)
        for media_type in ['image', 'document', 'video', 'other', 'thumbnails']:
            os.makedirs(os.path.join(v, media_type), exist_ok=True)
        return v
    @property
    def media_base_url(self) -> str:
        if self.ENVIRONMENT == Environment.PRODUCTION and self.MEDIA_CDN_URL:
            return self.MEDIA_CDN_URL
        return self.MEDIA_URL
    class Config:
        case_sensitive = True
        env_file = '.env'
settings = Settings()