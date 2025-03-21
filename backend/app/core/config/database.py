# app/core/config/database.py

from __future__ import annotations

"""
Database configuration settings.

This module handles all database-related settings including connection
parameters for PostgreSQL and Redis.
"""

from typing import Optional

from pydantic import Field, PostgresDsn, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Database connection settings."""

    # PostgreSQL settings
    POSTGRES_SERVER: str = Field("localhost")
    POSTGRES_USER: str = Field("postgres")
    POSTGRES_PASSWORD: str = Field("postgres")
    POSTGRES_DB: str = Field("crown_nexus")
    POSTGRES_PORT: str = Field("5432")
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    # Redis settings
    REDIS_HOST: str = Field("localhost")
    REDIS_PORT: int = Field(6379)
    REDIS_PASSWORD: Optional[SecretStr] = None
    REDIS_DB: int = Field(0)
    REDIS_MAX_CONNECTIONS: int = Field(5000)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @model_validator(mode="after")
    def assemble_db_connection(self) -> DatabaseSettings:
        """Build the database URI if not provided directly."""
        if not self.SQLALCHEMY_DATABASE_URI:
            self.SQLALCHEMY_DATABASE_URI = PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_SERVER,
                port=int(self.POSTGRES_PORT),
                path=f"{self.POSTGRES_DB}",
            )
        return self

    @property
    def redis_uri(self) -> str:
        """Get Redis connection URI."""
        password_part = ""
        if self.REDIS_PASSWORD:
            password_part = f":{self.REDIS_PASSWORD.get_secret_value()}@"

        return f"redis://{password_part}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
