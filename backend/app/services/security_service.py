# backend/app/services/security_service.py
from __future__ import annotations

import hmac
import ipaddress
import json
import re
import secrets
import time
from enum import Enum
from typing import Any, Dict, List, Optional, Pattern, Set, Tuple, Union

from app.core.config import settings
from app.core.logging import get_logger
from app.services.interfaces import ServiceInterface

logger = get_logger("app.services.security_service")


class SecurityService:
    """
    Service for handling security-related functionality.

    This service handles:
    - Input validation and sanitization
    - CSRF token generation and validation
    - IP address validation
    - Content moderation
    - Token generation
    """

    def __init__(self, error_handling_service: Optional[ErrorHandlingService] = None) -> None:
        """
        Initialize the SecurityService.

        Args:
            error_handling_service: Optional error handling service for error reporting
        """
        self.secret_key: str = settings.security.SECRET_KEY
        self.allowed_hosts: Set[str] = set(settings.security.ALLOWED_HOSTS)
        self.trusted_ips: Set[str] = set(settings.security.TRUSTED_PROXIES)
        self.csrf_token_expiry: int = settings.security.CSRF_TOKEN_EXPIRY
        self.error_handling_service = error_handling_service

        # Regex patterns for validation
        self.email_pattern: Pattern[str] = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        self.username_pattern: Pattern[str] = re.compile(r"^[a-zA-Z0-9_-]{3,32}$")
        self.url_pattern: Pattern[str] = re.compile(r"^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$")

        # Define patterns for suspicious content
        self.suspicious_patterns: List[str] = [
            r"<script",
            r"javascript:",
            r"eval\(",
            r"document\.cookie",
            r"localStorage",
            r"sessionStorage",
            r"DROP TABLE",
            r"--",
            r"UNION SELECT",
            r"1=1",
            r"../../",
            r"data:text/html",
        ]
        self.suspicious_regex = re.compile("|".join(self.suspicious_patterns), re.IGNORECASE)

        # Prohibited words for content moderation
        self.prohibited_words: List[str] = []

        logger.info("SecurityService initialized")

    async def initialize(self) -> None:
        """Initialize the security service."""
        logger.debug("Initializing security service")

        # Load prohibited words from configuration
        await self._load_prohibited_words()

    async def shutdown(self) -> None:
        """Shut down the security service."""
        logger.debug("Shutting down security service")

    async def _load_prohibited_words(self) -> None:
        """Load prohibited words from configuration."""
        # This would typically load from a database or file
        # For now, we'll use a small hardcoded list
        self.prohibited_words = [
            "badword1",
            "badword2",
            "badword3",
        ]
        logger.debug(f"Loaded {len(self.prohibited_words)} prohibited words")

    def generate_csrf_token(self, session_id: str) -> str:
        """
        Generate a CSRF token for the given session.

        Args:
            session_id: The session ID to generate a token for

        Returns:
            CSRF token string
        """
        timestamp: int = int(time.time())
        random_part: str = secrets.token_hex(16)
        message: str = f"{session_id}:{timestamp}:{random_part}"
        signature: str = hmac.new(
            self.secret_key.encode(),
            message.encode(),
            digestmod="sha256"
        ).hexdigest()

        logger.debug("Generated CSRF token", session_id=session_id)
        return f"{message}:{signature}"

    def validate_csrf_token(self, token: str, session_id: str) -> bool:
        """
        Validate a CSRF token.

        Args:
            token: The token to validate
            session_id: The session ID the token was generated for

        Returns:
            True if valid, False otherwise
        """
        try:
            parts: List[str] = token.split(":")
            if len(parts) != 4:
                logger.warning("Invalid CSRF token format", token=token)
                return False

            message: str = ":".join(parts[:3])
            provided_signature: str = parts[3]
            received_session_id, timestamp_str, random_part = parts[:3]

            if received_session_id != session_id:
                logger.warning(
                    "CSRF token session mismatch",
                    expected=session_id,
                    received=received_session_id
                )
                return False

            expected_signature: str = hmac.new(
                self.secret_key.encode(),
                message.encode(),
                digestmod="sha256"
            ).hexdigest()

            if not hmac.compare_digest(provided_signature, expected_signature):
                logger.warning("CSRF token signature mismatch")
                return False

            timestamp: int = int(timestamp_str)
            if int(time.time()) - timestamp > self.csrf_token_expiry:
                logger.warning("CSRF token expired")
                return False

            return True

        except Exception as e:
            logger.warning(
                "CSRF token validation error",
                error=str(e),
                token=token
            )
            return False

    def is_valid_hostname(self, hostname: str) -> bool:
        """
        Check if a hostname is valid.

        Args:
            hostname: The hostname to validate

        Returns:
            True if valid, False otherwise
        """
        if not hostname or len(hostname) > 255:
            return False

        if self.allowed_hosts and hostname not in self.allowed_hosts:
            return False

        allowed_chars: Pattern[str] = re.compile(r"^[a-zA-Z0-9.-]+$")
        if not allowed_chars.match(hostname):
            return False

        return True

    def is_trusted_ip(self, ip_address: str) -> bool:
        """
        Check if an IP address is trusted.

        Args:
            ip_address: The IP address to check

        Returns:
            True if trusted, False otherwise
        """
        try:
            ip = ipaddress.ip_address(ip_address)

            for trusted_ip in self.trusted_ips:
                if "/" in trusted_ip:
                    if ip in ipaddress.ip_network(trusted_ip):
                        return True
                elif ip == ipaddress.ip_address(trusted_ip):
                    return True

            return False

        except ValueError:
            logger.warning("Invalid IP address format", ip_address=ip_address)
            return False

    def sanitize_input(self, input_str: str) -> str:
        """
        Sanitize user input by escaping HTML special characters.

        Args:
            input_str: The input string to sanitize

        Returns:
            Sanitized string
        """
        if not input_str:
            return ""

        sanitized: str = input_str
        sanitized = sanitized.replace("&", "&amp;")
        sanitized = sanitized.replace("<", "&lt;")
        sanitized = sanitized.replace(">", "&gt;")
        sanitized = sanitized.replace('"', "&quot;")
        sanitized = sanitized.replace("'", "&#x27;")
        sanitized = sanitized.replace("/", "&#x2F;")

        return sanitized

    def is_valid_email(self, email: str) -> bool:
        """
        Validate an email address.

        Args:
            email: The email to validate

        Returns:
            True if valid, False otherwise
        """
        if not email or len(email) > 255:
            return False

        return bool(self.email_pattern.match(email))

    def is_valid_username(self, username: str) -> bool:
        """
        Validate a username.

        Args:
            username: The username to validate

        Returns:
            True if valid, False otherwise
        """
        if not username:
            return False

        return bool(self.username_pattern.match(username))

    def generate_secure_token(self, length: int = 32) -> str:
        """
        Generate a cryptographically secure random token.

        Args:
            length: Length of the token in bytes

        Returns:
            Secure token string
        """
        return secrets.token_hex(length)

    def detect_suspicious_content(self, content: str) -> bool:
        """
        Detect potentially malicious content.

        Args:
            content: The content to check

        Returns:
            True if suspicious content is detected, False otherwise
        """
        if not content:
            return False

        return bool(self.suspicious_regex.search(content))

    def validate_json_input(self, json_data: Any) -> bool:
        """
        Validate JSON input for suspicious content.

        Args:
            json_data: The JSON data to validate

        Returns:
            True if the input is valid, False otherwise
        """
        try:
            # Check if it's a dictionary or list
            if not isinstance(json_data, (dict, list)):
                return False

            # Convert to string to check for suspicious patterns
            json_str = json.dumps(json_data)
            if self.detect_suspicious_content(json_str):
                logger.warning("Suspicious content detected in JSON input")
                return False

            return True

        except Exception as e:
            logger.error(
                "Error validating JSON input",
                error=str(e)
            )
            return False

    async def moderate_content(self, content: str) -> str:
        """
        Moderate user content to filter out prohibited words.

        Args:
            content: The content to moderate

        Returns:
            Moderated content
        """
        moderated = content

        # Replace prohibited words
        for word in self.prohibited_words:
            replacement = "*" * len(word)
            # Use word boundary to match whole words only
            moderated = re.sub(
                rf"\b{re.escape(word)}\b",
                replacement,
                moderated,
                flags=re.IGNORECASE
            )

        return moderated

    def is_valid_enum_value(self, value: str, enum_class: type) -> bool:
        """
        Validate if a string value is a valid enum value.

        Args:
            value: The value to validate
            enum_class: The Enum class to validate against

        Returns:
            True if the value is valid, False otherwise
        """
        try:
            enum_class(value)
            return True
        except ValueError:
            return False

    def detect_rate_limiting_attack(
        self, ip_address: str, requests_count: int, time_window: int
    ) -> bool:
        """
        Detect potential rate limiting attacks.

        Args:
            ip_address: The IP address to check
            requests_count: Number of requests made
            time_window: Time window in seconds

        Returns:
            True if attack is detected, False otherwise
        """
        # Implement a simple threshold-based detection
        threshold = settings.security.RATE_LIMIT_REQUESTS_PER_MINUTE * 2

        if requests_count > threshold:
            logger.warning(
                "Rate limiting attack detected",
                ip_address=ip_address,
                requests_count=requests_count,
                time_window=time_window,
            )
            return True

        return False

    def validate_url(self, url: str) -> bool:
        """
        Validate a URL.

        Args:
            url: The URL to validate

        Returns:
            True if valid, False otherwise
        """
        if not url:
            return False

        return bool(self.url_pattern.match(url))

    def hash_password(self, password: str) -> str:
        """
        Hash a password securely.

        Args:
            password: The password to hash

        Returns:
            Hashed password
        """
        # Use passlib or bcrypt in actual implementation
        # This is a placeholder
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.

        Args:
            plain_password: The plain text password
            hashed_password: The hashed password to compare against

        Returns:
            True if the password matches, False otherwise
        """
        # Use passlib or bcrypt in actual implementation
        # This is a placeholder
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, hashed_password)
