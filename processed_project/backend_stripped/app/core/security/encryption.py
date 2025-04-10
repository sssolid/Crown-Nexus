from __future__ import annotations
'Data encryption and secure token functionality.\n\nThis module provides functions for encrypting and decrypting data,\nas well as generating cryptographically secure tokens.\n'
import base64
import binascii
import json
from typing import Union
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from app.core.config import settings
from app.core.exceptions import SecurityException, ErrorCode, ConfigurationException
from app.logging import get_logger
logger = get_logger('app.core.security.encryption')
def encrypt_data(data: Union[str, bytes, dict]) -> str:
    cipher = _get_cipher()
    try:
        if isinstance(data, dict):
            data = json.dumps(data)
        if isinstance(data, str):
            data = data.encode()
        encrypted = cipher.encrypt(data)
        return base64.urlsafe_b64encode(encrypted).decode()
    except Exception as e:
        logger.error(f'Encryption error: {str(e)}')
        raise SecurityException(message='Failed to encrypt data', details={'error': str(e)}) from e
def decrypt_data(encrypted_data: str) -> Union[str, dict]:
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
        logger.error(f'Decryption error: {str(e)}')
        raise SecurityException(message='Failed to decrypt data', details={'error': 'Invalid encrypted data format'}) from e
def generate_secure_token(length: int=32) -> str:
    if length < 16:
        error_msg = 'Token length must be at least 16 bytes for security'
        logger.warning(error_msg, extra={'length': length})
        raise ValueError(error_msg)
    try:
        token = secrets.token_urlsafe(length)
        logger.debug(f'Generated secure token of length {len(token)}')
        return token
    except Exception as e:
        logger.error(f'Failed to generate secure token: {str(e)}')
        raise SecurityException(message='Failed to generate secure token', details={'error': str(e)}) from e
def _get_cipher() -> Fernet:
    try:
        base_key = settings.SECRET_KEY.encode()
        salt = b'security_service_salt'
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
        key = base64.urlsafe_b64encode(kdf.derive(base_key))
        return Fernet(key)
    except Exception as e:
        logger.error(f'Failed to setup encryption: {str(e)}')
        raise ConfigurationException(message='Failed to initialize encryption', details={'error': str(e)}) from e
class EncryptionManager:
    def __init__(self) -> None:
        self._setup_encryption()
    def _setup_encryption(self) -> None:
        try:
            base_key = settings.SECRET_KEY.encode()
            salt = b'security_service_salt'
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
            key = base64.urlsafe_b64encode(kdf.derive(base_key))
            self.cipher = Fernet(key)
        except Exception as e:
            logger.error(f'Failed to setup encryption: {str(e)}')
            raise ConfigurationException(message='Failed to initialize encryption service', details={'error': str(e)}) from e
    def encrypt_data(self, data: Union[str, bytes, dict]) -> str:
        return encrypt_data(data)
    def decrypt_data(self, encrypted_data: str) -> Union[str, dict]:
        return decrypt_data(encrypted_data)
    def generate_secure_token(self, length: int=32) -> str:
        return generate_secure_token(length)