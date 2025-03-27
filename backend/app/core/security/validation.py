from __future__ import annotations

"""Input validation and sanitization functionality.

This module provides functions for validating and sanitizing user input,
detecting suspicious content, and generating security headers.
"""

import ipaddress
import json
import re
from typing import Any, Dict, Set, Tuple, Optional, Type
from enum import Enum

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger("app.core.security.validation")


def is_valid_hostname(hostname: str) -> bool:
    """Validate a hostname.

    Args:
        hostname: The hostname to validate.

    Returns:
        bool: True if the hostname is valid, False otherwise.
    """
    allowed_hosts: Set[str] = set(settings.security.ALLOWED_HOSTS)
    hostname_pattern = re.compile(r"^[a-zA-Z0-9.-]+$")

    if not hostname or len(hostname) > 255:
        return False

    if allowed_hosts and hostname not in allowed_hosts:
        return False

    return bool(hostname_pattern.match(hostname))


def is_trusted_ip(ip_address: str) -> bool:
    """Check if an IP address is in the trusted proxies list.

    Args:
        ip_address: The IP address to check.

    Returns:
        bool: True if the IP address is trusted, False otherwise.
    """
    trusted_proxies: Set[str] = set(settings.security.TRUSTED_PROXIES)

    try:
        ip = ipaddress.ip_address(ip_address)

        for trusted_ip in trusted_proxies:
            if "/" in trusted_ip:  # CIDR notation
                if ip in ipaddress.ip_network(trusted_ip):
                    return True
            elif ip == ipaddress.ip_address(trusted_ip):
                return True

        return False

    except ValueError:
        logger.warning(f"Invalid IP address format: {ip_address}")
        return False


def is_valid_enum_value(enum_class: Type[Enum], value: Any) -> bool:
    """Check if a value is a valid member of an Enum class.

    Args:
        enum_class: The Enum class to check against.
        value: The value to check.

    Returns:
        bool: True if the value is a valid enum member, False otherwise.
    """
    try:
        # Check if it's a direct enum member
        if isinstance(value, enum_class):
            return True

        # Check if it's a value that can be converted to an enum member
        if (
            hasattr(enum_class, "_value2member_map_")
            and value in enum_class._value2member_map_
        ):
            return True

        # Check if it's a name of an enum member
        if hasattr(enum_class, value):
            return True

        # Try to create the enum from the value
        enum_class(value)
        return True
    except (ValueError, TypeError, KeyError, AttributeError):
        return False


def sanitize_input(input_str: str) -> str:
    """Sanitize user input by escaping HTML characters.

    Args:
        input_str: The input string to sanitize.

    Returns:
        str: The sanitized string.
    """
    if not input_str:
        return ""

    sanitized = input_str
    sanitized = sanitized.replace("&", "&amp;")
    sanitized = sanitized.replace("<", "&lt;")
    sanitized = sanitized.replace(">", "&gt;")
    sanitized = sanitized.replace('"', "&quot;")
    sanitized = sanitized.replace("'", "&#x27;")
    sanitized = sanitized.replace("/", "&#x2F;")

    return sanitized


def validate_json_input(json_data: Any) -> bool:
    """Validate JSON input for suspicious content and structure.

    Args:
        json_data: The JSON data to validate.

    Returns:
        bool: True if the JSON is valid and safe, False otherwise.
    """
    try:
        if not isinstance(json_data, (dict, list)):
            return False

        json_str = json.dumps(json_data)

        if detect_suspicious_content(json_str):
            logger.warning("Suspicious content detected in JSON input")
            return False

        return True

    except Exception as e:
        logger.error(f"Error validating JSON input: {str(e)}")
        return False


def detect_suspicious_content(content: str) -> bool:
    """Detect potentially malicious content.

    Args:
        content: The content to check.

    Returns:
        bool: True if suspicious content is detected, False otherwise.
    """
    if not content:
        return False

    suspicious_patterns = [
        r"<script.*?>",
        r"javascript:",
        r"eval\(",
        r"document\.cookie",
        r"localStorage",
        r"sessionStorage",
        r"onload=",
        r"onerror=",
        r"onclick=",
        r"onmouseover=",
        r"DROP TABLE",
        r"--",
        r"UNION SELECT",
        r"1=1",
        r"../../",
        r"data:text/html",
        r"file://",
    ]

    suspicious_regex = re.compile("|".join(suspicious_patterns), re.IGNORECASE)
    return bool(suspicious_regex.search(content))


