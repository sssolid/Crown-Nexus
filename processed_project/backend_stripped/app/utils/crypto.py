from __future__ import annotations
import base64
import os
from typing import Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from app.core.config import settings
def _get_encryption_key() -> bytes:
    salt = settings.CHAT_ENCRYPTION_SALT.encode()
    if not salt:
        salt = b'crown_nexus_chat_salt'
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
    key = base64.urlsafe_b64encode(kdf.derive(settings.SECRET_KEY.encode()))
    return key
_fernet = Fernet(_get_encryption_key())
def encrypt_message(message: str) -> str:
    encrypted = _fernet.encrypt(message.encode())
    return encrypted.decode()
def decrypt_message(encrypted_message: str) -> str:
    decrypted = _fernet.decrypt(encrypted_message.encode())
    return decrypted.decode()
def generate_secure_token(length: int=32) -> str:
    return os.urandom(length).hex()