# backend/app/services/security/service.py
"""Main security service implementation.

This module provides the primary SecurityService that coordinates and implements
high-level security features by composing the various security components.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from app.core.config import settings
from app.core.logging import get_logger
from app.services.interfaces import ServiceInterface
from app.services.security.api_keys import ApiKeyService
from app.services.security.base import SecurityViolation
from app.services.security.csrf import CsrfService
from app.services.security.encryption import EncryptionService
from app.services.security.passwords import PasswordService
from app.services.security.rate_limiting import RateLimitService
from app.services.security.tokens import TokenService
from app.services.security.validation import ValidationService

logger = get_logger(__name__)


class SecurityService(ServiceInterface):
    """Coordinating service for security features.

    This service provides a unified interface to the various security components,
    coordinating their functionality and providing high-level security operations.
    """

    def __init__(self) -> None:
        """Initialize the security service."""
        # Initialize component services
        self.password_service = PasswordService()
        self.token_service = TokenService()
        self.api_key_service = ApiKeyService()
        self.csrf_service = CsrfService()
        self.validation_service = ValidationService()
        self.rate_limit_service = RateLimitService()
        self.encryption_service = EncryptionService()

        # Initialize security logging
        self.security_log_prefix = "security_event:"

        logger.info("SecurityService initialized")

    async def initialize(self) -> None:
        """Initialize the security service."""
        logger.debug("Initializing security service")
        # No specific initialization needed yet

    async def shutdown(self) -> None:
        """Shut down the security service."""
        logger.debug("Shutting down security service")
        # No specific shutdown process needed yet

    # Convenience methods that delegate to component services

    # Password methods
    async def validate_password_policy(self, password: str, user_id: Optional[str] = None):
        """Validate a password against the password policy."""
        return await self.password_service.validate_password_policy(password, user_id)

    def hash_password(self, password: str) -> str:
        """Hash a password using a secure algorithm."""
        return self.password_service.hash_password(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash."""
        return self.password_service.verify_password(plain_password, hashed_password)

    # Token methods
    async def create_access_token(self, subject: Union[str, int], **kwargs):
        """Create an access token."""
        return await self.token_service.create_access_token(subject, **kwargs)

    async def create_token_pair(self, subject: Union[str, int], **kwargs):
        """Create an access and refresh token pair."""
        return await self.token_service.create_token_pair(subject, **kwargs)

    async def validate_token(self, token: str, **kwargs):
        """Validate a token."""
        return await self.token_service.validate_token(token, **kwargs)

    async def refresh_access_token(self, refresh_token: str):
        """Generate a new access token from a refresh token."""
        return await self.token_service.refresh_access_token(refresh_token)

    async def blacklist_token(self, token: str, reason: str = "revoked"):
        """Add a token to the blacklist."""
        return await self.token_service.blacklist_token(token, reason)

    # API key methods
    def generate_api_key(self, user_id: str, name: str, permissions: Optional[List[str]] = None):
        """Generate a new API key."""
        return self.api_key_service.generate_api_key(user_id, name, permissions)

    def verify_api_key(self, api_key: str, stored_hash: str) -> bool:
        """Verify an API key against a stored hash."""
        return self.api_key_service.verify_api_key(api_key, stored_hash)

    # CSRF methods
    def generate_csrf_token(self, session_id: str) -> str:
        """Generate a CSRF token."""
        return self.csrf_service.generate_token(session_id)

    def validate_csrf_token(self, token: str, session_id: str) -> bool:
        """Validate a CSRF token."""
        return self.csrf_service.validate_token(token, session_id)

    # Validation methods
    def is_valid_hostname(self, hostname: str) -> bool:
        """Check if a hostname is valid and allowed."""
        return self.validation_service.is_valid_hostname(hostname)

    def is_trusted_ip(self, ip_address: str) -> bool:
        """Check if an IP address is trusted."""
        return self.validation_service.is_trusted_ip(ip_address)

    def sanitize_input(self, input_str: str) -> str:
        """Sanitize user input to prevent XSS."""
        return self.validation_service.sanitize_input(input_str)

    def detect_suspicious_content(self, content: str) -> bool:
        """Detect potentially malicious content."""
        return self.validation_service.detect_suspicious_content(content)

    def get_security_headers(self) -> Dict[str, str]:
        """Get security headers for HTTP responses."""
        return self.validation_service.get_security_headers()

    # Rate limiting methods
    async def check_rate_limit(self, key: str, max_requests: int, window_seconds: int):
        """Check if a request should be rate limited."""
        return await self.rate_limit_service.check_rate_limit(key, max_requests, window_seconds)

    # Encryption methods
    def encrypt_data(self, data: Union[str, bytes, dict]) -> str:
        """Encrypt sensitive data."""
        return self.encryption_service.encrypt_data(data)

    def decrypt_data(self, encrypted_data: str) -> Union[str, dict]:
        """Decrypt encrypted data."""
        return self.encryption_service.decrypt_data(encrypted_data)

    def generate_secure_token(self, length: int = 32) -> str:
        """Generate a cryptographically secure random token."""
        return self.encryption_service.generate_secure_token(length)

    # Security event logging
    async def log_security_event(
        self,
        violation_type: SecurityViolation,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log a security event.

        Args:
            violation_type: The type of violation
            user_id: The user ID involved
            ip_address: The IP address involved
            details: Additional details about the event
        """
        log_data = {
            "violation_type": violation_type,
            "user_id": user_id,
            "ip_address": ip_address,
            "details": details or {},
        }

        logger.warning(f"Security violation: {violation_type.value}", **log_data)
