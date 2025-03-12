from __future__ import annotations
import os
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, DirectoryPath, PostgresDsn, validator
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    PROJECT_NAME: str = 'Crown Nexus'
    DESCRIPTION: str = 'B2B platform for automotive aftermarket industry'
    VERSION: str = '0.1.0'
    API_V1_STR: str = '/api/v1'
    SECRET_KEY: str = 'your-secret-key-change-in-production'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
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
    MEDIA_ROOT: DirectoryPath = 'media'
    MEDIA_URL: str = '/media/'
    @validator('MEDIA_ROOT', pre=True)
    def create_media_directories(cls, v: str) -> str:
        os.makedirs(v, exist_ok=True)
        for media_type in ['image', 'document', 'video', 'other', 'thumbnails']:
            os.makedirs(os.path.join(v, media_type), exist_ok=True)
        return v
    class Config:
        case_sensitive = True
        env_file = '.env'
settings = Settings()