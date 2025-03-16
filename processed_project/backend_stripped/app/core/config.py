from __future__ import annotations
import os
import secrets
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, DirectoryPath, Field, PostgresDsn, SecretStr, field_validator, model_validator
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
class DatabaseSettings(BaseSettings):
    POSTGRES_SERVER: str = Field('localhost')
    POSTGRES_USER: str = Field('postgres')
    POSTGRES_PASSWORD: str = Field('postgres')
    POSTGRES_DB: str = Field('crown_nexus')
    POSTGRES_PORT: str = Field('5432')
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True)
    @model_validator(mode='after')
    def assemble_db_connection(self) -> 'DatabaseSettings':
        if self.SQLALCHEMY_DATABASE_URI:
            return self
        self.SQLALCHEMY_DATABASE_URI = PostgresDsn.build(scheme='postgresql+asyncpg', username=self.POSTGRES_USER, password=self.POSTGRES_PASSWORD, host=self.POSTGRES_SERVER, port=int(self.POSTGRES_PORT), path=f'{self.POSTGRES_DB}')
        return self
class ElasticsearchSettings(BaseSettings):
    ELASTICSEARCH_HOST: str = Field('localhost')
    ELASTICSEARCH_PORT: int = Field(9200)
    ELASTICSEARCH_USE_SSL: bool = Field(False)
    ELASTICSEARCH_USERNAME: Optional[str] = None
    ELASTICSEARCH_PASSWORD: Optional[SecretStr] = None
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True)
    @property
    def uri(self) -> str:
        protocol = 'https' if self.ELASTICSEARCH_USE_SSL else 'http'
        auth = ''
        if self.ELASTICSEARCH_USERNAME:
            password = self.ELASTICSEARCH_PASSWORD.get_secret_value() if self.ELASTICSEARCH_PASSWORD else ''
            auth = f'{self.ELASTICSEARCH_USERNAME}:{password}@'
        return f'{protocol}://{auth}{self.ELASTICSEARCH_HOST}:{self.ELASTICSEARCH_PORT}'
class RedisSettings(BaseSettings):
    REDIS_HOST: str = Field('localhost')
    REDIS_PORT: int = Field(6379)
    REDIS_PASSWORD: Optional[SecretStr] = None
    REDIS_DB: int = Field(0)
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True)
    @property
    def uri(self) -> str:
        password_part = ''
        if self.REDIS_PASSWORD:
            password_part = f':{self.REDIS_PASSWORD.get_secret_value()}@'
        return f'redis://{password_part}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}'
class LocaleSettings(BaseSettings):
    DEFAULT_LOCALE: str = Field('en')
    AVAILABLE_LOCALES: List[str] = Field(['en', 'es', 'fr', 'de'])
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True)
class ChatSettings(BaseSettings):
    CHAT_ENCRYPTION_SALT: str = Field(default_factory=lambda: secrets.token_hex(16))
    CHAT_MESSAGE_LIMIT: int = Field(50)
    CHAT_RATE_LIMIT_PER_MINUTE: int = Field(60)
    CHAT_WEBSOCKET_KEEPALIVE: int = Field(30)
    CHAT_MAX_MESSAGE_LENGTH: int = Field(5000)
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True)
class FitmentSettings(BaseSettings):
    VCDB_PATH: str = Field('data/vcdb.accdb')
    PCDB_PATH: str = Field('data/pcdb.accdb')
    MODEL_MAPPINGS_PATH: Optional[str] = None
    FITMENT_DB_URL: Optional[str] = None
    FITMENT_LOG_LEVEL: str = Field('INFO')
    FITMENT_CACHE_SIZE: int = Field(100)
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True)
    @model_validator(mode='after')
    def validate_file_paths(self) -> 'FitmentSettings':
        if os.getenv('ENVIRONMENT') == Environment.PRODUCTION.value:
            if not os.path.exists(self.VCDB_PATH):
                raise ValueError(f'VCDB_PATH does not exist: {self.VCDB_PATH}')
            if not os.path.exists(self.PCDB_PATH):
                raise ValueError(f'PCDB_PATH does not exist: {self.PCDB_PATH}')
            if self.MODEL_MAPPINGS_PATH and (not os.path.exists(self.MODEL_MAPPINGS_PATH)):
                raise ValueError(f'MODEL_MAPPINGS_PATH does not exist: {self.MODEL_MAPPINGS_PATH}')
        return self
