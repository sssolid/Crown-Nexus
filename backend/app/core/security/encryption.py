from __future__ import annotations

"""Data encryption and secure token functionality.

This module provides functions for encrypting and decrypting data,
as well as generating cryptographically secure tokens.
"""

import base64
import binascii
import json
from typing import Union

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from app.core.config import settings
from app.core.exceptions import SecurityException, ErrorCode, ConfigurationException
from app.core.logging import get_logger

logger = get_logger(__name__)


def encrypt_data(data: Union[str, bytes, dict]) -> str:
    """Encrypt data.

    Args:
        data: The data to encrypt.

    Returns:
        str: The encrypted data as a base64-encoded string.

    Raises:
        SecurityException: If encryption fails.
    """
    cipher = _get_cipher()

    try:
        if isinstance(data, dict):
            data = json.dumps(data)

        if isinstance(data, str):
            data = data.encode()

        encrypted = cipher.encrypt(data)
        return base64.urlsafe_b64encode(encrypted).decode()

    except Exception as e:
        logger.error(f"Encryption error: {str(e)}")
        raise SecurityException(
            message="Failed to encrypt data",
            code=ErrorCode.SECURITY_ERROR,
            details={"error": str(e)},
        ) from e


def decrypt_data(encrypted_data: str) -> Union[str, dict]:
    """Decrypt data.

    Args:
        encrypted_data: The encrypted data as a base64-encoded string.

    Returns:
        Union[str, dict]: The decrypted data.

    Raises:
        SecurityException: If decryption fails.
    """
    cipher = _get_cipher()

    try:
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_data)
        decrypted = cipher.decrypt(encrypted_bytes)
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
        ) from e


def generate_secure_token(length: int = 32) -> str:
    """Generate a cryptographically secure random token.

    Args:
        length: The length of the token in bytes.

    Returns:
        str: The generated token.

    Raises:
        SecurityException: If token generation fails.
        ValueError: If the token length is too short.
    """
    if length < 16:
        error_msg = "Token length must be at least 16 bytes for security"
        logger.warning(error_msg, extra={"length": length})
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
        ) from e


def _get_cipher() -> Fernet:
    """Get or create a Fernet cipher using the application secret key.

    Returns:
        Fernet: A configured Fernet cipher.

    Raises:
        ConfigurationException: If the cipher cannot be created.
    """
    try:
        base_key = settings.SECRET_KEY.encode()
        salt = b"security_service_salt"

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000
        )
        key = base64.urlsafe_b64encode(kdf.derive(base_key))

        return Fernet(key)
    except Exception as e:
        logger.error(f"Failed to setup encryption: {str(e)}")
        raise ConfigurationException(
            message="Failed to initialize encryption",
            details={"error": str(e)},
        ) from e


class EncryptionManager:
    """Manager for encryption-related functionality."""

    def __init__(self) -> None:
        """Initialize the encryption manager."""
        self._setup_encryption()

    def _setup_encryption(self) -> None:
        """Set up encryption with a derived key."""
        try:
            base_key = settings.SECRET_KEY.encode()
            salt = b"security_service_salt"

            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000
            )
            key = base64.urlsafe_b64encode(kdf.derive(base_key))

            self.cipher = Fernet(key)
        except Exception as e:
            logger.error(f"Failed to setup encryption: {str(e)}")
            raise ConfigurationException(
                message="Failed to initialize encryption service",
                details={"error": str(e)},
            ) from e

    def encrypt_data(self, data: Union[str, bytes, dict]) -> str:
        """Encrypt data.

        Args:
            data: The data to encrypt.

        Returns:
            str: The encrypted data as a base64-encoded string.
        """
        return encrypt_data(data)

    def decrypt_data(self, encrypted_data: str) -> Union[str, dict]:
        """Decrypt data.

        Args:
            encrypted_data: The encrypted data as a base64-encoded string.

        Returns:
            Union[str, dict]: The decrypted data.
        """
        return decrypt_data(encrypted_data)

    def generate_secure_token(self, length: int = 32) -> str:
        """Generate a cryptographically secure random token.

        Args:
            length: The length of the token in bytes.

        Returns:
            str: The generated token.
        """
        return generate_secure_token(length)
