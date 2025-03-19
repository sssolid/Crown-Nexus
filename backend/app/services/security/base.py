# backend/app/services/security/base.py
"""Base interfaces and types for the security system.

This module defines common security-related types, enums, and models
that are used across the security service components.
"""
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Set, Union

from pydantic import BaseModel, EmailStr, Field, SecretStr


class SecurityViolation(str, Enum):
    """Types of security violations that can be detected."""

    INVALID_TOKEN = "invalid_token"
    EXPIRED_TOKEN = "expired_token"
    CSRF_VIOLATION = "csrf_violation"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    BRUTE_FORCE_ATTEMPT = "brute_force_attempt"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    INVALID_IP = "invalid_ip"
    PERMISSION_VIOLATION = "permission_violation"
    INJECTION_ATTEMPT = "injection_attempt"
    XSS_ATTEMPT = "xss_attempt"


class PasswordPolicy(BaseModel):
    """Policy for password requirements and restrictions."""

    min_length: int = 8
    require_uppercase: bool = True
    require_lowercase: bool = True
    require_digit: bool = True
    require_special_char: bool = True
    max_length: int = 128
    prevent_common_passwords: bool = True
    password_history_count: int = 5
    max_failed_attempts: int = 5
    lockout_duration_minutes: int = 30
    password_expiry_days: Optional[int] = 90


class TokenConfig(BaseModel):
    """Configuration for token generation and validation."""

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    reset_token_expire_minutes: int = 60
    verification_token_expire_days: int = 7
    invitation_token_expire_days: int = 14


class ApiKeyData(BaseModel):
    """Data structure for API key information."""

    api_key: str
    key_id: str
    hashed_secret: str
    token: str
    name: str
    created_at: str
    permissions: List[str] = []


class SecurityConfig(BaseModel):
    """Configuration for security services."""

    allowed_hosts: Set[str] = Field(default_factory=set)
    trusted_proxies: Set[str] = Field(default_factory=set)
    cors_origins: List[str] = Field(default_factory=list)
    csrf_token_expiry: int = 3600  # 1 hour
    session_expiry: int = 86400  # 24 hours
    secure_cookies: bool = True
    same_site_policy: str = "lax"
    content_security_policy: str = "default-src 'self'"
    permissions_policy: str = ""
    rate_limit_enabled: bool = True