class CurrencySettings(BaseSettings):
    EXCHANGE_RATE_API_KEY: str = Field('')
    EXCHANGE_RATE_UPDATE_FREQUENCY: int = Field(24)
    STORE_INVERSE_RATES: bool = Field(True)
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True)
class CORSSettings(BaseSettings):
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = Field(default_factory=list)
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True)
    @field_validator('BACKEND_CORS_ORIGINS', mode='before')
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and (not v.startswith('[')):
            return [i.strip() for i in v.split(',')]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
class SecuritySettings(BaseSettings):
    SECRET_KEY: str = Field('your-secret-key-change-in-production')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60 * 24 * 8)
    ALGORITHM: str = Field('HS256')
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True)
class MediaSettings(BaseSettings):
    MEDIA_ROOT: DirectoryPath = Field('media')
    MEDIA_URL: str = Field('/media/')
    MEDIA_STORAGE_TYPE: str = Field('local')
    MEDIA_CDN_URL: Optional[str] = None
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True)
    @field_validator('MEDIA_ROOT', mode='before')
    @classmethod
    def create_media_directories(cls, v: str) -> str:
        os.makedirs(v, exist_ok=True)
        for media_type in ['image', 'document', 'video', 'other', 'thumbnails']:
            os.makedirs(os.path.join(v, media_type), exist_ok=True)
        return v
    @property
    def media_base_url(self) -> str:
        if os.getenv('ENVIRONMENT') == Environment.PRODUCTION.value and self.MEDIA_CDN_URL:
            return self.MEDIA_CDN_URL
        return self.MEDIA_URL
