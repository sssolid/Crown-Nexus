# backend/app/services/media_service.py
"""
Media service for file storage and retrieval.

This module provides a media service with a consistent API for storing, retrieving,
and managing media files. It supports different storage backends (local filesystem,
S3, etc.) through environment configuration, allowing for a seamless transition
from development to production environments.
"""

from __future__ import annotations

import asyncio
import logging
import os
import uuid
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import AsyncGenerator, BinaryIO, List, Optional, Protocol, Set, Tuple

from fastapi import HTTPException, UploadFile
from pydantic import BaseModel, Field, ValidationError

from app.core.config import Environment, settings

logger = logging.getLogger(__name__)


class MediaType(str, Enum):
    """Enumeration of supported media types."""

    IMAGE = "image"
    DOCUMENT = "document"
    VIDEO = "video"
    OTHER = "other"


class MediaStorageBackend(Protocol):
    """Protocol defining media storage backend interface."""

    async def save_file(
        self, file: UploadFile, destination: str, media_type: MediaType
    ) -> str:
        """
        Save a file to storage and return its public URL.

        Args:
            file: The uploaded file
            destination: Relative path where the file should be stored
            media_type: Type of media being stored

        Returns:
            str: Public URL to access the file
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
        """
        ...

    async def generate_thumbnail(
        self, file_path: str, width: int = 200, height: int = 200
    ) -> Optional[str]:
        """
        Generate a thumbnail for an image file.

        Args:
            file_path: Relative path to the original image
            width: Desired thumbnail width
            height: Desired thumbnail height

        Returns:
            Optional[str]: Path to the thumbnail if successful, None otherwise
        """
        ...


