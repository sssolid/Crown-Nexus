from __future__ import annotations
'\nDatabase configuration settings.\n\nThis module handles all database-related settings including connection\nparameters for PostgreSQL and Redis.\n'
from typing import Optional
from pydantic import PostgresDsn, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
class DatabaseSettings(BaseSettings):
    POSTGRES_SERVER: str = 'localhost'
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'postgres'
    POSTGRES_DB: str = 'crown_nexus'
    POSTGRES_PORT: str = '5432'
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[SecretStr] = None
    REDIS_DB: int = 0
    REDIS_MAX_CONNECTIONS: int = 5000
    REDIS_URI: str = 'redis://localhost:6379/0'
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True, extra='ignore')
    @model_validator(mode='after')
    def assemble_db_connection(self) -> 'DatabaseSettings':
        if not self.SQLALCHEMY_DATABASE_URI:
            self.SQLALCHEMY_DATABASE_URI = PostgresDsn.build(scheme='postgresql+asyncpg', username=self.POSTGRES_USER, password=self.POSTGRES_PASSWORD, host=self.POSTGRES_SERVER, port=int(self.POSTGRES_PORT), path=f'{self.POSTGRES_DB}')
        return self
    @property
    def redis_uri(self) -> str:
        password_part = ''
        if self.REDIS_PASSWORD:
            password_part = f':{self.REDIS_PASSWORD.get_secret_value()}@'
        return f'redis://{password_part}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}'