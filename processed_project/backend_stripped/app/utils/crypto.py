from __future__ import annotations
import base64
import os
from typing import Optional
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from app.core.config import settings
from app.core.exceptions import ConfigurationException, SecurityException, ErrorCode
from app.logging import get_logger
logger = get_logger('app.utils.crypto')
class CryptoError(SecurityException):
    def __init__(self, message: str, code: ErrorCode=ErrorCode.SECURITY_ERROR, details: Optional[dict]=None, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details or {}, status_code=500, original_exception=original_exception)
def _get_encryption_key() -> bytes:
    try:
        salt = settings.CHAT_ENCRYPTION_SALT.encode()
        if not salt:
            logger.warning('Encryption salt not configured, using default')
            salt = b'crown_nexus_chat_salt'
        if not settings.SECRET_KEY:
            error_msg = 'SECRET_KEY not configured'
            logger.error(error_msg)
            raise ConfigurationException(message=error_msg, code=ErrorCode.CONFIGURATION_ERROR, details={'missing_setting': 'SECRET_KEY'})
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
        key = base64.urlsafe_b64encode(kdf.derive(settings.SECRET_KEY.encode()))
        logger.debug('Encryption key derived successfully')
        return key
    except Exception as e:
        logger.error(f'Failed to derive encryption key: {str(e)}', exc_info=True)
        raise CryptoError(message='Failed to derive encryption key', original_exception=e) from e
try:
    _fernet = Fernet(_get_encryption_key())
    logger.info('Fernet encryption initialized successfully')
except Exception as e:
    logger.critical('Failed to initialize Fernet encryption', exc_info=True)
    raise CryptoError(message='Failed to initialize encryption system', original_exception=e) from e
def encrypt_message(message: str) -> str:
    if not message:
        logger.warning('Attempted to encrypt empty message')
        return ''
    try:
        encrypted = _fernet.encrypt(message.encode())
        return encrypted.decode()
    except Exception as e:
        logger.error(f'Encryption failed: {str(e)}', exc_info=True)
        raise CryptoError(message='Failed to encrypt message', original_exception=e) from e
def decrypt_message(encrypted_message: str) -> str:
    if not encrypted_message:
        logger.warning('Attempted to decrypt empty message')
        return ''
    try:
        decrypted = _fernet.decrypt(encrypted_message.encode())
        return decrypted.decode()
    except InvalidToken as e:
        logger.error('Invalid token for decryption', exc_info=True)
        raise CryptoError(message='Invalid encryption token', code=ErrorCode.SECURITY_ERROR, details={'error_type': 'invalid_token'}, original_exception=e) from e
    except Exception as e:
        logger.error(f'Decryption failed: {str(e)}', exc_info=True)
        raise CryptoError(message='Failed to decrypt message', original_exception=e) from e
def generate_secure_token(length: int=32) -> str:
    if length < 16:
        error_msg = 'Token length must be at least 16 bytes for security'
        logger.warning(error_msg, length=length)
        raise ValueError(error_msg)
    try:
        token = os.urandom(length).hex()
        logger.debug(f'Generated secure token of length {len(token)}')
        return token
    except Exception as e:
        logger.error(f'Failed to generate secure token: {str(e)}', exc_info=True)
        raise CryptoError(message='Failed to generate secure token', original_exception=e) from e