# backend/app/services/security/encryption.py
"""Data encryption services.

This module provides services for encrypting and decrypting sensitive data,
using strong cryptographic algorithms.
"""
from __future__ import annotations

import base64
import binascii
import json
from typing import Any, Union

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from app.core.config import settings
from app.core.exceptions import SecurityException, ErrorCode
from app.core.logging import get_logger

logger = get_logger(__name__)


class EncryptionService:
    """Service for data encryption and decryption."""

    def __init__(self) -> None:
        """Initialize the encryption service."""
        # Set up encryption key
        self._setup_encryption()

    def _setup_encryption(self) -> None:
        """Set up encryption for sensitive data."""
        base_key = settings.SECRET_KEY.encode()
        salt = b"security_service_salt"
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        key = base64.urlsafe_b64encode(kdf.derive(base_key))
        self.cipher = Fernet(key)

    def encrypt_data(self, data: Union[str, bytes, dict]) -> str:
        """
        Encrypt sensitive data.

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
        """
        Decrypt encrypted data.

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
                details={"error": "Invalid encrypted data format"}
            ) from e

    def generate_secure_token(self, length: int = 32) -> str:
        """
        Generate a cryptographically secure random token.

        Args:
            length: The desired token length in bytes

        Returns:
            A secure random token

        Raises:
            ValueError: If the requested length is too short
        """
        import secrets

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
                details={"error": str(e)}
            ) from e
