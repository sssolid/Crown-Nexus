# backend/app/services/security_service.py
"""Security service implementation for Crown Nexus application.

This module provides a service for handling security-related operations
such as CSRF protection, input validation, and IP/hostname verification.
"""

from __future__ import annotations

import hmac
import ipaddress
import re
from typing import Any, Dict, List, Optional, Pattern, Set, Tuple, Union
import secrets
import time

from app.core.config import settings
from app.core.logging import get_logger
from app.services.interfaces import ServiceInterface

logger = get_logger("app.services.security")


class SecurityService:
    """Service for security-related operations.

    This service provides methods for token validation, CSRF protection,
    IP validation, and other security operations.

    Attributes:
        secret_key: Application secret key for signing tokens
        allowed_hosts: Set of allowed hostnames
        trusted_ips: Set of trusted proxy IP addresses
        email_pattern: Compiled regex for validating email addresses
        username_pattern: Compiled regex for validating usernames
    """

    def __init__(self, error_handling_service: Optional[ErrorHandlingService] = None) -> None:
        """Initialize the security service.

        Args:
            error_handling_service: Service for handling security errors
        """
        self.secret_key: str = settings.security.SECRET_KEY
        self.allowed_hosts: Set[str] = set(settings.security.ALLOWED_HOSTS)
        self.trusted_ips: Set[str] = set(settings.security.TRUSTED_PROXIES)
        self.csrf_token_expiry: int = settings.security.CSRF_TOKEN_EXPIRY
        self.error_handling_service = error_handling_service

        # Precompile regex patterns
        self.email_pattern: Pattern[str] = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        self.username_pattern: Pattern[str] = re.compile(r'^[a-zA-Z0-9_-]{3,32}$')

        logger.info("SecurityService initialized")

    async def initialize(self) -> None:
        """Initialize service resources."""
        pass

    async def shutdown(self) -> None:
        """Release service resources."""
        pass

    def generate_csrf_token(self, session_id: str) -> str:
        """Generate a CSRF token for a session.

        Args:
            session_id: The session ID to generate a token for

        Returns:
            str: A secure CSRF token
        """
        timestamp: int = int(time.time())
        random_part: str = secrets.token_hex(16)
        message: str = f"{session_id}:{timestamp}:{random_part}"

        signature: str = hmac.new(
            self.secret_key.encode(),
            message.encode(),
            digestmod="sha256"
        ).hexdigest()

        return f"{message}:{signature}"

    def validate_csrf_token(self, token: str, session_id: str) -> bool:
        """Validate a CSRF token.

        Args:
            token: The CSRF token to validate
            session_id: The session ID the token was generated for

        Returns:
            bool: True if the token is valid
        """
        try:
            parts: List[str] = token.split(":")
            if len(parts) != 4:
                return False

            message: str = ":".join(parts[:3])
            provided_signature: str = parts[3]

            # Check token structure
            received_session_id, timestamp_str, random_part = parts[:3]

            # Verify the session ID
            if received_session_id != session_id:
                return False

            # Verify the signature
            expected_signature: str = hmac.new(
                self.secret_key.encode(),
                message.encode(),
                digestmod="sha256"
            ).hexdigest()

            if not hmac.compare_digest(provided_signature, expected_signature):
                return False

            # Check token expiration (default: 24 hours)
            timestamp: int = int(timestamp_str)
            if int(time.time()) - timestamp > self.csrf_token_expiry:
                return False

            return True
        except Exception as e:
            logger.warning(f"CSRF token validation failed: {str(e)}")
            return False

    def is_valid_hostname(self, hostname: str) -> bool:
        """Check if a hostname is valid and allowed.

        Args:
            hostname: The hostname to check

        Returns:
            bool: True if the hostname is valid and allowed
        """
        if not hostname or len(hostname) > 255:
            return False

        # Check if hostname is in allowed hosts
        if self.allowed_hosts and hostname not in self.allowed_hosts:
            return False

        # Basic hostname validation
        allowed_chars: Pattern[str] = re.compile(r'^[a-zA-Z0-9.-]+$')
        if not allowed_chars.match(hostname):
            return False

        return True

    def is_trusted_ip(self, ip_address: str) -> bool:
        """Check if an IP address is in the trusted IP range.

        Args:
            ip_address: The IP address to check

        Returns:
            bool: True if the IP address is trusted
        """
        try:
            ip = ipaddress.ip_address(ip_address)

            # Check if IP is in trusted ranges
            for trusted_ip in self.trusted_ips:
                if '/' in trusted_ip:  # CIDR notation
                    if ip in ipaddress.ip_network(trusted_ip):
                        return True
                else:  # Single IP
                    if ip == ipaddress.ip_address(trusted_ip):
                        return True

            return False
        except ValueError:
            return False

    def sanitize_input(self, input_str: str) -> str:
        """Sanitize user input to prevent XSS attacks.

        Args:
            input_str: The string to sanitize

        Returns:
            str: Sanitized string
        """
        if not input_str:
            return ""

        # Replace potentially dangerous characters
        sanitized: str = input_str
        sanitized = sanitized.replace('&', '&amp;')
        sanitized = sanitized.replace('<', '&lt;')
        sanitized = sanitized.replace('>', '&gt;')
        sanitized = sanitized.replace('"', '&quot;')
        sanitized = sanitized.replace("'", '&#x27;')
        sanitized = sanitized.replace('/', '&#x2F;')

        return sanitized

    def is_valid_email(self, email: str) -> bool:
        """Check if an email address is valid.

        Args:
            email: The email address to check

        Returns:
            bool: True if the email address is valid
        """
        if not email or len(email) > 255:
            return False

        return bool(self.email_pattern.match(email))

    def is_valid_username(self, username: str) -> bool:
        """Check if a username is valid.

        Args:
            username: The username to check

        Returns:
            bool: True if the username is valid
        """
        if not username:
            return False

        return bool(self.username_pattern.match(username))

    def generate_secure_token(self, length: int = 32) -> str:
        """Generate a cryptographically secure random token.

        Args:
            length: Length of the token in bytes

        Returns:
            str: A secure random token
        """
        return secrets.token_hex(length)
