# backend/app/services/media/base.py
"""Base interfaces and types for the media storage system.

This module defines the common interfaces, protocols, and type definitions
used throughout the media service, ensuring consistent interaction between
different storage backends and the main service.
"""
from __future__ import annotations

import abc
from enum import Enum
from pathlib import Path
from typing import (
    Any, BinaryIO, Dict, Optional, Protocol, Set, Tuple, TypedDict, Union
)

from fastapi import UploadFile


class StorageBackendType(str, Enum):
    """Enumeration of supported storage backend types."""
    LOCAL = "local"
    S3 = "s3"
    AZURE = "azure"  # Future implementation


class FileMetadata(TypedDict, total=False):
    """File metadata type definition."""
    width: Optional[int]
    height: Optional[int]
    content_type: str
    file_size: int
    original_filename: str
    created_at: str


class MediaStorageError(Exception):
    """Base exception for media storage errors."""
    pass


class FileNotFoundError(MediaStorageError):
    """Exception raised when a file is not found."""
    pass


class StorageConnectionError(MediaStorageError):
    """Exception raised when connection to storage fails."""
    pass


class MediaStorageBackend(Protocol):
    """Protocol defining media storage backend interface."""

    async def initialize(self) -> None:
        """Initialize storage backend connection."""
        ...

    async def save_file(
        self,
        file: Union[UploadFile, BinaryIO, bytes],
        destination: str,
        media_type: str,
        content_type: Optional[str] = None,
    ) -> str:
        """
        Save a file to storage and return its public URL.

        Args:
            file: The file to upload (UploadFile, file-like object, or bytes)
            destination: Relative path where the file should be stored
            media_type: Type of media being stored
            content_type: Optional content type override

        Returns:
            str: Public URL to access the file

        Raises:
            MediaStorageError: If saving fails
        """
        ...

    async def get_file_url(self, file_path: str) -> str:
        """
        Get the URL for accessing a file.

        Args:
            file_path: Relative path to the file

        Returns:
            str: Public URL to access the file
        """
        ...

    async def delete_file(self, file_path: str) -> bool:
        """
        Delete a file from storage.

        Args:
            file_path: Relative path to the file

        Returns:
            bool: True if file was successfully deleted, False otherwise

        Raises:
            MediaStorageError: If deletion fails
        """
        ...

    async def file_exists(self, file_path: str) -> bool:
        """
        Check if a file exists in storage.

        Args:
            file_path: Relative path to the file

        Returns:
            bool: True if file exists, False otherwise
        """
        ...

    async def generate_thumbnail(
        self,
        file_path: str,
        width: int = 200,
        height: int = 200
    ) -> Optional[str]:
        """
        Generate a thumbnail for an image file.

        Args:
            file_path: Relative path to the original image
            width: Desired thumbnail width
            height: Desired thumbnail height

        Returns:
            Optional[str]: Path to the thumbnail if successful, None otherwise

        Raises:
            MediaStorageError: If thumbnail generation fails
        """
        ...