class LocalMediaStorage:
    """Local filesystem storage backend for development."""

    ALLOWED_IMAGE_TYPES: Set[str] = {
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/svg+xml",
    }
    ALLOWED_DOCUMENT_TYPES: Set[str] = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "text/plain",
        "text/csv",
    }
    ALLOWED_VIDEO_TYPES: Set[str] = {
        "video/mp4",
        "video/quicktime",
        "video/x-msvideo",
        "video/x-ms-wmv",
    }

    async def save_file(
        self, file: UploadFile, destination: str, media_type: MediaType
    ) -> str:
        """
        Save file to local storage.

        Args:
            file: The uploaded file
            destination: Relative path where the file should be stored
            media_type: Type of media being stored

        Returns:
            str: URL to access the saved file

        Raises:
            HTTPException: If the file type is not allowed for the specified media type
        """
        # Validate file type based on media type
        content_type = file.content_type or "application/octet-stream"
        self._validate_file_type(content_type, media_type)

        # Create full path to file
        file_path = Path(settings.MEDIA_ROOT) / media_type.value / destination
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Read and write file contents
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        # Log successful file save
        logger.info(
            f"File saved successfully: {file_path} ({len(content)} bytes, {content_type})"
        )

        # Return public URL using the environment-aware media_base_url property
        return f"{settings.media_base_url}{media_type.value}/{destination}"

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
        Delete file from local storage.

        Args:
            file_path: Relative path to the file

        Returns:
            bool: True if file was successfully deleted, False otherwise
        """
        # Create full path to file
        if file_path.startswith("/"):
            file_path = file_path[1:]

        full_path = Path(settings.MEDIA_ROOT) / file_path

        # Check if file exists
        if not full_path.exists():
            logger.warning(f"Attempted to delete non-existent file: {full_path}")
            return False

        try:
            # Delete file
            full_path.unlink()
            logger.info(f"File deleted successfully: {full_path}")
            return True
        except Exception as e:
            logger.error(f"Error deleting file {full_path}: {str(e)}")
            return False

    async def generate_thumbnail(
        self, file_path: str, width: int = 200, height: int = 200
    ) -> Optional[str]:
        """
        Generate a thumbnail for an image file.

        Args:
            file_path: Relative path to the original image
            width: Desired thumbnail width
            height: Desired thumbnail height

        Returns:
            Optional[str]: Path to the thumbnail if successful, None otherwise
        """
        try:
            # Import Pillow library only when needed
            from PIL import Image

            # Normalize file path
            if file_path.startswith("/"):
                file_path = file_path[1:]

            # Get full path to original image
            original_path = Path(settings.MEDIA_ROOT) / file_path
            if not original_path.exists():
                logger.warning(f"Original image not found: {original_path}")
                return None

            # Determine thumbnail path
            filename = original_path.name
            thumbnail_name = f"thumb_{width}x{height}_{filename}"
            thumbnail_rel_path = f"thumbnails/{thumbnail_name}"
            thumbnail_path = Path(settings.MEDIA_ROOT) / "thumbnails" / thumbnail_name

            # Create thumbnails directory if it doesn't exist
            thumbnail_path.parent.mkdir(parents=True, exist_ok=True)

            # Generate thumbnail
            with Image.open(original_path) as img:
                img.thumbnail((width, height))
                img.save(thumbnail_path)

            logger.info(f"Thumbnail generated successfully: {thumbnail_path}")
            return thumbnail_rel_path

        except ImportError:
            logger.error(
                "Pillow library not installed. Please install with 'pip install Pillow'"
            )
            return None
        except Exception as e:
            logger.error(f"Error generating thumbnail: {str(e)}")
            return None

    def _validate_file_type(self, content_type: str, media_type: MediaType) -> None:
        """
        Validate that the file content type is allowed for the specified media type.

        Args:
            content_type: MIME type of the file
            media_type: Type of media being stored

        Raises:
            HTTPException: If the file type is not allowed for the specified media type
        """
        if media_type == MediaType.IMAGE and content_type not in self.ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid image type: {content_type}. Allowed types: {self.ALLOWED_IMAGE_TYPES}",
            )
        elif (
            media_type == MediaType.DOCUMENT
            and content_type not in self.ALLOWED_DOCUMENT_TYPES
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid document type: {content_type}. Allowed types: {self.ALLOWED_DOCUMENT_TYPES}",
            )
        elif (
            media_type == MediaType.VIDEO and content_type not in self.ALLOWED_VIDEO_TYPES
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid video type: {content_type}. Allowed types: {self.ALLOWED_VIDEO_TYPES}",
            )


class S3MediaStorage:
    """S3 storage backend for production."""

    async def save_file(
        self, file: UploadFile, destination: str, media_type: MediaType
    ) -> str:
        """
        Save file to S3 storage.

        Args:
            file: The uploaded file
            destination: Relative path where the file should be stored
            media_type: Type of media being stored

        Returns:
            str: URL to access the saved file

        Raises:
            HTTPException: If upload to S3 fails
        """
        # This is a stub implementation. In a real application, you would:
        # 1. Read the file content
        # 2. Upload to S3 using boto3 or similar
        # 3. Return the S3 URL or CDN URL

        logger.info(f"S3 storage backend is not fully implemented. Using CDN URL pattern")
        return f"{settings.media_base_url}{media_type.value}/{destination}"

    async def get_file_url(self, file_path: str) -> str:
        """
        Get URL for S3 file.

        Args:
            file_path: Relative path to the file

        Returns:
            str: Public URL to access the file
        """
        if file_path.startswith("/"):
            file_path = file_path[1:]

        return f"{settings.media_base_url}{file_path}"

    async def delete_file(self, file_path: str) -> bool:
        """
        Delete file from S3 storage.

        Args:
            file_path: Relative path to the file

        Returns:
            bool: True if file was successfully deleted, False otherwise
        """
        # Stub implementation
        logger.info(f"S3 delete operation not fully implemented for: {file_path}")
        return True

    async def generate_thumbnail(
        self, file_path: str, width: int = 200, height: int = 200
    ) -> Optional[str]:
        """
        Generate a thumbnail for an image file in S3.

        Args:
            file_path: Relative path to the original image
            width: Desired thumbnail width
            height: Desired thumbnail height

        Returns:
            Optional[str]: Path to the thumbnail if successful, None otherwise
        """
        # Stub implementation
        logger.info(f"S3 thumbnail generation not fully implemented for: {file_path}")

        # In production, you might use S3 Lambda functions or similar for thumbnail generation
        thumbnail_rel_path = f"thumbnails/thumb_{width}x{height}_{Path(file_path).name}"
        return thumbnail_rel_path


def get_media_storage() -> MediaStorageBackend:
    """
    Get the appropriate media storage backend based on configuration.

    Returns:
        MediaStorageBackend: Configured storage backend
    """
    storage_type = settings.MEDIA_STORAGE_TYPE.lower()

    if storage_type == "local":
        return LocalMediaStorage()
    elif storage_type == "s3":
        return S3MediaStorage()
    else:
        logger.warning(f"Unknown storage type: {storage_type}, falling back to local")
        return LocalMediaStorage()


class MediaService:
    """Service for handling media operations."""

    def __init__(self) -> None:
        """Initialize the media service with the configured storage backend."""
        self.storage = get_media_storage()
        logger.info(f"Using {settings.MEDIA_STORAGE_TYPE} storage backend in {settings.ENVIRONMENT} environment")

    async def upload_file(
        self,
        file: UploadFile,
        media_type: MediaType,
        product_id: Optional[str] = None,
        generate_thumbnail: bool = True,
    ) -> Tuple[str, Optional[str]]:
        """
        Upload a file to storage.

        Args:
            file: The uploaded file
            media_type: Type of media being uploaded
            product_id: Optional product ID to associate with the file
            generate_thumbnail: Whether to generate a thumbnail for images

        Returns:
            Tuple[str, Optional[str]]: Tuple of (file URL, thumbnail URL or None)

        Raises:
            HTTPException: If the file type is invalid or upload fails
        """
        try:
            # Generate a unique filename
            original_filename = file.filename or f"unnamed_{uuid.uuid4()}"
            file_ext = Path(original_filename).suffix
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            unique_filename = f"{timestamp}_{uuid.uuid4().hex}{file_ext}"

            # Create destination path
            if product_id:
                destination = f"{product_id}/{unique_filename}"
            else:
                destination = unique_filename

            # Save the file
            file_url = await self.storage.save_file(file, destination, media_type)

            # Generate thumbnail for images if requested
            thumbnail_url = None
            if (
                generate_thumbnail
                and media_type == MediaType.IMAGE
                and file.content_type in LocalMediaStorage.ALLOWED_IMAGE_TYPES
            ):
                # Calculate path relative to media root
                rel_path = f"{media_type.value}/{destination}"
                thumbnail_path = await self.storage.generate_thumbnail(rel_path)
                if thumbnail_path:
                    thumbnail_url = await self.storage.get_file_url(thumbnail_path)

            return file_url, thumbnail_url

        except HTTPException:
            # Re-raise HTTP exceptions
            raise
        except Exception as e:
            logger.error(f"Error uploading file: {str(e)}")
            raise HTTPException(
                status_code=500, detail=f"Failed to upload file: {str(e)}"
            ) from e

    async def delete_file(self, file_url: str) -> bool:
        """
        Delete a file from storage.

        Args:
            file_url: URL of the file to delete

        Returns:
            bool: True if file was successfully deleted, False otherwise
        """
        try:
            # Extract relative path from URL
            media_url = settings.media_base_url
            if file_url.startswith(media_url):
                rel_path = file_url[len(media_url):]
            else:
                # Fallback to the default media URL if not found
                media_url = settings.MEDIA_URL
                if file_url.startswith(media_url):
                    rel_path = file_url[len(media_url):]
                else:
                    rel_path = file_url

            # Delete the file
            return await self.storage.delete_file(rel_path)
        except Exception as e:
            logger.error(f"Error deleting file {file_url}: {str(e)}")
            return False


# Create a singleton instance
media_service = MediaService()