class CelerySettings(BaseSettings):
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True)
class LoggingSettings(BaseSettings):
    LOG_LEVEL: LogLevel = Field(LogLevel.INFO)
    LOG_FORMAT: str = Field('text')
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True)
class Settings(BaseSettings):
    PROJECT_NAME: str = Field('Crown Nexus')
    DESCRIPTION: str = Field('B2B platform for automotive aftermarket industry')
    VERSION: str = Field('0.1.0')
    API_V1_STR: str = Field('/api/v1')
    ENVIRONMENT: Environment = Field(Environment.DEVELOPMENT)
    BASE_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent.parent)
    POSTGRES_SERVER: str = Field('localhost')
    POSTGRES_USER: str = Field('postgres')
    POSTGRES_PASSWORD: str = Field('postgres')
    POSTGRES_DB: str = Field('crown_nexus')
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    ELASTICSEARCH_HOST: str = Field('localhost')
    ELASTICSEARCH_PORT: int = Field(9200)
    REDIS_HOST: str = Field('localhost')
    REDIS_PORT: int = Field(6379)
    SECRET_KEY: str = Field('your-secret-key-change-in-production')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60 * 24 * 8)
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = Field(default_factory=list)
    MEDIA_ROOT: DirectoryPath = Field('media')
    MEDIA_URL: str = Field('/media/')
    MEDIA_STORAGE_TYPE: str = Field('local')
    MEDIA_CDN_URL: Optional[str] = None
    DEFAULT_LOCALE: str = Field('en')
    AVAILABLE_LOCALES: List[str] = Field(['en', 'es', 'fr', 'de'])
    CHAT_ENCRYPTION_SALT: str = Field('')
    CHAT_MESSAGE_LIMIT: int = Field(50)
    CHAT_RATE_LIMIT_PER_MINUTE: int = Field(60)
    CHAT_WEBSOCKET_KEEPALIVE: int = Field(30)
    CHAT_MAX_MESSAGE_LENGTH: int = Field(5000)
    VCDB_PATH: str = Field('data/vcdb.accdb')
    PCDB_PATH: str = Field('data/pcdb.accdb')
    MODEL_MAPPINGS_PATH: Optional[str] = None
    FITMENT_DB_URL: Optional[str] = None
    FITMENT_LOG_LEVEL: str = Field('INFO')
    FITMENT_CACHE_SIZE: int = Field(100)
    EXCHANGE_RATE_API_KEY: str = Field('')
    EXCHANGE_RATE_UPDATE_FREQUENCY: int = Field(24)
    STORE_INVERSE_RATES: bool = Field(True)
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True)
    @field_validator('BACKEND_CORS_ORIGINS', mode='before')
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and (not v.startswith('[')):
            return [i.strip() for i in v.split(',')]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    @field_validator('MEDIA_ROOT', mode='before')
    @classmethod
    def create_media_directories(cls, v: str) -> str:
        os.makedirs(v, exist_ok=True)
        for media_type in ['image', 'document', 'video', 'other', 'thumbnails']:
            os.makedirs(os.path.join(v, media_type), exist_ok=True)
        return v
    @model_validator(mode='after')
    def assemble_db_connection(self) -> 'Settings':
        if not self.SQLALCHEMY_DATABASE_URI:
            self.SQLALCHEMY_DATABASE_URI = PostgresDsn.build(scheme='postgresql+asyncpg', username=self.POSTGRES_USER, password=self.POSTGRES_PASSWORD, host=self.POSTGRES_SERVER, path=f'{self.POSTGRES_DB}')
        return self
    @property
    def media_base_url(self) -> str:
        if self.ENVIRONMENT == Environment.PRODUCTION and self.MEDIA_CDN_URL:
            return self.MEDIA_CDN_URL
        return self.MEDIA_URL
    @property
    def db(self) -> DatabaseSettings:
        return DatabaseSettings(POSTGRES_SERVER=self.POSTGRES_SERVER, POSTGRES_USER=self.POSTGRES_USER, POSTGRES_PASSWORD=self.POSTGRES_PASSWORD, POSTGRES_DB=self.POSTGRES_DB, SQLALCHEMY_DATABASE_URI=self.SQLALCHEMY_DATABASE_URI)
    @property
    def elasticsearch(self) -> ElasticsearchSettings:
        return ElasticsearchSettings(ELASTICSEARCH_HOST=self.ELASTICSEARCH_HOST, ELASTICSEARCH_PORT=self.ELASTICSEARCH_PORT)
    @property
    def redis(self) -> RedisSettings:
        return RedisSettings(REDIS_HOST=self.REDIS_HOST, REDIS_PORT=self.REDIS_PORT)
    @property
    def security(self) -> SecuritySettings:
        return SecuritySettings(SECRET_KEY=self.SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES=self.ACCESS_TOKEN_EXPIRE_MINUTES)
    @property
    def media(self) -> MediaSettings:
        return MediaSettings(MEDIA_ROOT=self.MEDIA_ROOT, MEDIA_URL=self.MEDIA_URL, MEDIA_STORAGE_TYPE=self.MEDIA_STORAGE_TYPE, MEDIA_CDN_URL=self.MEDIA_CDN_URL)
    @property
    def locale(self) -> LocaleSettings:
        return LocaleSettings(DEFAULT_LOCALE=self.DEFAULT_LOCALE, AVAILABLE_LOCALES=self.AVAILABLE_LOCALES)
    @property
    def chat(self) -> ChatSettings:
        return ChatSettings(CHAT_ENCRYPTION_SALT=self.CHAT_ENCRYPTION_SALT, CHAT_MESSAGE_LIMIT=self.CHAT_MESSAGE_LIMIT, CHAT_RATE_LIMIT_PER_MINUTE=self.CHAT_RATE_LIMIT_PER_MINUTE, CHAT_WEBSOCKET_KEEPALIVE=self.CHAT_WEBSOCKET_KEEPALIVE, CHAT_MAX_MESSAGE_LENGTH=self.CHAT_MAX_MESSAGE_LENGTH)
    @property
    def fitment(self) -> FitmentSettings:
        return FitmentSettings(VCDB_PATH=self.VCDB_PATH, PCDB_PATH=self.PCDB_PATH, MODEL_MAPPINGS_PATH=self.MODEL_MAPPINGS_PATH, FITMENT_DB_URL=self.FITMENT_DB_URL, FITMENT_LOG_LEVEL=self.FITMENT_LOG_LEVEL, FITMENT_CACHE_SIZE=self.FITMENT_CACHE_SIZE)
    @property
    def currency(self) -> CurrencySettings:
        return CurrencySettings(EXCHANGE_RATE_API_KEY=self.EXCHANGE_RATE_API_KEY, EXCHANGE_RATE_UPDATE_FREQUENCY=self.EXCHANGE_RATE_UPDATE_FREQUENCY, STORE_INVERSE_RATES=self.STORE_INVERSE_RATES)
@lru_cache
def get_settings() -> Settings:
    return Settings()
settings = get_settings()