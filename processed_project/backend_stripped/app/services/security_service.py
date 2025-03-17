from __future__ import annotations
import hmac
import ipaddress
import re
from typing import Any, Dict, List, Optional, Pattern, Set, Tuple, Union
import secrets
import time
from app.core.config import settings
from app.core.logging import get_logger
from app.services.interfaces import ServiceInterface
logger = get_logger('app.services.security')
class SecurityService:
    def __init__(self, error_handling_service: Optional[ErrorHandlingService]=None) -> None:
        self.secret_key: str = settings.security.SECRET_KEY
        self.allowed_hosts: Set[str] = set(settings.security.ALLOWED_HOSTS)
        self.trusted_ips: Set[str] = set(settings.security.TRUSTED_PROXIES)
        self.csrf_token_expiry: int = settings.security.CSRF_TOKEN_EXPIRY
        self.error_handling_service = error_handling_service
        self.email_pattern: Pattern[str] = re.compile('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$')
        self.username_pattern: Pattern[str] = re.compile('^[a-zA-Z0-9_-]{3,32}$')
        logger.info('SecurityService initialized')
    async def initialize(self) -> None:
        pass
    async def shutdown(self) -> None:
        pass
    def generate_csrf_token(self, session_id: str) -> str:
        timestamp: int = int(time.time())
        random_part: str = secrets.token_hex(16)
        message: str = f'{session_id}:{timestamp}:{random_part}'
        signature: str = hmac.new(self.secret_key.encode(), message.encode(), digestmod='sha256').hexdigest()
        return f'{message}:{signature}'
    def validate_csrf_token(self, token: str, session_id: str) -> bool:
        try:
            parts: List[str] = token.split(':')
            if len(parts) != 4:
                return False
            message: str = ':'.join(parts[:3])
            provided_signature: str = parts[3]
            received_session_id, timestamp_str, random_part = parts[:3]
            if received_session_id != session_id:
                return False
            expected_signature: str = hmac.new(self.secret_key.encode(), message.encode(), digestmod='sha256').hexdigest()
            if not hmac.compare_digest(provided_signature, expected_signature):
                return False
            timestamp: int = int(timestamp_str)
            if int(time.time()) - timestamp > self.csrf_token_expiry:
                return False
            return True
        except Exception as e:
            logger.warning(f'CSRF token validation failed: {str(e)}')
            return False
    def is_valid_hostname(self, hostname: str) -> bool:
        if not hostname or len(hostname) > 255:
            return False
        if self.allowed_hosts and hostname not in self.allowed_hosts:
            return False
        allowed_chars: Pattern[str] = re.compile('^[a-zA-Z0-9.-]+$')
        if not allowed_chars.match(hostname):
            return False
        return True
    def is_trusted_ip(self, ip_address: str) -> bool:
        try:
            ip = ipaddress.ip_address(ip_address)
            for trusted_ip in self.trusted_ips:
                if '/' in trusted_ip:
                    if ip in ipaddress.ip_network(trusted_ip):
                        return True
                elif ip == ipaddress.ip_address(trusted_ip):
                    return True
            return False
        except ValueError:
            return False
    def sanitize_input(self, input_str: str) -> str:
        if not input_str:
            return ''
        sanitized: str = input_str
        sanitized = sanitized.replace('&', '&amp;')
        sanitized = sanitized.replace('<', '&lt;')
        sanitized = sanitized.replace('>', '&gt;')
        sanitized = sanitized.replace('"', '&quot;')
        sanitized = sanitized.replace("'", '&#x27;')
        sanitized = sanitized.replace('/', '&#x2F;')
        return sanitized
    def is_valid_email(self, email: str) -> bool:
        if not email or len(email) > 255:
            return False
        return bool(self.email_pattern.match(email))
    def is_valid_username(self, username: str) -> bool:
        if not username:
            return False
        return bool(self.username_pattern.match(username))
    def generate_secure_token(self, length: int=32) -> str:
        return secrets.token_hex(length)