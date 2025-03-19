# backend/app/services/security/csrf.py
"""CSRF protection services.

This module provides services for protecting against Cross-Site Request Forgery (CSRF)
attacks by generating and validating CSRF tokens.
"""
from __future__ import annotations

import hmac
import time
from typing import Optional, Tuple

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class CsrfService:
    """Service for CSRF token management and validation."""

    def __init__(self) -> None:
        """Initialize the CSRF service."""
        self.secret_key = settings.SECRET_KEY
        self.token_expiry = (
            settings.security.CSRF_TOKEN_EXPIRY or 3600
        )  # 1 hour default

    def generate_token(self, session_id: str) -> str:
        """
        Generate a CSRF token for a session.

        Args:
            session_id: The session ID to associate with the token

        Returns:
            A CSRF token
        """
        timestamp = int(time.time())
        random_part = secrets.token_hex(8)
        message = f"{session_id}:{timestamp}:{random_part}"
        signature = hmac.new(
            self.secret_key.encode(), message.encode(), digestmod="sha256"
        ).hexdigest()

        return f"{message}:{signature}"

    def parse_token(self, token: str) -> Optional[Tuple[str, int, str, str]]:
        """
        Parse a CSRF token into its components.

        Args:
            token: The token to parse

        Returns:
            Tuple of (session_id, timestamp, random_part, signature) or None if invalid
        """
        try:
            parts = token.split(":")
            if len(parts) != 4:
                logger.warning(f"Invalid CSRF token format")
                return None

            session_id, timestamp_str, random_part, signature = parts
            timestamp = int(timestamp_str)

            return session_id, timestamp, random_part, signature
        except Exception as e:
            logger.warning(f"CSRF token parsing error: {str(e)}")
            return None

    def validate_token(self, token: str, session_id: str) -> bool:
        """
        Validate a CSRF token.

        Args:
            token: The token to validate
            session_id: The session ID to validate against

        Returns:
            True if the token is valid, False otherwise
        """
        # Parse the token
        parsed = self.parse_token(token)
        if not parsed:
            return False

        token_session_id, timestamp, random_part, provided_signature = parsed

        # Check session ID
        if token_session_id != session_id:
            logger.warning(f"CSRF token session mismatch")
            return False

        # Check if token has expired
        current_time = int(time.time())
        if current_time - timestamp > self.token_expiry:
            logger.warning(f"CSRF token expired")
            return False

        # Verify signature
        message = f"{token_session_id}:{timestamp}:{random_part}"
        expected_signature = hmac.new(
            self.secret_key.encode(), message.encode(), digestmod="sha256"
        ).hexdigest()

        if not hmac.compare_digest(provided_signature, expected_signature):
            logger.warning(f"CSRF token signature mismatch")
            return False

        return True


import secrets
