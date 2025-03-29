from __future__ import annotations
'Security models and type definitions.\n\nThis module defines the data models, enums, and type definitions used throughout\nthe security system, providing a consistent type framework.\n'
import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
class TokenType(str, Enum):
    ACCESS = 'access'
    REFRESH = 'refresh'
    RESET_PASSWORD = 'reset_password'
    EMAIL_VERIFICATION = 'email_verification'
    INVITATION = 'invitation'
    API_KEY = 'api_key'
    CSRF = 'csrf'
    SESSION = 'session'
class SecurityViolation(str, Enum):
    INVALID_TOKEN = 'invalid_token'
    EXPIRED_TOKEN = 'expired_token'
    CSRF_VIOLATION = 'csrf_violation'
    RATE_LIMIT_EXCEEDED = 'rate_limit_exceeded'
    BRUTE_FORCE_ATTEMPT = 'brute_force_attempt'
    SUSPICIOUS_ACTIVITY = 'suspicious_activity'
    UNAUTHORIZED_ACCESS = 'unauthorized_access'
    INVALID_IP = 'invalid_ip'
    PERMISSION_VIOLATION = 'permission_violation'
    INJECTION_ATTEMPT = 'injection_attempt'
    XSS_ATTEMPT = 'xss_attempt'
class TokenClaimsModel(BaseModel):
    sub: str = Field(..., description='Subject (user ID)')
    exp: datetime.datetime = Field(..., description='Expiration time')
    iat: datetime.datetime = Field(..., description='Issued at time')
    jti: str = Field(..., description='JWT ID (unique identifier)')
    type: str = Field(..., description='Token type')
    role: Optional[str] = Field(None, description='User role')
    permissions: Optional[List[str]] = Field(None, description='User permissions')
    user_data: Optional[Dict[str, Any]] = Field(None, description='Additional user data')
class TokenPair(BaseModel):
    access_token: str = Field(..., description='JWT access token')
    refresh_token: str = Field(..., description='JWT refresh token')
    token_type: str = Field('bearer', description='Token type')
    expires_in: int = Field(..., description='Access token lifetime in seconds')
class ApiKeyData(BaseModel):
    api_key: str
    key_id: str
    hashed_secret: str
    token: str
    name: str
    created_at: str
    permissions: List[str] = []
class PasswordPolicy(BaseModel):
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