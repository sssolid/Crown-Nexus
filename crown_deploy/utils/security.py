"""Security utilities for the Crown Nexus deployment system."""
from __future__ import annotations

import secrets
import string
from typing import Dict


def generate_secure_password(length: int = 16) -> str:
    """Generate a secure random password."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_deployment_credentials() -> Dict[str, str]:
    """Generate all necessary secure credentials for a deployment."""
    return {
        "db_password": generate_secure_password(24),
        "admin_password": generate_secure_password(12),
        "redis_password": generate_secure_password(24),
        "secret_key": generate_secure_password(32)
    }


def mask_sensitive_value(value: str) -> str:
    """Mask a sensitive value for display/logging."""
    if not value:
        return ""

    if len(value) <= 4:
        return "*" * len(value)

    # Show first 2 and last 2 characters, mask the rest
    return value[:2] + "*" * (len(value) - 4) + value[-2:]
