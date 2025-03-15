# backend/app/utils/crypto.py
"""
Cryptography utilities.

This module provides cryptographic functions for:
- Message encryption and decryption
- Secure token generation
- Hashing utilities

These utilities ensure secure communication and data storage
throughout the application.
"""

from __future__ import annotations

import base64
import os
from typing import Optional

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from app.core.config import settings


# Initialize encryption key from settings
def _get_encryption_key() -> bytes:
    """
    Get or generate the encryption key for message content.
    
    Uses the configured secret key with PBKDF2 to derive a secure
    encryption key for Fernet symmetric encryption.
    
    Returns:
        bytes: The derived encryption key
    """
    # Use PBKDF2 to derive a key from the application secret key
    salt = settings.CHAT_ENCRYPTION_SALT.encode()
    if not salt:
        # If no salt is configured, use a default (not recommended for production)
        salt = b'crown_nexus_chat_salt'
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    
    key = base64.urlsafe_b64encode(
        kdf.derive(settings.SECRET_KEY.encode())
    )
    return key


# Initialize the Fernet cipher with our key
_fernet = Fernet(_get_encryption_key())


def encrypt_message(message: str) -> str:
    """
    Encrypt a message using Fernet symmetric encryption.
    
    Args:
        message: The plaintext message to encrypt
        
    Returns:
        str: The encrypted message as a base64-encoded string
    """
    encrypted = _fernet.encrypt(message.encode())
    return encrypted.decode()


def decrypt_message(encrypted_message: str) -> str:
    """
    Decrypt a Fernet-encrypted message.
    
    Args:
        encrypted_message: The encrypted message as a base64-encoded string
        
    Returns:
        str: The decrypted plaintext message
        
    Raises:
        cryptography.fernet.InvalidToken: If the message is invalid or corrupted
    """
    decrypted = _fernet.decrypt(encrypted_message.encode())
    return decrypted.decode()


def generate_secure_token(length: int = 32) -> str:
    """
    Generate a cryptographically secure random token.
    
    Args:
        length: The desired length of the token in bytes
        
    Returns:
        str: A secure random token as a hex string
    """
    return os.urandom(length).hex()
