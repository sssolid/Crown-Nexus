from __future__ import annotations

"""Password handling functionality.

This module provides functions for password hashing, verification, and policy validation,
ensuring secure password management throughout the application.
"""

import re
from pathlib import Path
from typing import Optional, Set, Tuple

from passlib.context import CryptContext

from app.core.config import settings
from app.core.logging import get_logger
from app.core.security.models import PasswordPolicy

logger = get_logger("app.core.security.passwords")

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash.

    Args:
        plain_password: The plain text password.
        hashed_password: The hashed password to verify against.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt.

    Args:
        password: The password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


async def validate_password_policy(
    password: str, user_id: Optional[str] = None
) -> Tuple[bool, Optional[str]]:
    """Validate a password against the password policy.

    Args:
        password: The password to validate.
        user_id: Optional user ID for password history checks.

    Returns:
        Tuple[bool, Optional[str]]: A tuple containing a boolean indicating if the password
            is valid and an optional error message if it's not.
    """
    policy = PasswordPolicy()
    common_passwords = _load_common_passwords()

    if len(password) < policy.min_length:
        return (
            False,
            f"Password must be at least {policy.min_length} characters long",
        )

    if len(password) > policy.max_length:
        return (
            False,
            f"Password cannot be longer than {policy.max_length} characters",
        )

    if policy.require_uppercase and not any(c.isupper() for c in password):
        return (False, "Password must contain at least one uppercase letter")

    if policy.require_lowercase and not any(c.islower() for c in password):
        return (False, "Password must contain at least one lowercase letter")

    if policy.require_digit and not any(c.isdigit() for c in password):
        return (False, "Password must contain at least one digit")

    if policy.require_special_char and not any(not c.isalnum() for c in password):
        return (False, "Password must contain at least one special character")

    if policy.prevent_common_passwords and password.lower() in common_passwords:
        return (False, "Password is too common and easily guessed")

    if user_id and policy.password_history_count > 0:
        # Password history check would be implemented here
        pass

    return (True, None)


def _load_common_passwords() -> Set[str]:
    """Load common passwords from a file.

    Returns:
        Set[str]: A set of common passwords.
    """
    common_passwords: Set[str] = set()
    try:
        passwords_file = (
            Path(settings.BASE_DIR) / "app" / "data" / "common_passwords.txt"
        )
        if passwords_file.exists():
            with open(passwords_file, "r") as f:
                for line in f:
                    common_passwords.add(line.strip())
            logger.debug(f"Loaded {len(common_passwords)} common passwords")
        else:
            common_passwords = {
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
                f"Using default list of {len(common_passwords)} common passwords"
            )
    except Exception as e:
        logger.error(f"Error loading common passwords: {str(e)}")
        common_passwords = {
            "password",
            "123456",
            "123456789",
            "qwerty",
            "12345678",
        }
    return common_passwords


class PasswordManager:
    """Manager for password-related functionality."""

    def __init__(self) -> None:
        """Initialize the password manager."""
        self.policy = PasswordPolicy()
        self.common_passwords: Set[str] = set()
        self.password_regex = re.compile(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        )
        self._load_common_passwords_sync()

    def _load_common_passwords_sync(self) -> None:
        """Load common passwords from a file."""
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
        """Validate a password against the password policy.

        Args:
            password: The password to validate.
            user_id: Optional user ID for password history checks.

        Returns:
            Tuple[bool, Optional[str]]: A tuple containing a boolean indicating if the password
                is valid and an optional error message if it's not.
        """
        # Implementation same as the function above
        # Calling the global function to avoid duplication
        return await validate_password_policy(password, user_id)

    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt.

        Args:
            password: The password to hash.

        Returns:
            str: The hashed password.
        """
        return get_password_hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash.

        Args:
            plain_password: The plain text password.
            hashed_password: The hashed password to verify against.

        Returns:
            bool: True if the password matches the hash, False otherwise.
        """
        try:
            return verify_password(plain_password, hashed_password)
        except Exception as e:
            logger.error(f"Password verification error: {str(e)}")
            return False
