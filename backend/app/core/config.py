from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, PostgresDsn, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings.
    
    Attributes:
        PROJECT_NAME: Name of the project
        DESCRIPTION: Project description
        VERSION: API version
        API_V1_STR: API v1 prefix
        SECRET_KEY: Secret key for JWT tokens
        ACCESS_TOKEN_EXPIRE_MINUTES: Expiration time for access tokens in minutes
        BACKEND_CORS_ORIGINS: List of origins that should be allowed by CORS
        POSTGRES_SERVER: PostgreSQL server hostname
        POSTGRES_USER: PostgreSQL username
        POSTGRES_PASSWORD: PostgreSQL password
        POSTGRES_DB: PostgreSQL database name
        SQLALCHEMY_DATABASE_URI: SQLAlchemy database URI
        ELASTICSEARCH_HOST: Elasticsearch host
        ELASTICSEARCH_PORT: Elasticsearch port
        REDIS_HOST: Redis host
        REDIS_PORT: Redis port
    """
    PROJECT_NAME: str = "Crown Nexus"
    DESCRIPTION: str = "B2B platform for automotive aftermarket industry"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """
        Parse CORS origins from string or list.
        
        Args:
            v: CORS origins as string or list
            
        Returns:
            Parsed CORS origins
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "crown_nexus"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        """
        Assemble database URI from components.
        
        Args:
            v: Database URI if already provided
            values: Settings values
            
        Returns:
            Assembled database URI
        """
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )
    
    # Elasticsearch
    ELASTICSEARCH_HOST: str = "localhost"
    ELASTICSEARCH_PORT: int = 9200
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
