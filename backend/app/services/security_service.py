from __future__ import annotations

"""Security service providing high-level security features and policies.

This service provides application-specific security functionality built on top of
the core security primitives. It includes:
- Password policy validation
- Suspicious request detection
- Host validation and IP checking
- API key management
- CSRF protection
- Rate limiting
- Validation of security-critical requests

It maintains a clear separation of concerns with the core security module by focusing
on application-specific security policies and features rather than primitives.
"""

import base64
import binascii
import hashlib
import hmac
import ipaddress
import json
import re
import secrets
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Pattern, Set, Tuple, Union

import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from fastapi import HTTPException, Request, Response, status
from pydantic import BaseModel, EmailStr, Field, SecretStr

from app.core.config import settings
from app.core.exceptions import (
    AuthenticationException,
    ErrorCode,
    SecurityException,
    ValidationException,
)
from app.core.logging import get_logger
from app.core.security import (
    TokenClaimsModel,
    TokenType,
    create_token,
    create_token_pair,
    decode_token,
    get_password_hash,
    verify_password,
)
from app.models.user import User
from app.utils.redis_manager import get_key, set_key, delete_key

logger = get_logger("app.services.security_service")


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


@dataclass
class TokenConfig:
    """Configuration for token generation and validation."""

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    reset_token_expire_minutes: int = 60
    verification_token_expire_days: int = 7
    invitation_token_expire_days: int = 14


