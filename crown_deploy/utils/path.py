"""Path utilities for the Crown Nexus deployment system."""
from __future__ import annotations

import os
import re
import logging
from pathlib import Path
from typing import Union, Optional

import structlog

logger = structlog.get_logger()


def normalize_path(path: str) -> str:
    """
    Normalize a file path for the current operating system.

    This is especially useful for handling Windows paths in Git Bash format (/c/Users/...).

    Args:
        path: The path to normalize

    Returns:
        A normalized path suitable for the current OS
    """
    # Expand user directory shorthand
    path = os.path.expanduser(path)

    # Handle Git Bash style paths on Windows
    if os.name == 'nt':  # Windows
        git_bash_pattern = r'^/([a-zA-Z])/'
        match = re.match(git_bash_pattern, path)
        if match:
            drive_letter = match.group(1)
            path = path.replace(f'/{drive_letter}/', f'{drive_letter}:/')
            logger.debug("Normalized Windows Git Bash path",
                         original_path=f'/{drive_letter}/',
                         normalized_path=f'{drive_letter}:/')

    # Normalize separators for current OS
    normalized_path = os.path.normpath(path)

    # Log if path was changed
    if normalized_path != path:
        logger.debug("Path normalized", original=path, normalized=normalized_path)

    return normalized_path


def validate_key_path(path: str) -> Optional[str]:
    """
    Validate that an SSH key path exists and is accessible.

    Args:
        path: Path to the SSH key file

    Returns:
        Normalized path if valid, None if invalid
    """
    normalized_path = normalize_path(path)
    key_path = Path(normalized_path)

    if not key_path.exists():
        logger.warning("SSH key file not found", path=normalized_path)
        return None

    if not os.access(key_path, os.R_OK):
        logger.warning("SSH key file not readable", path=normalized_path)
        return None

    return normalized_path


def get_ssh_key_path(path: str) -> str:
    """
    Get a valid SSH key path, with appropriate error handling.

    Args:
        path: Path to the SSH key file

    Returns:
        Normalized path to the SSH key

    Raises:
        FileNotFoundError: If the key file doesn't exist
        PermissionError: If the key file isn't readable
    """
    normalized_path = normalize_path(path)
    key_path = Path(normalized_path)

    if not key_path.exists():
        raise FileNotFoundError(f"SSH key not found: {normalized_path}")

    if not os.access(key_path, os.R_OK):
        raise PermissionError(f"SSH key not readable: {normalized_path}")

    return normalized_path
