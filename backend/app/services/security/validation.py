# backend/app/services/security/validation.py
"""Security validation utilities.

This module provides services for validating user input, hosts, IP addresses,
and other security-critical data to prevent attacks.
"""
from __future__ import annotations

import ipaddress
import re
import json
from typing import Any, Dict, Optional, Set

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class ValidationService:
    """Service for security validation."""

    def __init__(self) -> None:
        """Initialize the validation service."""
        # Set of allowed hosts
        self.allowed_hosts: Set[str] = set(settings.security.ALLOWED_HOSTS)

        # Set of trusted proxies
        self.trusted_proxies: Set[str] = set(settings.security.TRUSTED_PROXIES)

        # Compile regular expressions for validation
        self.patterns = {
            "email": re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"),
            "url": re.compile(
                r"^(https?:\/\/)?(([a-z\d]([a-z\d-]*[a-z\d])*)\.)+[a-z]{2,}|"
                r"((\d{1,3}\.){3}\d{1,3})(:\d+)?(\/[-a-z\d%_.~+]*)*"
                r"(\?[;&a-z\d%_.~+=-]*)?(#[-a-z\d_]*)?$",
                re.IGNORECASE,
            ),
            "hostname": re.compile(r"^[a-zA-Z0-9.-]+$"),
        }

        # Patterns for detecting suspicious content
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
        """
        Check if a hostname is valid and allowed.

        Args:
            hostname: The hostname to check

        Returns:
            True if the hostname is valid, False otherwise
        """
        if not hostname or len(hostname) > 255:
            return False

        if self.allowed_hosts and hostname not in self.allowed_hosts:
            return False

        return bool(self.patterns["hostname"].match(hostname))

    def is_trusted_ip(self, ip_address: str) -> bool:
        """
        Check if an IP address is in the trusted list.

        Args:
            ip_address: The IP address to check

        Returns:
            True if the IP is trusted, False otherwise
        """
        try:
            ip = ipaddress.ip_address(ip_address)

            for trusted_ip in self.trusted_proxies:
                if "/" in trusted_ip:  # CIDR notation
                    if ip in ipaddress.ip_network(trusted_ip):
                        return True
                elif ip == ipaddress.ip_address(trusted_ip):
                    return True

            return False
        except ValueError:
            logger.warning(f"Invalid IP address format: {ip_address}")
            return False

    def sanitize_input(self, input_str: str) -> str:
        """
        Sanitize user input to prevent XSS attacks.

        Args:
            input_str: The input string to sanitize

        Returns:
            The sanitized string
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

    def detect_suspicious_content(self, content: str) -> bool:
        """
        Detect potentially malicious content in user input.

        Args:
            content: The content to check

        Returns:
            True if suspicious content is detected, False otherwise
        """
        if not content:
            return False

        return bool(self.suspicious_regex.search(content))

    def validate_json_input(self, json_data: Any) -> bool:
        """
        Validate JSON input for security issues.

        Args:
            json_data: The JSON data to validate

        Returns:
            True if the input is valid, False otherwise
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

    def get_security_headers(self) -> Dict[str, str]:
        """
        Get recommended security headers for HTTP responses.

        Returns:
            Dictionary of security headers
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