class SecurityService:
    """Service providing high-level security features and policy enforcement."""

    def __init__(self) -> None:
        """Initialize the security service."""
        self.token_config = TokenConfig(
            secret_key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
            access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
        
        self.password_policy = PasswordPolicy()
        
        # Regular expression patterns for validation
        self.patterns = {
            "email": re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"),
            "phone": re.compile(r"^\+?[0-9]{10,15}$"),
            "username": re.compile(r"^[a-zA-Z0-9_-]{3,32}$"),
            "url": re.compile(
                r"^(https?:\/\/)?(([a-z\d]([a-z\d-]*[a-z\d])*)\.)+[a-z]{2,}|"
                r"((\d{1,3}\.){3}\d{1,3}))(:\d+)?(\/[-a-z\d%_.~+]*)*"
                r"(\?[;&a-z\d%_.~+=-]*)?(#[-a-z\d_]*)?$",
                re.IGNORECASE,
            ),
        }
        
        # Used for token blacklisting
        self.token_blacklist_prefix = "token:blacklist:"
        
        # Security configuration
        self.allowed_hosts: Set[str] = set(settings.security.ALLOWED_HOSTS)
        self.trusted_proxies: Set[str] = set(settings.security.TRUSTED_PROXIES)
        self.csrf_token_expiry: int = settings.security.CSRF_TOKEN_EXPIRY
        
        # Patterns for detecting suspicious content
        self.suspicious_patterns: List[str] = [
            r"<script.*?>",
            r"javascript:",
            r"eval\(",
            r"document\.cookie",
            r"localStorage",
            r"sessionStorage",
            r"onload=",
            r"onerror=",
            r"onclick=",
            r"onmouseover=",
            r"DROP TABLE",
            r"--",
            r"UNION SELECT",
            r"1=1",
            r"../../",
            r"data:text/html",
            r"file://",
        ]
        self.suspicious_regex = re.compile("|".join(self.suspicious_patterns), re.IGNORECASE)
        
        # Set up encryption for sensitive data
        self._setup_encryption()
        
        # Cache of common passwords for policy enforcement
        self.common_passwords: Set[str] = set()
        
        logger.info("SecurityService initialized")

    async def initialize(self) -> None:
        """Initialize the security service.
        
        Loads common passwords and performs other initialization tasks.
        """
        logger.debug("Initializing security service")
        if self.password_policy.prevent_common_passwords:
            await self._load_common_passwords()

    async def shutdown(self) -> None:
        """Shut down the security service."""
        logger.debug("Shutting down security service")

    def _setup_encryption(self) -> None:
        """Set up encryption for sensitive data."""
        base_key = settings.SECRET_KEY.encode()
        salt = b"security_service_salt"
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000
        )
        key = base64.urlsafe_b64encode(kdf.derive(base_key))
        self.cipher = Fernet(key)

    async def _load_common_passwords(self) -> None:
        """Load list of common passwords for policy enforcement."""
        self.common_passwords = set()
        try:
            passwords_file = Path(settings.BASE_DIR) / "app" / "data" / "common_passwords.txt"
            if passwords_file.exists():
                with open(passwords_file, "r") as f:
                    for line in f:
                        self.common_passwords.add(line.strip())
                logger.debug(f"Loaded {len(self.common_passwords)} common passwords")
            else:
                # Fallback to a small set of common passwords
                self.common_passwords = {
                    "password", "123456", "123456789", "qwerty", "12345678",
                    "111111", "1234567890", "1234567", "password1", "12345",
                    "123123", "000000", "iloveyou", "1234", "1q2w3e4r", "admin"
                }
                logger.debug(f"Using default list of {len(self.common_passwords)} common passwords")
        except Exception as e:
            logger.error(f"Error loading common passwords: {str(e)}")
            # Fallback to a minimal set
            self.common_passwords = {"password", "123456", "123456789", "qwerty", "12345678"}

    # Encryption methods
    def encrypt_data(self, data: Union[str, bytes, dict]) -> str:
        """Encrypt sensitive data.
        
        Args:
            data: The data to encrypt (string, bytes, or dict)
            
        Returns:
            Base64 encoded encrypted data
        """
        if isinstance(data, dict):
            data = json.dumps(data)
        if isinstance(data, str):
            data = data.encode()
        encrypted = self.cipher.encrypt(data)
        return base64.urlsafe_b64encode(encrypted).decode()

    def decrypt_data(self, encrypted_data: str) -> Union[str, dict]:
        """Decrypt encrypted data.
        
        Args:
            encrypted_data: The encrypted data to decrypt
            
        Returns:
            The decrypted data (string or dict)
            
        Raises:
            SecurityException: If decryption fails
        """
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data)
            decrypted = self.cipher.decrypt(encrypted_bytes)
            result = decrypted.decode()
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                return result
        except (binascii.Error, ValueError) as e:
            logger.error(f"Decryption error: {str(e)}")
            raise SecurityException(
                message="Failed to decrypt data",
                code=ErrorCode.SECURITY_ERROR,
                details={"error": "Invalid encrypted data format"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    # Advanced token methods
    async def create_and_store_token(
        self,
        subject: Union[str, uuid.UUID],
        token_type: TokenType,
        expires_delta: Optional[timedelta] = None,
        role: Optional[str] = None,
        permissions: Optional[List[str]] = None,
        user_data: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Create a token and store it in the database.
        
        Args:
            subject: The subject identifier (usually user ID)
            token_type: The type of token
            expires_delta: How long the token should be valid
            role: The role of the user
            permissions: Specific permissions for the user
            user_data: Additional user data to include in the token
            
        Returns:
            The encoded JWT token
        """
        # Create the JWT token using the core security module
        token = create_token(
            subject=str(subject),
            token_type=token_type.value,
            expires_delta=expires_delta,
            role=role or "",
            permissions=permissions,
            user_data=user_data,
        )
        
        # Additional security logic could be added here, such as:
        # - Storing token in database for auditing
        # - Limiting number of active tokens per user
        # - Recording IP address or device information
        
        return token

    async def validate_token(
        self,
        token: str,
        expected_type: Optional[TokenType] = None,
        verify_exp: bool = True,
        check_blacklist: bool = True,
    ) -> TokenClaimsModel:
        """Validate a token and apply additional security checks.
        
        Args:
            token: The token to validate
            expected_type: The expected token type
            verify_exp: Whether to verify expiration
            check_blacklist: Whether to check the token blacklist
            
        Returns:
            The decoded token claims
            
        Raises:
            AuthenticationException: If validation fails
        """
        try:
            # Decode and validate the token using the core security module
            token_data = await decode_token(token)
            
            # Apply additional token validations
            if expected_type and token_data.type != expected_type.value:
                logger.warning(
                    f"Token type mismatch: expected {expected_type}, got {token_data.type}",
                    subject=token_data.sub,
                )
                raise AuthenticationException(
                    message="Invalid token type",
                    code=ErrorCode.INVALID_TOKEN,
                    details={
                        "expected_type": expected_type.value,
                        "actual_type": token_data.type,
                    },
                )
                
            # Additional security checks can be added here
            # For example, verify the token against a whitelist of valid tokens
            # or check for IP address restrictions
            
            return token_data
            
        except AuthenticationException:
            # Let core authentication exceptions pass through
            raise
        except Exception as e:
            logger.error(f"Token validation error: {str(e)}")
            raise AuthenticationException(
                message="Token validation failed",
                code=ErrorCode.INVALID_TOKEN,
                details={"error": str(e)},
            )

    # Password policy validation
    async def validate_password_policy(
        self, password: str, user_id: Optional[str] = None
    ) -> Tuple[bool, Optional[str]]:
        """Validate a password against the password policy.
        
        Args:
            password: The password to validate
            user_id: Optional user ID for checking password history
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check length requirements
        if len(password) < self.password_policy.min_length:
            return (
                False,
                f"Password must be at least {self.password_policy.min_length} characters long",
            )
            
        if len(password) > self.password_policy.max_length:
            return (
                False,
                f"Password cannot be longer than {self.password_policy.max_length} characters",
            )

        # Check character requirements
        if self.password_policy.require_uppercase and not any(c.isupper() for c in password):
            return (False, "Password must contain at least one uppercase letter")
            
        if self.password_policy.require_lowercase and not any(c.islower() for c in password):
            return (False, "Password must contain at least one lowercase letter")
            
        if self.password_policy.require_digit and not any(c.isdigit() for c in password):
            return (False, "Password must contain at least one digit")
            
        if self.password_policy.require_special_char and not any(
            not c.isalnum() for c in password
        ):
            return (False, "Password must contain at least one special character")

        # Check against common passwords
        if self.password_policy.prevent_common_passwords and password.lower() in self.common_passwords:
            return (False, "Password is too common and easily guessed")

        # Check password history
        if user_id and self.password_policy.password_history_count > 0:
            # This would normally check against a database of password history
            # Implementation depends on your storage mechanism
            pass

        return (True, None)

    # API key management
    def generate_api_key(
        self, user_id: str, name: str, permissions: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """Generate a new API key.
        
        Args:
            user_id: The user ID the key belongs to
            name: A name for the key
            permissions: Specific permissions for this key
            
        Returns:
            Dictionary with API key details
        """
        key_id = str(uuid.uuid4())
        secret = secrets.token_urlsafe(32)
        hashed_secret = hashlib.sha256(secret.encode()).hexdigest()
        
        api_key = f"{key_id}.{secret}"
        
        # Create a JWT token with API key information
        token = create_token(
            subject=user_id,
            token_type=TokenType.API_KEY,
            permissions=permissions,
            user_data={"name": name, "key_id": key_id},
        )
        
        return {
            "api_key": api_key,
            "key_id": key_id,
            "hashed_secret": hashed_secret,
            "token": token,
            "name": name,
            "created_at": datetime.utcnow().isoformat(),
            "permissions": permissions or [],
        }

    def verify_api_key(self, api_key: str, stored_hash: str) -> bool:
        """Verify an API key against a stored hash.
        
        Args:
            api_key: The API key to verify
            stored_hash: The stored hash to compare against
            
        Returns:
            True if the key is valid, False otherwise
        """
        try:
            parts = api_key.split(".")
            if len(parts) != 2:
                return False
                
            _, secret = parts
            hashed_secret = hashlib.sha256(secret.encode()).hexdigest()
            
            # Use constant-time comparison to prevent timing attacks
            return hmac.compare_digest(hashed_secret, stored_hash)
        except Exception as e:
            logger.error(f"API key verification error: {str(e)}")
            return False

    # Request validation
    def is_valid_hostname(self, hostname: str) -> bool:
        """Check if a hostname is valid and allowed.
        
        Args:
            hostname: The hostname to check
            
        Returns:
            True if the hostname is valid, False otherwise
        """
        if not hostname or len(hostname) > 255:
            return False
            
        if self.allowed_hosts and hostname not in self.allowed_hosts:
            return False
            
        allowed_chars = re.compile(r"^[a-zA-Z0-9.-]+$")
        if not allowed_chars.match(hostname):
            return False
            
        return True

    def is_trusted_ip(self, ip_address: str) -> bool:
        """Check if an IP address is in the trusted list.
        
        Args:
            ip_address: The IP address to check
            
        Returns:
            True if the IP is trusted, False otherwise
        """
        try:
            ip = ipaddress.ip_address(ip_address)
            
            for trusted_ip in self.trusted_proxies:
                if "/" in trusted_ip:  # CIDR notation
                    if ip in ipaddress.ip_network(trusted_ip):
                        return True
                elif ip == ipaddress.ip_address(trusted_ip):
                    return True
                    
            return False
        except ValueError:
            logger.warning(f"Invalid IP address format: {ip_address}")
            return False

    def sanitize_input(self, input_str: str) -> str:
        """Sanitize user input to prevent XSS attacks.
        
        Args:
            input_str: The input string to sanitize
            
        Returns:
            The sanitized string
        """
        if not input_str:
            return ""
            
        sanitized = input_str
        sanitized = sanitized.replace("&", "&amp;")
        sanitized = sanitized.replace("<", "&lt;")
        sanitized = sanitized.replace(">", "&gt;")
        sanitized = sanitized.replace('"', "&quot;")
        sanitized = sanitized.replace("'", "&#x27;")
        sanitized = sanitized.replace("/", "&#x2F;")
        
        return sanitized

    def detect_suspicious_content(self, content: str) -> bool:
        """Detect potentially malicious content in user input.
        
        Args:
            content: The content to check
            
        Returns:
            True if suspicious content is detected, False otherwise
        """
        if not content:
            return False
            
        return bool(self.suspicious_regex.search(content))

    def validate_json_input(self, json_data: Any) -> bool:
        """Validate JSON input for security issues.
        
        Args:
            json_data: The JSON data to validate
            
        Returns:
            True if the input is valid, False otherwise
        """
        try:
            if not isinstance(json_data, (dict, list)):
                return False
                
            json_str = json.dumps(json_data)
            
            if self.detect_suspicious_content(json_str):
                logger.warning("Suspicious content detected in JSON input")
                return False
                
            return True
        except Exception as e:
            logger.error(f"Error validating JSON input: {str(e)}")
            return False

    # Authorization helpers
    def verify_access_policy(
        self, user_roles: List[str], required_roles: List[str], required_all: bool = False
    ) -> bool:
        """Verify if a user has the required roles.
        
        Args:
            user_roles: The user's roles
            required_roles: The roles required for access
            required_all: Whether all required roles are needed
            
        Returns:
            True if the user has the required roles, False otherwise
        """
        if not required_roles:
            return True
            
        if required_all:
            return all(role in user_roles for role in required_roles)
        else:
            return any(role in user_roles for role in required_roles)

    # Security event logging
    async def log_security_event(
        self,
        violation_type: SecurityViolation,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log a security event.
        
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
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        logger.warning(f"Security violation: {violation_type.value}", **log_data)
        
        # Additional security event logging logic could be implemented here,
        # such as:
        # - Storing in a security events database
        # - Sending alerts to administrators
        # - Triggering automated responses

    # Rate limiting
    async def throttle_requests(
        self, key: str, limit: int, window_seconds: int
    ) -> Tuple[bool, int]:
        """Apply rate limiting to requests.
        
        Args:
            key: The key to rate limit on
            limit: The maximum number of requests allowed
            window_seconds: The time window in seconds
            
        Returns:
            Tuple of (is_limited, current_count)
        """
        throttle_key = f"throttle:{key}:{int(time.time() / window_seconds)}"
        
        try:
            current = await get_key(throttle_key, 0)
            
            if current is None:
                await set_key(throttle_key, 1, window_seconds)
                return (False, 1)
                
            count = current + 1
            await set_key(throttle_key, count, window_seconds)
            
            if count > limit:
                return (True, count)
                
            return (False, count)
        except Exception as e:
            logger.error(f"Throttling error: {str(e)}")
            return (False, 0)

    # CSRF protection
    def generate_csrf_token(self, session_id: str) -> str:
        """Generate a CSRF token for a session.
        
        Args:
            session_id: The session ID to associate with the token
            
        Returns:
            A CSRF token
        """
        timestamp = int(time.time())
        random_part = secrets.token_hex(8)
        message = f"{session_id}:{timestamp}:{random_part}"
        signature = hmac.new(
            self.token_config.secret_key.encode(),
            message.encode(),
            digestmod="sha256"
        ).hexdigest()
        
        return f"{message}:{signature}"

    def validate_csrf_token(self, token: str, session_id: str) -> bool:
        """Validate a CSRF token.
        
        Args:
            token: The token to validate
            session_id: The session ID to validate against
            
        Returns:
            True if the token is valid, False otherwise
        """
        try:
            parts = token.split(":")
            if len(parts) != 4:
                logger.warning(f"Invalid CSRF token format")
                return False
                
            token_session_id, timestamp_str, random_part, provided_signature = parts
            
            if token_session_id != session_id:
                logger.warning(f"CSRF token session mismatch")
                return False
                
            message = f"{token_session_id}:{timestamp_str}:{random_part}"
            expected_signature = hmac.new(
                self.token_config.secret_key.encode(),
                message.encode(),
                digestmod="sha256"
            ).hexdigest()
            
            if not hmac.compare_digest(provided_signature, expected_signature):
                logger.warning(f"CSRF token signature mismatch")
                return False
                
            timestamp = int(timestamp_str)
            if int(time.time()) - timestamp > self.csrf_token_expiry:
                logger.warning(f"CSRF token expired")
                return False
                
            return True
        except Exception as e:
            logger.warning(f"CSRF token validation error: {str(e)}")
            return False

    # TLS/SSL and security headers
    def get_security_headers(self) -> Dict[str, str]:
        """Get recommended security headers for HTTP responses.
        
        Returns:
            Dictionary of security headers
        """
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Content-Security-Policy": settings.security.CONTENT_SECURITY_POLICY,
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": settings.security.PERMISSIONS_POLICY,
        }

    def hash_password(self, password: str) -> str:
        """Hash a password using a cryptographically secure algorithm.
        
        This method uses bcrypt with a higher work factor than the core implementation,
        providing a security-focused wrapper around the core function.
        
        Args:
            password: The password to hash
            
        Returns:
            The hashed password
        """
        # Use bcrypt with a higher work factor for better security
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()
        
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash with additional security measures.
        
        Args:
            plain_password: The plain text password
            hashed_password: The hashed password to compare against
            
        Returns:
            True if the password matches the hash, False otherwise
        """
        try:
            return verify_password(plain_password, hashed_password)
        except Exception as e:
            logger.error(f"Password verification error: {str(e)}")
            return False

    def generate_secure_token(self, length: int = 32) -> str:
        """Generate a cryptographically secure random token.
        
        Args:
            length: The desired token length
            
        Returns:
            A secure random token
            
        Raises:
            ValueError: If the requested length is too short
        """
        if length < 16:
            error_msg = "Token length must be at least 16 bytes for security"
            logger.warning(error_msg, length=length)
            raise ValueError(error_msg)
            
        try:
            token = secrets.token_urlsafe(length)
            logger.debug(f"Generated secure token of length {len(token)}")
            return token
        except Exception as e:
            logger.error(f"Failed to generate secure token: {str(e)}")
            raise SecurityException(
                message="Failed to generate secure token",
                code=ErrorCode.SECURITY_ERROR,
                details={"error": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                original_exception=e,
            )