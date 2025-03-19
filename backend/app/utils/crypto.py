# app/utils/crypto.py
"""
Cryptography utility module for handling secure encryption, decryption, and token generation.

This module provides functions for encrypting and decrypting sensitive data using Fernet
symmetric encryption, as well as utilities for generating secure random tokens. It uses
cryptography's Fernet implementation with PBKDF2HMAC key derivation for enhanced security.

All functions include proper error handling and logging to ensure security operations
are traceable and debuggable while maintaining security best practices.
"""

from __future__ import annotations

import base64
import os
from typing import Optional, Union, cast

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from app.core.config import settings
from app.core.exceptions import (
    ConfigurationException,
    SecurityException,
    ErrorCode,
)
from app.core.logging import get_logger

# Initialize structured logger
logger = get_logger("app.utils.crypto")


class CryptoError(SecurityException):
    """Exception raised for cryptographic operations failures."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.SECURITY_ERROR,
        details: Optional[dict] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize CryptoError.

        Args:
            message: Human-readable error description
            code: Error code from ErrorCode enum
            details: Additional error context
            original_exception: Original exception that caused this error
        """
        super().__init__(
            message=message,
            code=code,
            details=details or {},
            status_code=500,
            original_exception=original_exception,
        )


def _get_encryption_key() -> bytes:
    """Generate encryption key using PBKDF2HMAC with SHA-256.

    The key is derived from the application secret key using a salt specified
    in the application settings. This provides protection against rainbow table attacks.

    Returns:
        bytes: Base64-encoded encryption key

    Raises:
        CryptoError: If key derivation fails
        ConfigurationException: If required settings are missing
    """
    try:
        salt = settings.CHAT_ENCRYPTION_SALT.encode()
        if not salt:
            logger.warning("Encryption salt not configured, using default")
            salt = b"crown_nexus_chat_salt"

        if not settings.SECRET_KEY:
            error_msg = "SECRET_KEY not configured"
            logger.error(error_msg)
            raise ConfigurationException(
                message=error_msg,
                code=ErrorCode.CONFIGURATION_ERROR,
                details={"missing_setting": "SECRET_KEY"},
            )

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(settings.SECRET_KEY.encode()))
        logger.debug("Encryption key derived successfully")
        return key
    except Exception as e:
        logger.error(f"Failed to derive encryption key: {str(e)}", exc_info=True)
        raise CryptoError(
            message="Failed to derive encryption key", original_exception=e
        ) from e


# Initialize Fernet instance with derived key
try:
    _fernet = Fernet(_get_encryption_key())
    logger.info("Fernet encryption initialized successfully")
except Exception as e:
    logger.critical("Failed to initialize Fernet encryption", exc_info=True)
    raise CryptoError(
        message="Failed to initialize encryption system", original_exception=e
    ) from e


def encrypt_message(message: str) -> str:
    """Encrypt a message using Fernet symmetric encryption.

    Args:
        message: Plaintext message to encrypt

    Returns:
        str: Base64-encoded encrypted message

    Raises:
        CryptoError: If encryption fails
    """
    if not message:
        logger.warning("Attempted to encrypt empty message")
        return ""

    try:
        encrypted = _fernet.encrypt(message.encode())
        return encrypted.decode()
    except Exception as e:
        logger.error(f"Encryption failed: {str(e)}", exc_info=True)
        raise CryptoError(
            message="Failed to encrypt message", original_exception=e
        ) from e


def decrypt_message(encrypted_message: str) -> str:
    """Decrypt a Fernet-encrypted message.

    Args:
        encrypted_message: Base64-encoded encrypted message

    Returns:
        str: Decrypted plaintext message

    Raises:
        CryptoError: If decryption fails or token is invalid
    """
    if not encrypted_message:
        logger.warning("Attempted to decrypt empty message")
        return ""

    try:
        decrypted = _fernet.decrypt(encrypted_message.encode())
        return decrypted.decode()
    except InvalidToken as e:
        logger.error("Invalid token for decryption", exc_info=True)
        raise CryptoError(
            message="Invalid encryption token",
            code=ErrorCode.SECURITY_ERROR,
            details={"error_type": "invalid_token"},
            original_exception=e,
        ) from e
    except Exception as e:
        logger.error(f"Decryption failed: {str(e)}", exc_info=True)
        raise CryptoError(
            message="Failed to decrypt message", original_exception=e
        ) from e


def generate_secure_token(length: int = 32) -> str:
    """Generate a cryptographically secure random token.

    Args:
        length: Length of the token in bytes (resulting hex string will be twice this length)

    Returns:
        str: Hexadecimal string representation of the random token

    Raises:
        CryptoError: If token generation fails
        ValueError: If length is less than 16
    """
    if length < 16:
        error_msg = "Token length must be at least 16 bytes for security"
        logger.warning(error_msg, length=length)
        raise ValueError(error_msg)

    try:
        token = os.urandom(length).hex()
        logger.debug(f"Generated secure token of length {len(token)}")
        return token
    except Exception as e:
        logger.error(f"Failed to generate secure token: {str(e)}", exc_info=True)
        raise CryptoError(
            message="Failed to generate secure token", original_exception=e
        ) from e
