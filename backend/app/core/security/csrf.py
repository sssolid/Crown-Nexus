from __future__ import annotations

"""CSRF protection functionality.

This module provides functions for generating and validating CSRF tokens
to protect against cross-site request forgery attacks.
"""

import hmac
import secrets
import time
from typing import Optional, Tuple

from app.core.config import settings
from app.logging import get_logger

logger = get_logger("app.core.security.csrf")


def generate_csrf_token(session_id: str) -> str:
    """Generate a CSRF token.

    Args:
        session_id: The session ID to bind the token to.

    Returns:
        str: The generated CSRF token.
    """
    timestamp = int(time.time())
    random_part = secrets.token_hex(8)
    message = f"{session_id}:{timestamp}:{random_part}"

    signature = hmac.new(
        settings.SECRET_KEY.encode(), message.encode(), digestmod="sha256"
    ).hexdigest()

    return f"{message}:{signature}"


def validate_csrf_token(token: str, session_id: str) -> bool:
    """Validate a CSRF token.

    Args:
        token: The token to validate.
        session_id: The session ID to validate against.

    Returns:
        bool: True if the token is valid, False otherwise.
    """
    try:
        parts = token.split(":")
        if len(parts) != 4:
            logger.warning("Invalid CSRF token format")
            return False

        token_session_id, timestamp_str, random_part, provided_signature = parts

        if token_session_id != session_id:
            logger.warning("CSRF token session mismatch")
            return False

        timestamp = int(timestamp_str)
        current_time = int(time.time())
        token_expiry = settings.security.CSRF_TOKEN_EXPIRY or 3600

        if current_time - timestamp > token_expiry:
            logger.warning("CSRF token expired")
            return False

        message = f"{token_session_id}:{timestamp}:{random_part}"
        expected_signature = hmac.new(
            settings.SECRET_KEY.encode(), message.encode(), digestmod="sha256"
        ).hexdigest()

        if not hmac.compare_digest(provided_signature, expected_signature):
            logger.warning("CSRF token signature mismatch")
            return False

        return True

    except Exception as e:
        logger.warning(f"CSRF token validation error: {str(e)}")
        return False


class CsrfManager:
    """Manager for CSRF token-related functionality."""

    def __init__(self) -> None:
        """Initialize the CSRF manager."""
        self.secret_key = settings.SECRET_KEY
        self.token_expiry = settings.security.CSRF_TOKEN_EXPIRY or 3600

    def generate_token(self, session_id: str) -> str:
        """Generate a CSRF token.

        Args:
            session_id: The session ID to bind the token to.

        Returns:
            str: The generated CSRF token.
        """
        return generate_csrf_token(session_id)

    def parse_token(self, token: str) -> Optional[Tuple[str, int, str, str]]:
        """Parse a CSRF token.

        Args:
            token: The token to parse.

        Returns:
            Optional[Tuple[str, int, str, str]]: A tuple containing the parsed token parts,
                or None if parsing fails.
        """
        try:
            parts = token.split(":")
            if len(parts) != 4:
                logger.warning("Invalid CSRF token format")
                return None

            session_id, timestamp_str, random_part, signature = parts
            timestamp = int(timestamp_str)

            return (session_id, timestamp, random_part, signature)

        except Exception as e:
            logger.warning(f"CSRF token parsing error: {str(e)}")
            return None

    def validate_token(self, token: str, session_id: str) -> bool:
        """Validate a CSRF token.

        Args:
            token: The token to validate.
            session_id: The session ID to validate against.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        return validate_csrf_token(token, session_id)
