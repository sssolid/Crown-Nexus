# app/core/config/security.py

from __future__ import annotations

"""
Security configuration settings.

This module defines security-related settings for the application including
authentication, CORS, rate limiting, and content security policies.
"""

import secrets
from typing import Any, List, Union

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class SecuritySettings(BaseSettings):
    """Security-related application settings."""

    # Auth settings
    SECRET_KEY: str = Field("your-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60 * 24 * 8)  # 8 days
    ALGORITHM: str = Field("HS256")

    # Host and proxy settings
    ALLOWED_HOSTS: List[str] = Field(
        default=["localhost", "127.0.0.1"], description="List of allowed hostnames"
    )
    TRUSTED_PROXIES: List[str] = Field(
        default=["127.0.0.1", "::1"], description="List of trusted proxy IP addresses"
    )

    # CORS settings
    CORS_ALWAYS_ALLOW: bool = Field(
        default=False, description="Whether to always allow CORS requests"
    )
    BACKEND_CORS_ORIGINS: List[str] = Field(default_factory=list)

    # CSRF protection
    CSRF_COOKIE_SECURE: bool = Field(
        default=True, description="Whether to only send CSRF cookie over HTTPS"
    )
    CSRF_TOKEN_EXPIRY: int = Field(
        default=86400,
        description="Expiration time for CSRF tokens in seconds (24 hours)",
    )

    # Rate limiting
    RATE_LIMIT_ENABLED: bool = Field(
        default=True, description="Whether rate limiting is enabled"
    )
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = Field(
        default=600, description="Default requests allowed per minute"
    )
    RATE_LIMIT_BURST_MULTIPLIER: float = Field(
        default=1.5, description="Multiplier for burst capacity"
    )
    RATE_LIMIT_STORAGE: str = Field(
        default="redis",
        description="Storage backend for rate limiting ('redis' or 'memory')",
    )

    # Content security policies
    CONTENT_SECURITY_POLICY: str = Field(
        default=(
            "default-src 'self'; "
            "img-src 'self' data: https://fastapi.tiangolo.com; "
            "script-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
            "style-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
            "connect-src 'self';"
        ),
        description="Content Security Policy header value",
    )
    PERMISSIONS_POLICY: str = Field(
        default="camera=(), microphone=(), geolocation=(), payment=()",
        description="Permissions Policy header value",
    )

    # Audit logging
    AUDIT_LOGGING_ENABLED: bool = Field(
        default=True, description="Whether audit logging is enabled"
    )
    AUDIT_LOG_TO_DB: bool = Field(
        default=True, description="Whether to log audit events to database"
    )
    AUDIT_LOG_TO_FILE: bool = Field(
        default=False, description="Whether to log audit events to file"
    )
    AUDIT_LOG_FILE: str = Field(
        default="logs/audit.log", description="File path for audit log"
    )

    # Chat security settings
    CHAT_ENCRYPTION_SALT: str = Field(default_factory=lambda: secrets.token_hex(16))
    CHAT_MESSAGE_LIMIT: int = Field(50)
    CHAT_RATE_LIMIT_PER_MINUTE: int = Field(60)
    CHAT_WEBSOCKET_KEEPALIVE: int = Field(30)
    CHAT_MAX_MESSAGE_LENGTH: int = Field(5000)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Allow extra fields in env file
        json_schema_extra={
            # Disable JSON parsing for these fields that use string-based parsing
            "ALLOWED_HOSTS": {"env_mode": "str"},
            "TRUSTED_PROXIES": {"env_mode": "str"},
            "BACKEND_CORS_ORIGINS": {"env_mode": "str"},
        },
    )

    @field_validator("ALLOWED_HOSTS", "TRUSTED_PROXIES", mode="before")
    @classmethod
    def parse_str_to_list(cls, v: Any) -> List[str]:
        """Parse string to list of strings if needed."""
        if isinstance(v, str):
            if not v:
                return []
            if "," in v:
                return [item.strip() for item in v.split(",")]
            return [v.strip()]
        return v

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            if not v:
                return []
            if "," in v:
                return [i.strip() for i in v.split(",")]
            return [v.strip()]
        return v

    @field_validator("RATE_LIMIT_STORAGE")
    @classmethod
    def validate_rate_limit_storage(cls, v: str) -> str:
        """Validate rate limit storage backend."""
        valid_storage = {"redis", "memory"}
        if v not in valid_storage:
            raise ValueError(
                f"Invalid rate limit storage: {v}. Must be one of {valid_storage}"
            )
        return v
