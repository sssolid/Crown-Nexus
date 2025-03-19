# backend/app/services/media/service.py
"""Main media service implementation.

This module provides the primary MediaService that handles file uploading,
storage, and retrieval operations using configurable storage backends.
"""
from __future__ import annotations

import os
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from fastapi import HTTPException, UploadFile, status

from app.core.config import settings
from app.core.logging import get_logger
from app.models.media import MediaType, MediaVisibility
from app.services.interfaces import ServiceInterface
from app.services.media.base import (
    FileNotFoundError,
    MediaStorageBackend,
    MediaStorageError,
    StorageBackendType,
)
from app.services.media.factory import StorageBackendFactory

logger = get_logger(__name__)


class MediaService(ServiceInterface):
    """Service for handling media file operations with configurable storage backends."""

    def __init__(self, storage_type: Optional[str] = None):
        """
        Initialize the media service.

        Args:
            storage_type: Optional storage backend type.
                If None, uses the value from settings.
        """
        self.storage_type = (
            StorageBackendType(storage_type.lower())
            if storage_type
            else StorageBackendType(settings.MEDIA_STORAGE_TYPE.lower())
        )
        self.storage: Optional[MediaStorageBackend] = None
        self.initialized = False

    async def initialize(self) -> None:
        """
        Initialize the media service and storage backend.

        This must be called before using any other methods.

        Raises:
            MediaStorageError: If storage initialization fails
        """
        if self.initialized:
            return

        logger.info("media_service_initializing", storage_type=self.storage_type)

        # Create the appropriate storage backend
        self.storage = StorageBackendFactory.get_backend(self.storage_type.value)

        # Initialize storage
        await self.storage.initialize()
        self.initialized = True

        logger.info("media_service_initialized", storage_type=self.storage_type)

    async def ensure_initialized(self) -> None:
        """Ensure the service is initialized."""
        if not self.initialized or not self.storage:
            await self.initialize()

    async def upload_file(
        self,
        file: UploadFile,
        media_type: MediaType,
        product_id: Optional[str] = None,
        filename: Optional[str] = None,
        visibility: MediaVisibility = MediaVisibility.PRIVATE,
        generate_thumbnail: bool = True,
    ) -> Tuple[str, Dict[str, Any], Optional[str]]:
        """
        Upload a file to storage with improved error handling.

        Args:
            file: The uploaded file
            media_type: Type of media being uploaded
            product_id: Optional product ID to associate with the file
            filename: Optional filename override
            visibility: Visibility level for the file
            generate_thumbnail: Whether to generate a thumbnail for images

        Returns:
            Tuple[str, Dict[str, Any], Optional[str]]:
                Tuple of (file URL, metadata, thumbnail URL or None)

        Raises:
            HTTPException: If the file type is invalid or upload fails
        """
        await self.ensure_initialized()

        try:
            # Validate the file
            if not file.filename:
                raise ValueError("No filename provided")

            # Use provided filename or original
            safe_filename = self._sanitize_filename(filename or file.filename)

            # Generate a unique filename with timestamp and UUID
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            ext = Path(safe_filename).suffix
            unique_filename = f"{timestamp}_{uuid.uuid4().hex}{ext}"

            # Create destination path
            if product_id:
                destination = f"{product_id}/{unique_filename}"
            else:
                # Use current date for organizing files
                date_path = datetime.now().strftime("%Y/%m/%d")
                destination = f"{date_path}/{unique_filename}"

            # Get content type
            content_type = file.content_type or self._guess_content_type(safe_filename)

            # Collect metadata
            metadata: Dict[str, Any] = {
                "original_filename": safe_filename,
                "content_type": content_type,
                "visibility": visibility.value,
                "product_id": product_id,
                "uploaded_at": datetime.now().isoformat(),
            }

            # Save the file
            file_url = await self.storage.save_file(
                file, destination, media_type, content_type
            )

            # Generate thumbnail for images if requested
            thumbnail_url = None
            if (
                generate_thumbnail
                and media_type == MediaType.IMAGE
                and content_type
                in ["image/jpeg", "image/png", "image/gif", "image/webp"]
                and not content_type.endswith("svg+xml")  # Skip SVG thumbnails
            ):
                # Calculate path relative to media root
                rel_path = f"{media_type.value}/{destination}"
                thumbnail_path = await self.storage.generate_thumbnail(rel_path)
                if thumbnail_path:
                    thumbnail_url = await self.storage.get_file_url(thumbnail_path)

            return file_url, metadata, thumbnail_url

        except ValueError as e:
            # Handle validation errors
            logger.warning(
                "file_upload_validation_failed",
                filename=getattr(file, "filename", "unknown"),
                error=str(e),
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
            ) from e

        except MediaStorageError as e:
            # Handle storage errors
            logger.error(
                "file_upload_storage_failed",
                filename=getattr(file, "filename", "unknown"),
                error=str(e),
                exc_info=True,
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Storage error: {str(e)}",
            ) from e

        except Exception as e:
            # Handle unexpected errors
            logger.error(
                "file_upload_unexpected_error",
                filename=getattr(file, "filename", "unknown"),
                error=str(e),
                exc_info=True,
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}",
            ) from e

    async def delete_file(self, file_url: str) -> bool:
        """
        Delete a file from storage with improved error handling.

        Args:
            file_url: URL of the file to delete

        Returns:
            bool: True if file was successfully deleted

        Raises:
            HTTPException: If deletion fails
        """
        await self.ensure_initialized()

        try:
            # Extract relative path from URL
            media_url = settings.media_base_url
            if file_url.startswith(media_url):
                rel_path = file_url[len(media_url) :]
            else:
                # Try to extract path from any URL format
                from urllib.parse import urlparse

                parsed_url = urlparse(file_url)
                rel_path = parsed_url.path

                # Remove any leading media path
                if rel_path.startswith(settings.MEDIA_URL):
                    rel_path = rel_path[len(settings.MEDIA_URL) :]

                # Remove any leading slash
                if rel_path.startswith("/"):
                    rel_path = rel_path[1:]

            # Check if file exists
            if not await self.storage.file_exists(rel_path):
                logger.warning("file_not_found_for_deletion", path=rel_path)
                return False

            # Delete the file
            result = await self.storage.delete_file(rel_path)

            # Try to delete thumbnail if it exists
            try:
                # Check if this is an image that might have a thumbnail
                if any(
                    ext in rel_path.lower()
                    for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]
                ):
                    # Extract filename
                    filename = Path(rel_path).name

                    # Check for various thumbnail patterns
                    thumb_patterns = [
                        f"thumbnails/thumb_{filename}",
                        f"thumbnails/thumb_200x200_{filename}",
                        f"thumbnails/thumb_300x300_{filename}",
                    ]

                    for pattern in thumb_patterns:
                        if await self.storage.file_exists(pattern):
                            await self.storage.delete_file(pattern)
            except Exception as e:
                # Log but don't fail if thumbnail deletion fails
                logger.warning(
                    "thumbnail_deletion_failed", original_path=rel_path, error=str(e)
                )

            return result

        except FileNotFoundError:
            # Not necessarily an error, just log and return False
            return False

        except MediaStorageError as e:
            # Handle storage errors
            logger.error(
                "file_deletion_storage_failed",
                url=file_url,
                error=str(e),
                exc_info=True,
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Storage error: {str(e)}",
            ) from e

        except Exception as e:
            # Handle unexpected errors
            logger.error(
                "file_deletion_unexpected_error",
                url=file_url,
                error=str(e),
                exc_info=True,
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}",
            ) from e

    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitize a filename to be safe for storage.

        Args:
            filename: Original filename

        Returns:
            str: Sanitized filename
        """
        # Replace potentially problematic characters
        safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_."

        # Extract extension
        name, ext = os.path.splitext(filename)

        # Sanitize the name part
        safe_name = "".join(c for c in name if c in safe_chars)

        # If the name becomes empty, use a default
        if not safe_name:
            safe_name = "file"

        # Sanitize extension and convert to lowercase
        safe_ext = ext.lower() if ext and all(c in safe_chars for c in ext) else ext

        # Return the sanitized name with the sanitized extension
        return safe_name + safe_ext

    def _guess_content_type(self, filename: str) -> str:
        """
        Guess the content type from filename extension.

        Args:
            filename: Filename to analyze

        Returns:
            str: Guessed content type
        """
        import mimetypes

        # Ensure mimetypes is initialized
        mimetypes.init()

        # Guess content type
        content_type, _ = mimetypes.guess_type(filename)

        # Default to binary if we can't determine
        return content_type or "application/octet-stream"

    async def shutdown(self) -> None:
        """Release resources during service shutdown."""
        logger.info("Shutting down media service")
        # Currently no specific shutdown tasks needed
