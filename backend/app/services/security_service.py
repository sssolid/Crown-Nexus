# app/services/security_service.py
from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import ipaddress
import json
import os
import re
import secrets
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Pattern, Set, Tuple, Union, TypedDict

import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from fastapi import HTTPException, Request, Response, status
from jose import jwt
from pydantic import BaseModel, EmailStr, Field, SecretStr

from app.core.config import settings
from app.core.exceptions import (
    AuthenticationException,
    ErrorCode,
    SecurityException,
    ValidationException
)
from app.core.logging import get_logger
from app.models.user import User
from app.services.interfaces import ServiceInterface
from app.utils.redis_manager import get_key, set_key, delete_key

logger = get_logger("app.services.security_service")


class TokenType(str, Enum):
    """Enum for different types of tokens."""

    ACCESS = "access"
    REFRESH = "refresh"
    RESET_PASSWORD = "reset_password"
    EMAIL_VERIFICATION = "email_verification"
    INVITATION = "invitation"
    API_KEY = "api_key"
    CSRF = "csrf"
    SESSION = "session"


class SecurityViolation(str, Enum):
    """Enum for different types of security violations."""

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
    """Model for password policy configuration."""

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


class TokenClaimsModel(BaseModel):
    """Model for token claims."""

    sub: str
    exp: datetime
    iat: datetime
    jti: str
    type: TokenType
    role: Optional[str] = None
    permissions: Optional[List[str]] = None
    user_data: Optional[Dict[str, Any]] = None


class TokenPayload(TypedDict, total=False):
    """TypedDict for token payload."""

    sub: str
    exp: int
    iat: int
    jti: str
    type: str
    role: str
    permissions: List[str]
    user_data: Dict[str, Any]


@dataclass
class TokenConfig:
    """Configuration for token generation."""

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    reset_token_expire_minutes: int = 60
    verification_token_expire_days: int = 7
    invitation_token_expire_days: int = 14


