from __future__ import annotations

"""Security service implementation.

This module provides a unified service interface for security functions throughout
the application, integrating with the application's dependency management, metrics,
caching, and error handling systems.
"""

import time
from typing import Any, Dict, List, Optional, Tuple, Union

from app.core.dependency_manager import get_service, register_service
from app.core.error import ErrorContext, handle_exception, report_error
from app.core.exceptions import AuthenticationException, SecurityException
from app.core.security.api_keys import ApiKeyManager
from app.core.security.csrf import CsrfManager
from app.core.security.encryption import EncryptionManager
from app.core.security.models import ApiKeyData, TokenClaimsModel, TokenPair, TokenType
from app.core.security.passwords import PasswordManager
from app.core.security.tokens import (
    TokenManager,
    add_token_to_blacklist,
    decode_token,
    is_token_blacklisted,
)
from app.core.security.validation import ValidationManager
from app.logging import get_logger

logger = get_logger("app.core.security.service")


class SecurityService:
    """Comprehensive security service for the application.

    This service integrates all security components (tokens, passwords, encryption, etc.)
    and connects them with the application's core systems like metrics, caching,
    error handling, and event publication.
    """

    def __init__(self, db=None) -> None:
        """Initialize the security service.

        Args:
            db: Optional database session for operations requiring database access
        """
        self.db = db
        self.logger = get_logger("app.core.security.service")

        # Initialize managers
        self.token_manager = TokenManager()
        self.password_manager = PasswordManager()
        self.api_key_manager = ApiKeyManager()
        self.encryption_manager = EncryptionManager()
        self.csrf_manager = CsrfManager()
        self.validation_manager = ValidationManager()

        # Get core services
        try:
            self.metrics_service = get_service("metrics_service")
        except Exception as e:
            self.logger.warning(f"Metrics service not available: {str(e)}")
            self.metrics_service = None

        try:
            self.cache_service = get_service("cache_service")
        except Exception as e:
            self.logger.warning(f"Cache service not available: {str(e)}")
            self.cache_service = None

        try:
            self.event_service = get_service("event_service")
        except Exception as e:
            self.logger.warning(f"Event service not available: {str(e)}")
            self.event_service = None

        try:
            self.error_service = get_service("error_service")
        except Exception as e:
            self.logger.warning(f"Error service not available: {str(e)}")
            self.error_service = None

        self.logger.info("Security service initialized")

    async def initialize(self) -> None:
        """Initialize the security service and its components."""
        self.logger.info("Initializing security service")
        # Any async initialization tasks would go here

    async def shutdown(self) -> None:
        """Shutdown the security service, releasing any resources."""
        self.logger.info("Shutting down security service")
        # Any cleanup tasks would go here

    # Token Management Methods

    async def validate_token(
        self, token: str, request_id: Optional[str] = None
    ) -> TokenClaimsModel:
        """Validate a JWT token with metrics tracking.

        Args:
            token: The JWT token to validate
            request_id: Optional request ID for tracking

        Returns:
            TokenClaimsModel: The validated token data

        Raises:
            AuthenticationException: If the token is invalid or expired
        """
        start_time = time.monotonic()
        valid = False
        error = None

        try:
            # Check cache for blacklisted token (optimization)
            if self.cache_service:
                token_data = await decode_token(token)
                blacklist_key = f"token:blacklist:{token_data.jti}"
                cached_result = await self.cache_service.get(blacklist_key)

                if cached_result is not None and cached_result == "1":
                    self.logger.warning(
                        f"Blacklisted token used (cache hit): {token_data.jti}",
                        request_id=request_id,
                    )
                    raise AuthenticationException(message="Token has been revoked")

            # Attempt validation
            token_data = await decode_token(token)
            valid = True
            return token_data

        except AuthenticationException as e:
            error = "auth_error"
            raise

        except Exception as e:
            error = "unexpected_error"
            handle_exception(e, request_id=request_id)
            raise

        finally:
            duration = time.monotonic() - start_time

            # Track metrics if available
            if self.metrics_service:
                self.metrics_service.observe_histogram(
                    "token_validation_duration_seconds",
                    duration,
                    {"success": str(valid), "error_type": error or "none"},
                )
                self.metrics_service.increment_counter(
                    "token_validations_total",
                    labels={"success": str(valid), "error_type": error or "none"},
                )

    async def create_token_pair(
        self,
        user_id: Union[str, int],
        role: str,
        permissions: Optional[List[str]] = None,
        user_data: Optional[Dict[str, Any]] = None,
    ) -> TokenPair:
        """Create a token pair (access token and refresh token).

        Args:
            user_id: The user ID to include in the token
            role: The user's role
            permissions: Optional list of user permissions
            user_data: Optional additional user data

        Returns:
            TokenPair: The generated access and refresh tokens
        """
        start_time = time.monotonic()

        try:
            token_pair = self.token_manager.create_token_pair(
                user_id=user_id, role=role, permissions=permissions, user_data=user_data
            )

            # Track the token creation
            if self.metrics_service:
                self.metrics_service.increment_counter(
                    "tokens_created_total", labels={"type": "token_pair", "role": role}
                )

            # Publish token creation event
            if self.event_service:
                await self.event_service.publish(
                    event_name="security.token_created",
                    payload={
                        "user_id": str(user_id),
                        "token_type": "token_pair",
                        "role": role,
                    },
                )

            return token_pair

        except Exception as e:
            handle_exception(e, user_id=str(user_id))
            raise

        finally:
            if self.metrics_service:
                duration = time.monotonic() - start_time
                self.metrics_service.observe_histogram(
                    "token_creation_duration_seconds", duration, {"type": "token_pair"}
                )

    async def revoke_token(
        self,
        token: str,
        user_id: str,
        reason: str = "manual_logout",
        request_id: Optional[str] = None,
    ) -> None:
        """Revoke a token and publish an event.

        Args:
            token: The token to revoke
            user_id: The user ID associated with the token
            reason: The reason for revocation
            request_id: Optional request ID for tracking

        Raises:
            AuthenticationException: If the token is invalid
        """
        try:
            # Validate and extract token data
            token_data = await self.validate_token(token, request_id)

            # Add token to blacklist
            await add_token_to_blacklist(token_data.jti, token_data.exp)

            # Add to cache for faster lookups
            if self.cache_service:
                cache_key = f"token:blacklist:{token_data.jti}"
                ttl = int((token_data.exp - token_data.iat).total_seconds())
                await self.cache_service.set(cache_key, "1", ttl=ttl)

            # Publish event for token revocation
            if self.event_service:
                await self.event_service.publish(
                    event_name="security.token_revoked",
                    payload={
                        "token_jti": token_data.jti,
                        "user_id": user_id,
                        "reason": reason,
                    },
                )

            self.logger.info(
                f"Token revoked: {token_data.jti}",
                user_id=user_id,
                reason=reason,
                request_id=request_id,
            )

        except Exception as e:
            handle_exception(e, user_id=user_id, request_id=request_id)
            raise

    async def refresh_tokens(
        self, refresh_token: str, request_id: Optional[str] = None
    ) -> TokenPair:
        """Refresh tokens using a valid refresh token.

        Args:
            refresh_token: The refresh token
            request_id: Optional request ID for tracking

        Returns:
            TokenPair: New access and refresh tokens

        Raises:
            AuthenticationException: If the refresh token is invalid
        """
        start_time = time.monotonic()
        success = False

        try:
            # Validate the refresh token
            token_data = await self.validate_token(refresh_token, request_id)

            # Verify it's a refresh token
            if token_data.type != TokenType.REFRESH:
                raise AuthenticationException(message="Invalid token type")

            # Blacklist the old token
            await add_token_to_blacklist(token_data.jti, token_data.exp)

            # Create new tokens
            token_pair = await self.create_token_pair(
                user_id=token_data.sub,
                role=token_data.role or "",
                permissions=token_data.permissions,
                user_data=token_data.user_data,
            )

            success = True
            return token_pair

        except Exception as e:
            handle_exception(e, request_id=request_id)
            raise

        finally:
            # Track metrics
            if self.metrics_service:
                duration = time.monotonic() - start_time
                self.metrics_service.observe_histogram(
                    "token_refresh_duration_seconds",
                    duration,
                    {"success": str(success)},
                )
                self.metrics_service.increment_counter(
                    "token_refresh_total", labels={"success": str(success)}
                )

    # Password Management Methods

    async def verify_password(
        self, plain_password: str, hashed_password: str, user_id: Optional[str] = None
    ) -> bool:
        """Verify a password against a hash with metrics tracking.

        Args:
            plain_password: The plaintext password
            hashed_password: The hashed password
            user_id: Optional user ID for tracking

        Returns:
            bool: True if the password is correct
        """
        start_time = time.monotonic()
        success = False

        try:
            success = self.password_manager.verify_password(
                plain_password, hashed_password
            )

            # Track failed attempts for security monitoring
            if not success and self.metrics_service and user_id:
                self.metrics_service.increment_counter(
                    "password_verification_failures_total",
                    labels={
                        "user_id": user_id[:8]
                    },  # Use truncated user_id for privacy
                )

            return success

        except Exception as e:
            handle_exception(e, user_id=user_id)
            return False

        finally:
            if self.metrics_service:
                duration = time.monotonic() - start_time
                self.metrics_service.observe_histogram(
                    "password_verification_duration_seconds",
                    duration,
                    {"success": str(success)},
                )
                self.metrics_service.increment_counter(
                    "password_verifications_total", labels={"success": str(success)}
                )

    def hash_password(self, password: str) -> str:
        """Hash a password using the configured password manager.

        Args:
            password: The plaintext password

        Returns:
            str: The hashed password
        """
        return self.password_manager.hash_password(password)

    async def validate_password_policy(
        self, password: str, user_id: Optional[str] = None
    ) -> Tuple[bool, Optional[str]]:
        """Validate a password against the policy.

        Args:
            password: The password to validate
            user_id: Optional user ID for checking password history

        Returns:
            Tuple[bool, Optional[str]]: Validity and error message
        """
        return await self.password_manager.validate_password_policy(password, user_id)

    # API Key Management Methods

    def generate_api_key(
        self, user_id: str, name: str, permissions: Optional[List[str]] = None
    ) -> ApiKeyData:
        """Generate an API key for a user.

        Args:
            user_id: The user ID to associate with the key
            name: A name for the API key
            permissions: Optional list of permissions

        Returns:
            ApiKeyData: The generated API key data
        """
        start_time = time.monotonic()

        try:
            api_key_data = self.api_key_manager.generate_api_key(
                user_id=user_id, name=name, permissions=permissions
            )

            # Track API key creation
            if self.metrics_service:
                self.metrics_service.increment_counter(
                    "api_keys_created_total", labels={"user_id": user_id[:8]}
                )

            # Publish API key creation event
            if self.event_service:
                self.event_service.publish(
                    event_name="security.api_key_created",
                    payload={
                        "user_id": user_id,
                        "key_id": api_key_data.key_id,
                        "name": name,
                    },
                )

            return api_key_data

        except Exception as e:
            handle_exception(e, user_id=user_id)
            raise

        finally:
            if self.metrics_service:
                duration = time.monotonic() - start_time
                self.metrics_service.observe_histogram(
                    "api_key_creation_duration_seconds", duration
                )

    def verify_api_key(self, api_key: str, stored_hash: str) -> bool:
        """Verify an API key against a stored hash.

        Args:
            api_key: The API key to verify
            stored_hash: The stored hash to compare against

        Returns:
            bool: True if the API key is valid
        """
        start_time = time.monotonic()
        success = False

        try:
            success = self.api_key_manager.verify_api_key(api_key, stored_hash)
            return success

        except Exception as e:
            handle_exception(e)
            return False

        finally:
            if self.metrics_service:
                duration = time.monotonic() - start_time
                self.metrics_service.observe_histogram(
                    "api_key_verification_duration_seconds",
                    duration,
                    {"success": str(success)},
                )
                self.metrics_service.increment_counter(
                    "api_key_verifications_total", labels={"success": str(success)}
                )

    # Encryption Methods

    def encrypt_data(self, data: Union[str, bytes, dict]) -> str:
        """Encrypt data using the encryption manager.

        Args:
            data: The data to encrypt

        Returns:
            str: The encrypted data

        Raises:
            SecurityException: If encryption fails
        """
        return self.encryption_manager.encrypt_data(data)

    def decrypt_data(self, encrypted_data: str) -> Union[str, dict]:
        """Decrypt data using the encryption manager.

        Args:
            encrypted_data: The encrypted data

        Returns:
            Union[str, dict]: The decrypted data

        Raises:
            SecurityException: If decryption fails
        """
        return self.encryption_manager.decrypt_data(encrypted_data)

    def generate_secure_token(self, length: int = 32) -> str:
        """Generate a cryptographically secure token.

        Args:
            length: The length of the token

        Returns:
            str: The generated token

        Raises:
            SecurityException: If token generation fails
        """
        return self.encryption_manager.generate_secure_token(length)

    # CSRF Protection Methods

    def generate_csrf_token(self, session_id: str) -> str:
        """Generate a CSRF token for a session.

        Args:
            session_id: The session ID

        Returns:
            str: The generated CSRF token
        """
        return self.csrf_manager.generate_token(session_id)

    def validate_csrf_token(self, token: str, session_id: str) -> bool:
        """Validate a CSRF token.

        Args:
            token: The CSRF token to validate
            session_id: The session ID to validate against

        Returns:
            bool: True if the token is valid
        """
        start_time = time.monotonic()
        valid = False

        try:
            valid = self.csrf_manager.validate_token(token, session_id)

            # Log CSRF failures as potential security issues
            if not valid:
                self.logger.warning(
                    "CSRF token validation failed",
                    session_id=session_id[:8],
                    token_prefix=token[:8] if token else None,
                )

            return valid

        except Exception as e:
            handle_exception(e)
            return False

        finally:
            if self.metrics_service:
                duration = time.monotonic() - start_time
                self.metrics_service.observe_histogram(
                    "csrf_validation_duration_seconds", duration, {"valid": str(valid)}
                )
                self.metrics_service.increment_counter(
                    "csrf_validations_total", labels={"valid": str(valid)}
                )

    # Input Validation Methods

    def is_trusted_ip(self, ip_address: str) -> bool:
        """Check if an IP address is in the trusted list.

        Args:
            ip_address: The IP address to check

        Returns:
            bool: True if the IP is trusted
        """
        return self.validation_manager.is_trusted_ip(ip_address)

    def detect_suspicious_content(self, content: str) -> bool:
        """Detect potentially suspicious content.

        Args:
            content: The content to check

        Returns:
            bool: True if suspicious content is detected
        """
        result = self.validation_manager.detect_suspicious_content(content)

        # Log and track suspicious content
        if result and self.metrics_service:
            self.logger.warning(
                "Suspicious content detected", content_length=len(content)
            )
            self.metrics_service.increment_counter(
                "suspicious_content_detections_total"
            )

        return result

    def sanitize_input(self, input_str: str) -> str:
        """Sanitize input to prevent XSS attacks.

        Args:
            input_str: The input string to sanitize

        Returns:
            str: The sanitized string
        """
        return self.validation_manager.sanitize_input(input_str)

    def get_security_headers(self) -> Dict[str, str]:
        """Get security headers for HTTP responses.

        Returns:
            Dict[str, str]: Dictionary of security headers
        """
        return self.validation_manager.get_security_headers()


# Create a singleton instance for dependency injection
_security_service: Optional[SecurityService] = None


@register_service
def get_security_service(db=None) -> SecurityService:
    """Get or create a SecurityService instance.

    Args:
        db: Optional database session

    Returns:
        SecurityService: The security service instance
    """
    global _security_service
    if _security_service is None:
        _security_service = SecurityService(db)
    elif db is not None:
        _security_service.db = db
    return _security_service
