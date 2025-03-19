# backend/app/services/security/passwords.py
"""Password handling and policy enforcement.

This module provides services for password hashing, validation, and policy enforcement,
ensuring secure password handling throughout the application.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Optional, Set, Tuple

import bcrypt

from app.core.config import settings
from app.core.logging import get_logger
from app.core.security import get_password_hash, verify_password
from app.services.security.base import PasswordPolicy

logger = get_logger(__name__)


class PasswordService:
    """Service for password management and policy enforcement."""

    def __init__(self) -> None:
        """Initialize the password service."""
        self.policy = PasswordPolicy()
        self.common_passwords: Set[str] = set()

        # Regular expression for password strength validation
        self.password_regex = re.compile(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        )

        # Load common passwords
        self._load_common_passwords_sync()

    def _load_common_passwords_sync(self) -> None:
        """Load list of common passwords from file."""
        try:
            passwords_file = (
                Path(settings.BASE_DIR) / "app" / "data" / "common_passwords.txt"
            )
            if passwords_file.exists():
                with open(passwords_file, "r") as f:
                    for line in f:
                        self.common_passwords.add(line.strip())
                logger.debug(f"Loaded {len(self.common_passwords)} common passwords")
            else:
                # Fallback to a small set of common passwords
                self.common_passwords = {
                    "password",
                    "123456",
                    "123456789",
                    "qwerty",
                    "12345678",
                    "111111",
                    "1234567890",
                    "1234567",
                    "password1",
                    "12345",
                    "123123",
                    "000000",
                    "iloveyou",
                    "1234",
                    "1q2w3e4r",
                    "admin",
                }
                logger.debug(
                    f"Using default list of {len(self.common_passwords)} common passwords"
                )
        except Exception as e:
            logger.error(f"Error loading common passwords: {str(e)}")
            # Fallback to a minimal set
            self.common_passwords = {
                "password",
                "123456",
                "123456789",
                "qwerty",
                "12345678",
            }

    async def validate_password_policy(
        self, password: str, user_id: Optional[str] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate a password against the password policy.

        Args:
            password: The password to validate
            user_id: Optional user ID for checking password history

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check length requirements
        if len(password) < self.policy.min_length:
            return (
                False,
                f"Password must be at least {self.policy.min_length} characters long",
            )

        if len(password) > self.policy.max_length:
            return (
                False,
                f"Password cannot be longer than {self.policy.max_length} characters",
            )

        # Check character requirements
        if self.policy.require_uppercase and not any(c.isupper() for c in password):
            return (False, "Password must contain at least one uppercase letter")

        if self.policy.require_lowercase and not any(c.islower() for c in password):
            return (False, "Password must contain at least one lowercase letter")

        if self.policy.require_digit and not any(c.isdigit() for c in password):
            return (False, "Password must contain at least one digit")

        if self.policy.require_special_char and not any(
            not c.isalnum() for c in password
        ):
            return (False, "Password must contain at least one special character")

        # Check against common passwords
        if (
            self.policy.prevent_common_passwords
            and password.lower() in self.common_passwords
        ):
            return (False, "Password is too common and easily guessed")

        # Check password history
        if user_id and self.policy.password_history_count > 0:
            # This would normally check against a database of password history
            # Implementation depends on your storage mechanism
            pass

        return (True, None)

    def hash_password(self, password: str) -> str:
        """
        Hash a password using a cryptographically secure algorithm.

        This method uses bcrypt with a work factor for security.

        Args:
            password: The password to hash

        Returns:
            The hashed password
        """
        # Use bcrypt with a secure work factor
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against a hash with additional security measures.

        Args:
            plain_password: The plain text password
            hashed_password: The hashed password to compare against

        Returns:
            True if the password matches the hash, False otherwise
        """
        try:
            return verify_password(plain_password, hashed_password)
        except Exception as e:
            logger.error(f"Password verification error: {str(e)}")
            return False
