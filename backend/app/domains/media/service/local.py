# backend/app/services/media/local.py
"""Local filesystem storage backend implementation.

This module provides a local filesystem implementation of the MediaStorageBackend
protocol, suitable for development and testing environments.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import BinaryIO, Dict, Optional, Set, Tuple, Union

import aiofiles
from app.domains.media.service.base import (
    FileNotFoundError,
    MediaStorageError,
)
from app.domains.media.service.thumbnails import ThumbnailGenerator
from fastapi import UploadFile

from app.core.config import settings
from app.core.logging import get_logger
from app.domains.media.models import MediaType

logger = get_logger(__name__)


@dataclass
class LocalMediaStorage:
    """Local filesystem storage backend for development."""

    ALLOWED_MIME_TYPES: Dict[MediaType, Set[str]] = field(
        default_factory=lambda: {
            MediaType.IMAGE: {
                "image/jpeg",
                "image/png",
                "image/gif",
                "image/webp",
                "image/svg+xml",
            },
            MediaType.DOCUMENT: {
                "application/pdf",
                "application/msword",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "application/vnd.ms-excel",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "text/plain",
                "text/csv",
            },
            MediaType.VIDEO: {
                "video/mp4",
                "video/quicktime",
                "video/x-msvideo",
                "video/x-ms-wmv",
            },
            MediaType.OTHER: {
                "application/zip",
                "application/x-zip-compressed",
                "application/octet-stream",
            },
        }
    )

    # Maximum file sizes by type (in bytes)
    MAX_FILE_SIZES: Dict[MediaType, int] = field(
        default_factory=lambda: {
            MediaType.IMAGE: 10 * 1024 * 1024,  # 10MB
            MediaType.DOCUMENT: 50 * 1024 * 1024,  # 50MB
            MediaType.VIDEO: 500 * 1024 * 1024,  # 500MB
            MediaType.OTHER: 100 * 1024 * 1024,  # 100MB
        }
    )

    # Thumbnail dimensions
    DEFAULT_THUMBNAIL_SIZE: Tuple[int, int] = (300, 300)

    media_root: Path = field(default_factory=lambda: Path(settings.MEDIA_ROOT))

    def __post_init__(self) -> None:
        """Ensure media directories exist."""
        # Base initialization - will run synchronously
        self.media_root.mkdir(parents=True, exist_ok=True)

        # Create subdirectories for each media type
        for media_type in MediaType:
            (self.media_root / media_type.value).mkdir(parents=True, exist_ok=True)

        # Create thumbnails directory
        (self.media_root / "thumbnails").mkdir(parents=True, exist_ok=True)

    async def initialize(self) -> None:
        """
        Initialize storage backend connection.

        For local storage, this is a no-op as directories are created in __post_init__.
        """
        pass  # Already initialized in __post_init__

    async def save_file(
        self,
        file: Union[UploadFile, BinaryIO, bytes],
        destination: str,
        media_type: MediaType,
        content_type: Optional[str] = None,
    ) -> str:
        """
        Save file to local storage asynchronously.

        Args:
            file: The file to upload (UploadFile, file-like object, or bytes)
            destination: Relative path where the file should be stored
            media_type: Type of media being stored
            content_type: Optional content type override

        Returns:
            str: URL to access the saved file

        Raises:
            MediaStorageError: If file saving fails
            ValueError: If invalid file type or format
        """
        # Validate media type
        if media_type not in MediaType:
            raise ValueError(f"Invalid media type: {media_type}")

        # Determine content type if not provided
        file_content_type = content_type
        if isinstance(file, UploadFile):
            file_content_type = file_content_type or file.content_type

        # Validate content type if we have it
        if file_content_type and media_type != MediaType.OTHER:
            # Check if the content type is allowed for this media type
            if file_content_type not in self.ALLOWED_MIME_TYPES.get(media_type, set()):
                allowed_types = ", ".join(
                    self.ALLOWED_MIME_TYPES.get(media_type, set())
                )
                raise ValueError(
                    f"Content type '{file_content_type}' not allowed for {media_type.value}. "
                    f"Allowed types: {allowed_types}"
                )

        # Create full path to file
        file_path = self.media_root / media_type.value / destination
        file_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Read and write file contents asynchronously
            if isinstance(file, UploadFile):
                content = await file.read()
                async with aiofiles.open(file_path, "wb") as f:
                    await f.write(content)
            elif isinstance(file, bytes):
                async with aiofiles.open(file_path, "wb") as f:
                    await f.write(file)
            else:
                # Handle file-like objects
                content = file.read()
                if not isinstance(content, bytes):
                    content = content.encode("utf-8")
                async with aiofiles.open(file_path, "wb") as f:
                    await f.write(content)

            # Log successful file save with structured logging
            logger.info(
                "file_saved",
                path=str(file_path),
                size=file_path.stat().st_size,
                content_type=file_content_type,
                media_type=media_type.value,
            )

            # Return public URL using the environment-aware media_base_url property
            return f"{settings.media_base_url}{media_type.value}/{destination}"

        except Exception as e:
            # Log error with structured logging
            logger.error(
                "file_save_failed", path=str(file_path), error=str(e), exc_info=True
            )
            raise MediaStorageError(f"Failed to save file: {str(e)}") from e

    async def get_file_url(self, file_path: str) -> str:
        """
        Get URL for local file.

        Args:
            file_path: Relative path to the file

        Returns:
            str: Public URL to access the file
        """
        # Make sure the path is relative to media root
        if file_path.startswith("/"):
            file_path = file_path[1:]

        # Return public URL using the environment-aware media_base_url property
        return f"{settings.media_base_url}{file_path}"

    async def delete_file(self, file_path: str) -> bool:
        """
        Delete file from local storage asynchronously.

        Args:
            file_path: Relative path to the file

        Returns:
            bool: True if file was successfully deleted, False otherwise

        Raises:
            FileNotFoundError: If the file doesn't exist
            MediaStorageError: If deletion fails
        """
        # Create full path to file
        if file_path.startswith("/"):
            file_path = file_path[1:]

        full_path = self.media_root / file_path

        # Check if file exists
        if not full_path.exists():
            logger.warning("file_not_found", path=str(full_path))
            raise FileNotFoundError(f"File not found: {full_path}")

        try:
            # Delete file
            full_path.unlink()
            logger.info("file_deleted", path=str(full_path))
            return True
        except Exception as e:
            logger.error(
                "file_delete_failed", path=str(full_path), error=str(e), exc_info=True
            )
            raise MediaStorageError(f"Failed to delete file: {str(e)}") from e

    async def file_exists(self, file_path: str) -> bool:
        """
        Check if a file exists in storage asynchronously.

        Args:
            file_path: Relative path to the file

        Returns:
            bool: True if file exists, False otherwise
        """
        # Create full path to file
        if file_path.startswith("/"):
            file_path = file_path[1:]

        full_path = self.media_root / file_path
        return full_path.exists()

    async def generate_thumbnail(
        self, file_path: str, width: int = 200, height: int = 200
    ) -> Optional[str]:
        """
        Generate a thumbnail for an image file asynchronously.

        Args:
            file_path: Relative path to the original image
            width: Desired thumbnail width
            height: Desired thumbnail height

        Returns:
            Optional[str]: Path to the thumbnail if successful, None otherwise

        Raises:
            MediaStorageError: If thumbnail generation fails
            FileNotFoundError: If the original file doesn't exist
        """
        # Normalize file path
        if file_path.startswith("/"):
            file_path = file_path[1:]

        # Skip thumbnail generation for non-image files or SVG files
        if not ThumbnailGenerator.can_generate_thumbnail(file_path):
            return None

        # Get paths
        original_path = self.media_root / file_path
        thumbnail_rel_path = ThumbnailGenerator.get_thumbnail_path(
            file_path, width, height
        )
        thumbnail_path = self.media_root / thumbnail_rel_path

        try:
            # Generate the thumbnail
            await ThumbnailGenerator.generate_thumbnail(
                original_path, thumbnail_path, width, height
            )
            return thumbnail_rel_path
        except Exception as e:
            logger.error(
                "thumbnail_generation_failed",
                original_path=file_path,
                width=width,
                height=height,
                error=str(e),
                exc_info=True,
            )
            if isinstance(e, FileNotFoundError):
                raise
            raise MediaStorageError(f"Thumbnail generation failed: {str(e)}") from e