def moderate_content(
    content: str, content_type: str = "text"
) -> Tuple[bool, Optional[str]]:
    """Moderate content for inappropriate or harmful material.

    Args:
        content: The content to moderate.
        content_type: The type of content (text, image, etc.)

    Returns:
        Tuple[bool, Optional[str]]: A tuple containing a boolean indicating if the content
            is acceptable and an optional reason if it's not.
    """
    if not content:
        return True, None

    # Basic moderation rules - expand these based on your needs
    moderation_patterns = [
        # Offensive language patterns
        r"\b(obscenity|profanity|slur)\b",
        # Violence patterns
        r"\b(threat|kill|attack|bomb)\b",
        # Harmful instruction patterns
        r"how to (hack|steal|forge|break)",
    ]

    moderation_regex = re.compile("|".join(moderation_patterns), re.IGNORECASE)
    match = moderation_regex.search(content)

    if match:
        return (
            False,
            f"Content contains potentially inappropriate material: {match.group(0)}",
        )

    # You could add more sophisticated checks here or API calls to content moderation services

    return True, None


def get_security_headers() -> Dict[str, str]:
    """Get security headers for HTTP responses.

    Returns:
        Dict[str, str]: A dictionary of security headers.
    """
    return {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Content-Security-Policy": settings.security.CONTENT_SECURITY_POLICY,
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": settings.security.PERMISSIONS_POLICY,
    }


class ValidationManager:
    """Manager for input validation and sanitization."""

    def __init__(self) -> None:
        """Initialize the validation manager."""
        self.allowed_hosts: Set[str] = set(settings.security.ALLOWED_HOSTS)
        self.trusted_proxies: Set[str] = set(settings.security.TRUSTED_PROXIES)

        self.patterns = {
            "email": re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"),
            "url": re.compile(
                r"^(https?:\/\/)?(([a-z\d]([a-z\d-]*[a-z\d])*)\.)+"
                r"[a-z]{2,}|(((\d{1,3}\.){3}\d{1,3}))(:\d+)?"
                r"(\/[-a-z\d%_.~+]*)*(\\?[;&a-z\d%_.~+=-]*)?(#[-a-z\d_]*)?$",
                re.IGNORECASE,
            ),
            "hostname": re.compile(r"^[a-zA-Z0-9.-]+$"),
        }

        self.suspicious_patterns = [
            r"<script.*?>",
            r"javascript:",
            r"eval\(",
            r"document\.cookie",
            r"localStorage",
            r"sessionStorage",
            r"onload=",
            r"onerror=",
            r"onclick=",
            r"onmouseover=",
            r"DROP TABLE",
            r"--",
            r"UNION SELECT",
            r"1=1",
            r"../../",
            r"data:text/html",
            r"file://",
        ]

        self.suspicious_regex = re.compile(
            "|".join(self.suspicious_patterns), re.IGNORECASE
        )

    def is_valid_hostname(self, hostname: str) -> bool:
        """Validate a hostname.

        Args:
            hostname: The hostname to validate.

        Returns:
            bool: True if the hostname is valid, False otherwise.
        """
        return is_valid_hostname(hostname)

    def is_trusted_ip(self, ip_address: str) -> bool:
        """Check if an IP address is in the trusted proxies list.

        Args:
            ip_address: The IP address to check.

        Returns:
            bool: True if the IP address is trusted, False otherwise.
        """
        return is_trusted_ip(ip_address)

    def is_valid_enum_value(self, enum_class: Type[Enum], value: Any) -> bool:
        """Check if a value is a valid member of an Enum class.

        Args:
            enum_class: The Enum class to check against.
            value: The value to check.

        Returns:
            bool: True if the value is a valid enum member, False otherwise.
        """
        return is_valid_enum_value(enum_class, value)

    def sanitize_input(self, input_str: str) -> str:
        """Sanitize user input by escaping HTML characters.

        Args:
            input_str: The input string to sanitize.

        Returns:
            str: The sanitized string.
        """
        return sanitize_input(input_str)

    def detect_suspicious_content(self, content: str) -> bool:
        """Detect potentially malicious content.

        Args:
            content: The content to check.

        Returns:
            bool: True if suspicious content is detected, False otherwise.
        """
        return detect_suspicious_content(content)

    def validate_json_input(self, json_data: Any) -> bool:
        """Validate JSON input for suspicious content.

        Args:
            json_data: The JSON data to validate.

        Returns:
            bool: True if the JSON is valid and safe, False otherwise.
        """
        try:
            if not isinstance(json_data, (dict, list)):
                return False

            json_str = json.dumps(json_data)

            if self.detect_suspicious_content(json_str):
                logger.warning("Suspicious content detected in JSON input")
                return False

            return True

        except Exception as e:
            logger.error(f"Error validating JSON input: {str(e)}")
            return False

    def moderate_content(
        self, content: str, content_type: str = "text"
    ) -> Tuple[bool, Optional[str]]:
        """Moderate content for inappropriate or harmful material.

        Args:
            content: The content to moderate.
            content_type: The type of content (text, image, etc.)

        Returns:
            Tuple[bool, Optional[str]]: A tuple containing a boolean indicating if the content
                is acceptable and an optional reason if it's not.
        """
        return moderate_content(content, content_type)

    def get_security_headers(self) -> Dict[str, str]:
        """Get security headers for HTTP responses.

        Returns:
            Dict[str, str]: A dictionary of security headers.
        """
        return get_security_headers()