class SecurityService:
    """Service for security-related operations.

    Handles authentication, authorization, encryption, token management,
    password policies, and security monitoring.
    """

    def __init__(self) -> None:
        """Initialize the security service."""
        # Configuration
        self.token_config = TokenConfig(
            secret_key=settings.security.SECRET_KEY,
            algorithm=settings.security.ALGORITHM,
            access_token_expire_minutes=settings.security.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        self.password_policy = PasswordPolicy()

        # Define common security patterns
        self.patterns = {
            "email": re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"),
            "phone": re.compile(r"^\+?[0-9]{10,15}$"),
            "username": re.compile(r"^[a-zA-Z0-9_-]{3,32}$"),
            "url": re.compile(
                r"^(https?:\/\/)?"  # protocol
                r"(([a-z\d]([a-z\d-]*[a-z\d])*)\.)+[a-z]{2,}|"  # domain name
                r"((\d{1,3}\.){3}\d{1,3}))"  # OR ip (v4) address
                r"(\:\d+)?(\/[-a-z\d%_.~+]*)*"  # port and path
                r"(\?[;&a-z\d%_.~+=-]*)?"  # query string
                r"(\#[-a-z\d_]*)?$",  # fragment locator
                re.IGNORECASE,
            ),
        }

        # Token blacklist cache prefix
        self.token_blacklist_prefix = "token:blacklist:"

        # Security configurations
        self.allowed_hosts: Set[str] = set(settings.security.ALLOWED_HOSTS)
        self.trusted_proxies: Set[str] = set(settings.security.TRUSTED_PROXIES)
        self.csrf_token_expiry: int = settings.security.CSRF_TOKEN_EXPIRY

        # Suspicious patterns for detecting potential attacks
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
            r"file://"
        ]
        self.suspicious_regex = re.compile("|".join(self.suspicious_patterns), re.IGNORECASE)

        # Set up encryption
        self._setup_encryption()

        logger.info("SecurityService initialized")

    async def initialize(self) -> None:
        """Initialize the security service."""
        logger.debug("Initializing security service")

        # Load common passwords list for the password policy if enabled
        if self.password_policy.prevent_common_passwords:
            await self._load_common_passwords()

    async def shutdown(self) -> None:
        """Shutdown the security service."""
        logger.debug("Shutting down security service")

    def _setup_encryption(self) -> None:
        """Set up encryption keys and utilities."""
        # Use environment variable or settings for key
        base_key = settings.security.SECRET_KEY.encode()

        # Derive a proper key for Fernet
        salt = b"security_service_salt"  # Fixed salt for consistency
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(base_key))

        # Initialize Fernet cipher for encryption/decryption
        self.cipher = Fernet(key)

    async def _load_common_passwords(self) -> None:
        """Load list of common passwords to check against."""
        self.common_passwords = set()
        try:
            # Check if passwords file exists
            passwords_file = os.path.join(
                settings.BASE_DIR, "app", "data", "common_passwords.txt"
            )
            if os.path.exists(passwords_file):
                with open(passwords_file, "r") as f:
                    for line in f:
                        self.common_passwords.add(line.strip())
                logger.debug(f"Loaded {len(self.common_passwords)} common passwords")
            else:
                # If file doesn't exist, add some most common passwords
                self.common_passwords = {
                    "password", "123456", "123456789", "qwerty", "12345678",
                    "111111", "1234567890", "1234567", "password1", "12345",
                    "123123", "000000", "iloveyou", "1234", "1q2w3e4r", "admin"
                }
                logger.debug(f"Using default list of {len(self.common_passwords)} common passwords")
        except Exception as e:
            logger.error(f"Error loading common passwords: {str(e)}")
            # Add some most common as fallback
            self.common_passwords = {
                "password", "123456", "123456789", "qwerty", "12345678"
            }

    def encrypt_data(self, data: Union[str, bytes, dict]) -> str:
        """Encrypt sensitive data.

        Args:
            data: Data to encrypt

        Returns:
            Encrypted data as a string
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
            encrypted_data: Encrypted data string

        Returns:
            Decrypted data

        Raises:
            SecurityException: If decryption fails
        """
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data)
            decrypted = self.cipher.decrypt(encrypted_bytes)
            result = decrypted.decode()

            # Try to parse as JSON if possible
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
                status_code=status.HTTP_400_BAD_REQUEST
            )

    def create_token(
        self,
        subject: Union[str, uuid.UUID],
        token_type: TokenType,
        expires_delta: Optional[timedelta] = None,
        role: Optional[str] = None,
        permissions: Optional[List[str]] = None,
        user_data: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Create a JWT token.

        Args:
            subject: Subject identifier (usually user ID)
            token_type: Type of token to create
            expires_delta: Optional custom expiration time
            role: Optional user role
            permissions: Optional list of permissions
            user_data: Optional additional user data

        Returns:
            Generated JWT token
        """
        # Determine expiration based on token type
        if expires_delta is None:
            if token_type == TokenType.ACCESS:
                expires_delta = timedelta(minutes=self.token_config.access_token_expire_minutes)
            elif token_type == TokenType.REFRESH:
                expires_delta = timedelta(days=self.token_config.refresh_token_expire_days)
            elif token_type == TokenType.RESET_PASSWORD:
                expires_delta = timedelta(minutes=self.token_config.reset_token_expire_minutes)
            elif token_type == TokenType.EMAIL_VERIFICATION:
                expires_delta = timedelta(days=self.token_config.verification_token_expire_days)
            elif token_type == TokenType.INVITATION:
                expires_delta = timedelta(days=self.token_config.invitation_token_expire_days)
            else:
                # Default expiration
                expires_delta = timedelta(minutes=30)

        # Get current time and calculate expiration
        now = datetime.utcnow()
        expire = now + expires_delta

        # Generate a token ID
        token_jti = str(uuid.uuid4())

        # Prepare the payload
        to_encode: TokenPayload = {
            "sub": str(subject),
            "exp": int(expire.timestamp()),
            "iat": int(now.timestamp()),
            "jti": token_jti,
            "type": token_type.value
        }

        # Add optional fields if provided
        if role:
            to_encode["role"] = role

        if permissions:
            to_encode["permissions"] = permissions

        if user_data:
            to_encode["user_data"] = user_data

        # Encode the token
        token = jwt.encode(
            to_encode,
            self.token_config.secret_key,
            algorithm=self.token_config.algorithm
        )

        logger.debug(f"Created {token_type.value} token for subject {subject}")
        return token

    async def validate_token(
        self,
        token: str,
        expected_type: Optional[TokenType] = None,
        verify_exp: bool = True,
        check_blacklist: bool = True,
    ) -> TokenClaimsModel:
        """Validate and decode a JWT token.

        Args:
            token: The JWT token to validate
            expected_type: Optional expected token type
            verify_exp: Whether to verify token expiration
            check_blacklist: Whether to check if token is blacklisted

        Returns:
            Validated token claims

        Raises:
            AuthenticationException: If token validation fails
        """
        try:
            # Decode the token
            payload = jwt.decode(
                token,
                self.token_config.secret_key,
                algorithms=[self.token_config.algorithm],
                options={"verify_exp": verify_exp}
            )

            # Convert payload timestamps to datetime
            payload["exp"] = datetime.fromtimestamp(payload["exp"])
            payload["iat"] = datetime.fromtimestamp(payload["iat"])

            # Parse into model
            token_data = TokenClaimsModel(**payload)

            # Check token type if specified
            if expected_type and token_data.type != expected_type:
                logger.warning(
                    f"Token type mismatch: expected {expected_type}, got {token_data.type}",
                    subject=token_data.sub
                )
                raise AuthenticationException(
                    message="Invalid token type",
                    code=ErrorCode.INVALID_TOKEN,
                    details={"expected_type": expected_type.value, "actual_type": token_data.type}
                )

            # Check if token is blacklisted
            if check_blacklist:
                is_blacklisted = await self.is_token_blacklisted(token_data.jti)
                if is_blacklisted:
                    logger.warning(f"Blacklisted token used", jti=token_data.jti, subject=token_data.sub)
                    raise AuthenticationException(
                        message="Token has been revoked",
                        code=ErrorCode.INVALID_TOKEN
                    )

            return token_data

        except jwt.ExpiredSignatureError:
            logger.warning("Expired token used")
            raise AuthenticationException(
                message="Token has expired",
                code=ErrorCode.TOKEN_EXPIRED
            )
        except jwt.JWTError as e:
            logger.warning(f"JWT validation error: {str(e)}")
            raise AuthenticationException(
                message="Could not validate credentials",
                code=ErrorCode.INVALID_TOKEN,
                details={"error": str(e)}
            )
        except ValidationException as e:
            logger.warning(f"Token payload validation error: {str(e)}")
            raise AuthenticationException(
                message="Token has invalid format",
                code=ErrorCode.INVALID_TOKEN,
                details={"error": str(e)}
            )

    async def blacklist_token(self, token: str) -> None:
        """Add a token to the blacklist.

        Args:
            token: The token to blacklist

        Raises:
            AuthenticationException: If token validation fails
        """
        try:
            # Validate the token first
            token_data = await self.validate_token(token, verify_exp=False, check_blacklist=False)

            # Calculate TTL based on expiration
            now = datetime.utcnow()
            ttl = max(0, int((token_data.exp - now).total_seconds()))

            # Add to blacklist with expiration
            blacklist_key = f"{self.token_blacklist_prefix}{token_data.jti}"
            await set_key(blacklist_key, "1", ttl)

            logger.debug(f"Token blacklisted: {token_data.jti} for {ttl} seconds")

        except AuthenticationException:
            # If token is already invalid, no need to blacklist
            logger.debug("Attempted to blacklist an already invalid token")
            raise

    async def is_token_blacklisted(self, token_jti: str) -> bool:
        """Check if a token is blacklisted.

        Args:
            token_jti: Token ID to check

        Returns:
            True if token is blacklisted, False otherwise
        """
        blacklist_key = f"{self.token_blacklist_prefix}{token_jti}"
        value = await get_key(blacklist_key, None)
        return value is not None

    async def refresh_token_pair(self, refresh_token: str) -> Dict[str, str]:
        """Refresh access and refresh tokens using a refresh token.

        Args:
            refresh_token: The refresh token

        Returns:
            Dictionary with new access and refresh tokens

        Raises:
            AuthenticationException: If refresh token is invalid
        """
        # Validate the refresh token
        token_data = await self.validate_token(refresh_token, expected_type=TokenType.REFRESH)

        # Blacklist the used refresh token
        await self.blacklist_token(refresh_token)

        # Create new tokens
        new_access_token = self.create_token(
            subject=token_data.sub,
            token_type=TokenType.ACCESS,
            role=token_data.role,
            permissions=token_data.permissions,
            user_data=token_data.user_data
        )

        new_refresh_token = self.create_token(
            subject=token_data.sub,
            token_type=TokenType.REFRESH,
            role=token_data.role,
            permissions=token_data.permissions,
            user_data=token_data.user_data
        )

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "expires_in": self.token_config.access_token_expire_minutes * 60
        }

    def hash_password(self, password: str) -> str:
        """Hash a password securely.

        Args:
            password: Plain text password

        Returns:
            Hashed password
        """
        # Use bcrypt with appropriate work factor
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash.

        Args:
            plain_password: Plain text password
            hashed_password: Hashed password

        Returns:
            True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(
                plain_password.encode(),
                hashed_password.encode()
            )
        except Exception as e:
            logger.error(f"Password verification error: {str(e)}")
            return False

    async def validate_password_policy(self, password: str, user_id: Optional[str] = None) -> Tuple[bool, Optional[str]]:
        """Validate a password against the password policy.

        Args:
            password: Password to validate
            user_id: Optional user ID for password history check

        Returns:
            Tuple of (valid, error_message)
        """
        # Check length
        if len(password) < self.password_policy.min_length:
            return False, f"Password must be at least {self.password_policy.min_length} characters long"

        if len(password) > self.password_policy.max_length:
            return False, f"Password cannot be longer than {self.password_policy.max_length} characters"

        # Check complexity requirements
        if self.password_policy.require_uppercase and not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"

        if self.password_policy.require_lowercase and not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"

        if self.password_policy.require_digit and not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"

        if self.password_policy.require_special_char and not any(not c.isalnum() for c in password):
            return False, "Password must contain at least one special character"

        # Check against common passwords
        if self.password_policy.prevent_common_passwords and password.lower() in self.common_passwords:
            return False, "Password is too common and easily guessed"

        # Check password history if user_id provided
        if user_id and self.password_policy.password_history_count > 0:
            # This would normally check against stored password history
            # For simplicity, we're assuming it passes
            pass

        return True, None

    def generate_secure_token(self, length: int = 32) -> str:
        """Generate a cryptographically secure token.

        Args:
            length: Length of the token in bytes

        Returns:
            Secure random token
        """
        return secrets.token_urlsafe(length)

    def generate_csrf_token(self, session_id: str) -> str:
        """Generate a CSRF token bound to a session.

        Args:
            session_id: Session ID to bind the token to

        Returns:
            CSRF token
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
            token: CSRF token to validate
            session_id: Session ID the token should be bound to

        Returns:
            True if token is valid, False otherwise
        """
        try:
            # Split token into parts
            parts = token.split(":")
            if len(parts) != 4:
                logger.warning(f"Invalid CSRF token format")
                return False

            # Extract parts
            token_session_id, timestamp_str, random_part, provided_signature = parts

            # Verify session ID
            if token_session_id != session_id:
                logger.warning(f"CSRF token session mismatch")
                return False

            # Verify signature
            message = f"{token_session_id}:{timestamp_str}:{random_part}"
            expected_signature = hmac.new(
                self.token_config.secret_key.encode(),
                message.encode(),
                digestmod="sha256"
            ).hexdigest()

            if not hmac.compare_digest(provided_signature, expected_signature):
                logger.warning(f"CSRF token signature mismatch")
                return False

            # Check expiration
            timestamp = int(timestamp_str)
            if int(time.time()) - timestamp > self.csrf_token_expiry:
                logger.warning(f"CSRF token expired")
                return False

            return True

        except Exception as e:
            logger.warning(f"CSRF token validation error: {str(e)}")
            return False

    def is_valid_hostname(self, hostname: str) -> bool:
        """Validate a hostname against allowed hosts.

        Args:
            hostname: Hostname to validate

        Returns:
            True if hostname is valid, False otherwise
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
        """Check if an IP address is in the trusted proxies list.

        Args:
            ip_address: IP address to check

        Returns:
            True if IP is trusted, False otherwise
        """
        try:
            ip = ipaddress.ip_address(ip_address)

            for trusted_ip in self.trusted_proxies:
                if "/" in trusted_ip:
                    # It's a network
                    if ip in ipaddress.ip_network(trusted_ip):
                        return True
                elif ip == ipaddress.ip_address(trusted_ip):
                    # It's a specific IP
                    return True

            return False

        except ValueError:
            logger.warning(f"Invalid IP address format: {ip_address}")
            return False

    def sanitize_input(self, input_str: str) -> str:
        """Sanitize user input to prevent XSS attacks.

        Args:
            input_str: User input string

        Returns:
            Sanitized string
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
        """Detect potentially malicious content.

        Args:
            content: Content to check

        Returns:
            True if suspicious content is detected, False otherwise
        """
        if not content:
            return False

        return bool(self.suspicious_regex.search(content))

    def validate_json_input(self, json_data: Any) -> bool:
        """Validate JSON input for security issues.

        Args:
            json_data: JSON data to validate

        Returns:
            True if JSON is valid and safe, False otherwise
        """
        try:
            if not isinstance(json_data, (dict, list)):
                return False

            # Convert to string to check for suspicious patterns
            json_str = json.dumps(json_data)
            if self.detect_suspicious_content(json_str):
                logger.warning("Suspicious content detected in JSON input")
                return False

            return True

        except Exception as e:
            logger.error(f"Error validating JSON input: {str(e)}")
            return False

    def verify_access_policy(self, user_roles: List[str], required_roles: List[str], required_all: bool = False) -> bool:
        """Verify if a user has the required roles.

        Args:
            user_roles: List of user roles
            required_roles: List of required roles
            required_all: Whether all required roles are needed

        Returns:
            True if user has required roles, False otherwise
        """
        if not required_roles:
            return True

        if required_all:
            return all(role in user_roles for role in required_roles)
        else:
            return any(role in user_roles for role in required_roles)

    async def log_security_event(
        self,
        violation_type: SecurityViolation,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log a security event.

        Args:
            violation_type: Type of security violation
            user_id: Optional user ID
            ip_address: Optional IP address
            details: Optional additional details
        """
        # This would typically use the AuditService
        # For now, just log to the application logs
        log_data = {
            "violation_type": violation_type,
            "user_id": user_id,
            "ip_address": ip_address,
            "details": details or {},
            "timestamp": datetime.utcnow().isoformat()
        }

        logger.warning(
            f"Security violation: {violation_type.value}",
            **log_data
        )

    def generate_api_key(self, user_id: str, name: str, permissions: Optional[List[str]] = None) -> Dict[str, str]:
        """Generate an API key for a user.

        Args:
            user_id: User ID
            name: API key name
            permissions: Optional list of permissions

        Returns:
            Dictionary with API key details
        """
        # Generate a unique key ID
        key_id = str(uuid.uuid4())

        # Generate the secret part
        secret = secrets.token_urlsafe(32)

        # Hash the secret for storage
        hashed_secret = hashlib.sha256(secret.encode()).hexdigest()

        # Generate the full API key (ID.SECRET)
        api_key = f"{key_id}.{secret}"

        # Create JWT token for permissions
        token = self.create_token(
            subject=user_id,
            token_type=TokenType.API_KEY,
            permissions=permissions,
            user_data={"name": name, "key_id": key_id}
        )

        return {
            "api_key": api_key,
            "key_id": key_id,
            "hashed_secret": hashed_secret,
            "token": token,
            "name": name,
            "created_at": datetime.utcnow().isoformat(),
            "permissions": permissions or []
        }

    def verify_api_key(self, api_key: str, stored_hash: str) -> bool:
        """Verify an API key against a stored hash.

        Args:
            api_key: API key to verify
            stored_hash: Stored hash to verify against

        Returns:
            True if API key is valid, False otherwise
        """
        try:
            # Split the API key into ID and secret
            parts = api_key.split(".")
            if len(parts) != 2:
                return False

            _, secret = parts

            # Hash the secret
            hashed_secret = hashlib.sha256(secret.encode()).hexdigest()

            # Compare with stored hash
            return hmac.compare_digest(hashed_secret, stored_hash)

        except Exception as e:
            logger.error(f"API key verification error: {str(e)}")
            return False

    async def throttle_requests(
        self,
        key: str,
        limit: int,
        window_seconds: int
    ) -> Tuple[bool, int]:
        """Throttle requests to prevent abuse.

        Args:
            key: Throttling key (e.g., IP address or user ID)
            limit: Maximum number of requests
            window_seconds: Time window in seconds

        Returns:
            Tuple of (throttled, current_count)
        """
        # Normalize the key
        throttle_key = f"throttle:{key}:{int(time.time() / window_seconds)}"

        try:
            # Get current count
            current = await get_key(throttle_key, 0)

            if current is None:
                # Key doesn't exist, create it
                await set_key(throttle_key, 1, window_seconds)
                return False, 1

            # Increment count
            count = current + 1
            await set_key(throttle_key, count, window_seconds)

            # Check if limit exceeded
            if count > limit:
                return True, count

            return False, count

        except Exception as e:
            logger.error(f"Throttling error: {str(e)}")
            return False, 0
