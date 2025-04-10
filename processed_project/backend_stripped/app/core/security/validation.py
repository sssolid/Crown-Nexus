from __future__ import annotations
'Input validation and sanitization functionality.\n\nThis module provides functions for validating and sanitizing user input,\ndetecting suspicious content, and generating security headers.\n'
import ipaddress
import json
import re
from typing import Any, Dict, Set, Tuple, Optional, Type
from enum import Enum
from app.core.config import settings
from app.logging import get_logger
logger = get_logger('app.core.security.validation')
def is_valid_hostname(hostname: str) -> bool:
    allowed_hosts: Set[str] = set(settings.security.ALLOWED_HOSTS)
    hostname_pattern = re.compile('^[a-zA-Z0-9.-]+$')
    if not hostname or len(hostname) > 255:
        return False
    if allowed_hosts and hostname not in allowed_hosts:
        return False
    return bool(hostname_pattern.match(hostname))
def is_trusted_ip(ip_address: str) -> bool:
    trusted_proxies: Set[str] = set(settings.security.TRUSTED_PROXIES)
    try:
        ip = ipaddress.ip_address(ip_address)
        for trusted_ip in trusted_proxies:
            if '/' in trusted_ip:
                if ip in ipaddress.ip_network(trusted_ip):
                    return True
            elif ip == ipaddress.ip_address(trusted_ip):
                return True
        return False
    except ValueError:
        logger.warning(f'Invalid IP address format: {ip_address}')
        return False
def is_valid_enum_value(enum_class: Type[Enum], value: Any) -> bool:
    try:
        if isinstance(value, enum_class):
            return True
        if hasattr(enum_class, '_value2member_map_') and value in enum_class._value2member_map_:
            return True
        if hasattr(enum_class, value):
            return True
        enum_class(value)
        return True
    except (ValueError, TypeError, KeyError, AttributeError):
        return False
def sanitize_input(input_str: str) -> str:
    if not input_str:
        return ''
    sanitized = input_str
    sanitized = sanitized.replace('&', '&amp;')
    sanitized = sanitized.replace('<', '&lt;')
    sanitized = sanitized.replace('>', '&gt;')
    sanitized = sanitized.replace('"', '&quot;')
    sanitized = sanitized.replace("'", '&#x27;')
    sanitized = sanitized.replace('/', '&#x2F;')
    return sanitized
def validate_json_input(json_data: Any) -> bool:
    try:
        if not isinstance(json_data, (dict, list)):
            return False
        json_str = json.dumps(json_data)
        if detect_suspicious_content(json_str):
            logger.warning('Suspicious content detected in JSON input')
            return False
        return True
    except Exception as e:
        logger.error(f'Error validating JSON input: {str(e)}')
        return False
def detect_suspicious_content(content: str) -> bool:
    if not content:
        return False
    suspicious_patterns = ['<script.*?>', 'javascript:', 'eval\\(', 'document\\.cookie', 'localStorage', 'sessionStorage', 'onload=', 'onerror=', 'onclick=', 'onmouseover=', 'DROP TABLE', '--', 'UNION SELECT', '1=1', '../../', 'data:text/html', 'file://']
    suspicious_regex = re.compile('|'.join(suspicious_patterns), re.IGNORECASE)
    return bool(suspicious_regex.search(content))
def moderate_content(content: str, content_type: str='text') -> Tuple[bool, Optional[str]]:
    if not content:
        return (True, None)
    moderation_patterns = ['\\b(obscenity|profanity|slur)\\b', '\\b(threat|kill|attack|bomb)\\b', 'how to (hack|steal|forge|break)']
    moderation_regex = re.compile('|'.join(moderation_patterns), re.IGNORECASE)
    match = moderation_regex.search(content)
    if match:
        return (False, f'Content contains potentially inappropriate material: {match.group(0)}')
    return (True, None)
def get_security_headers() -> Dict[str, str]:
    return {'X-Content-Type-Options': 'nosniff', 'X-Frame-Options': 'DENY', 'X-XSS-Protection': '1; mode=block', 'Content-Security-Policy': settings.security.CONTENT_SECURITY_POLICY, 'Strict-Transport-Security': 'max-age=31536000; includeSubDomains', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Permissions-Policy': settings.security.PERMISSIONS_POLICY}
class ValidationManager:
    def __init__(self) -> None:
        self.allowed_hosts: Set[str] = set(settings.security.ALLOWED_HOSTS)
        self.trusted_proxies: Set[str] = set(settings.security.TRUSTED_PROXIES)
        self.patterns = {'email': re.compile('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'), 'url': re.compile('^(https?:\\/\\/)?(([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|(((\\d{1,3}\\.){3}\\d{1,3}))(:\\d+)?(\\/[-a-z\\d%_.~+]*)*(\\\\?[;&a-z\\d%_.~+=-]*)?(#[-a-z\\d_]*)?$', re.IGNORECASE), 'hostname': re.compile('^[a-zA-Z0-9.-]+$')}
        self.suspicious_patterns = ['<script.*?>', 'javascript:', 'eval\\(', 'document\\.cookie', 'localStorage', 'sessionStorage', 'onload=', 'onerror=', 'onclick=', 'onmouseover=', 'DROP TABLE', '--', 'UNION SELECT', '1=1', '../../', 'data:text/html', 'file://']
        self.suspicious_regex = re.compile('|'.join(self.suspicious_patterns), re.IGNORECASE)
    def is_valid_hostname(self, hostname: str) -> bool:
        return is_valid_hostname(hostname)
    def is_trusted_ip(self, ip_address: str) -> bool:
        return is_trusted_ip(ip_address)
    def is_valid_enum_value(self, enum_class: Type[Enum], value: Any) -> bool:
        return is_valid_enum_value(enum_class, value)
    def sanitize_input(self, input_str: str) -> str:
        return sanitize_input(input_str)
    def detect_suspicious_content(self, content: str) -> bool:
        return detect_suspicious_content(content)
    def validate_json_input(self, json_data: Any) -> bool:
        try:
            if not isinstance(json_data, (dict, list)):
                return False
            json_str = json.dumps(json_data)
            if self.detect_suspicious_content(json_str):
                logger.warning('Suspicious content detected in JSON input')
                return False
            return True
        except Exception as e:
            logger.error(f'Error validating JSON input: {str(e)}')
            return False
    def moderate_content(self, content: str, content_type: str='text') -> Tuple[bool, Optional[str]]:
        return moderate_content(content, content_type)
    def get_security_headers(self) -> Dict[str, str]:
        return get_security_headers()