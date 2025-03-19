# backend/app/services/media/s3.py
"""Amazon S3 storage backend implementation.

This module provides an S3 implementation of the MediaStorageBackend protocol,
suitable for production environments with scalable cloud storage.
"""
from __future__ import annotations

import asyncio
import tempfile
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, AsyncGenerator, BinaryIO, Dict, Optional, Set, Union

import aiofiles
import aioboto3
from fastapi import UploadFile

from app.core.config import settings
from app.core.logging import get_logger
from app.models.media import MediaType
from app.services.media.base import (
    FileNotFoundError,
    MediaStorageBackend,
    MediaStorageError,
    StorageConnectionError,
)
from app.services.media.thumbnails import ThumbnailGenerator

logger = get_logger(__name__)


@dataclass
class S3MediaStorage:
    """Amazon S3 storage backend for production."""

    bucket_name: str = field(default_factory=lambda: settings.AWS_STORAGE_BUCKET_NAME)
    region_name: str = field(default_factory=lambda: settings.AWS_REGION)
    access_key_id: Optional[str] = field(
        default_factory=lambda: settings.AWS_ACCESS_KEY_ID
    )
    secret_access_key: Optional[str] = field(
        default_factory=lambda: settings.AWS_SECRET_ACCESS_KEY
    )
    endpoint_url: Optional[str] = field(
        default_factory=lambda: settings.AWS_S3_ENDPOINT_URL
    )
    cdn_url: Optional[str] = field(default_factory=lambda: settings.MEDIA_CDN_URL)

    # S3 client - will be initialized in initialize()
    _session: Optional[Any] = None
    _client: Optional[Any] = None
    _resource: Optional[Any] = None

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

    async def initialize(self) -> None:
        """
        Initialize S3 client and create bucket if it doesn't exist.

        Raises:
            StorageConnectionError: If connection to S3 fails
        """
        try:
            # Create session and client
            self._session = aioboto3.Session(
                aws_access_key_id=self.access_key_id,
                aws_secret_access_key=self.secret_access_key,
                region_name=self.region_name,
            )

            # Initialize S3 client
            self._client = self._session.client(
                "s3",
                endpoint_url=self.endpoint_url,
            )

            # Initialize S3 resource
            self._resource = self._session.resource(
                "s3",
                endpoint_url=self.endpoint_url,
            )

            # Check if bucket exists, create if it doesn't
            async with self._client as client:
                try:
                    await client.head_bucket(Bucket=self.bucket_name)
                    logger.info("s3_bucket_exists", bucket=self.bucket_name)
                except Exception:
                    # Create bucket if it doesn't exist
                    await client.create_bucket(
                        Bucket=self.bucket_name,
                        CreateBucketConfiguration={
                            "LocationConstraint": self.region_name
                        },
                    )
                    logger.info("s3_bucket_created", bucket=self.bucket_name)

            logger.info(
                "s3_storage_initialized",
                bucket=self.bucket_name,
                region=self.region_name,
            )

        except Exception as e:
            logger.error(
                "s3_initialization_failed",
                bucket=self.bucket_name,
                error=str(e),
                exc_info=True,
            )
            raise StorageConnectionError(
                f"Failed to initialize S3 storage: {str(e)}"
            ) from e

    async def save_file(
        self,
        file: Union[UploadFile, BinaryIO, bytes],
        destination: str,
        media_type: MediaType,
        content_type: Optional[str] = None,
    ) -> str:
        """
        Save file to S3 storage.

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
        if not self._client:
            await self.initialize()

        # Validate media type
        if media_type not in MediaType:
            raise ValueError(f"Invalid media type: {media_type}")

        # Determine S3 key (path)
        s3_key = f"{media_type.value}/{destination}"

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

        try:
            # Read file content
            if isinstance(file, UploadFile):
                content = await file.read()
            elif isinstance(file, bytes):
                content = file
            else:
                # Handle file-like objects
                content = file.read()
                if not isinstance(content, bytes):
                    content = content.encode("utf-8")

            # Upload to S3
            extra_args = {}
            if file_content_type:
                extra_args["ContentType"] = file_content_type

            async with self._client as client:
                await client.put_object(
                    Bucket=self.bucket_name, Key=s3_key, Body=content, **extra_args
                )

            logger.info(
                "s3_file_saved",
                bucket=self.bucket_name,
                key=s3_key,
                size=len(content),
                content_type=file_content_type,
                media_type=media_type.value,
            )

            # Return URL
            return await self.get_file_url(s3_key)

        except Exception as e:
            logger.error(
                "s3_file_save_failed",
                bucket=self.bucket_name,
                key=s3_key,
                error=str(e),
                exc_info=True,
            )
            raise MediaStorageError(f"Failed to save file to S3: {str(e)}") from e

    async def get_file_url(self, file_path: str) -> str:
        """
        Get URL for S3 file.

        Args:
            file_path: Relative path to the file

        Returns:
            str: Public URL to access the file
        """
        # Strip leading slash if present
        if file_path.startswith("/"):
            file_path = file_path[1:]

        # Use CDN URL if available
        if self.cdn_url:
            return f"{self.cdn_url.rstrip('/')}/{file_path}"

        # Otherwise use S3 URL
        region_url = f".{self.region_name}" if self.region_name else ""
        return f"https://{self.bucket_name}.s3{region_url}.amazonaws.com/{file_path}"

    async def delete_file(self, file_path: str) -> bool:
        """
        Delete file from S3 storage.

        Args:
            file_path: Relative path to the file

        Returns:
            bool: True if file was successfully deleted, False otherwise

        Raises:
            MediaStorageError: If deletion fails
        """
        if not self._client:
            await self.initialize()

        # Strip leading slash if present
        if file_path.startswith("/"):
            file_path = file_path[1:]

        try:
            # Check if file exists first
            if not await self.file_exists(file_path):
                logger.warning(
                    "s3_file_not_found", bucket=self.bucket_name, key=file_path
                )
                raise FileNotFoundError(f"File not found in S3: {file_path}")

            # Delete the file
            async with self._client as client:
                await client.delete_object(Bucket=self.bucket_name, Key=file_path)

            logger.info("s3_file_deleted", bucket=self.bucket_name, key=file_path)
            return True

        except Exception as e:
            if isinstance(e, FileNotFoundError):
                raise

            logger.error(
                "s3_file_delete_failed",
                bucket=self.bucket_name,
                key=file_path,
                error=str(e),
                exc_info=True,
            )
            raise MediaStorageError(f"Failed to delete file from S3: {str(e)}") from e

    async def file_exists(self, file_path: str) -> bool:
        """
        Check if a file exists in S3 storage.

        Args:
            file_path: Relative path to the file

        Returns:
            bool: True if file exists, False otherwise
        """
        if not self._client:
            await self.initialize()

        # Strip leading slash if present
        if file_path.startswith("/"):
            file_path = file_path[1:]

        try:
            async with self._client as client:
                await client.head_object(Bucket=self.bucket_name, Key=file_path)
            return True
        except Exception:
            return False

    async def generate_thumbnail(
        self, file_path: str, width: int = 200, height: int = 200
    ) -> Optional[str]:
        """
        Generate a thumbnail for an image file in S3.

        This implementation downloads the file, generates the thumbnail locally,
        then uploads it back to S3. In a production environment, you might want
        to use a service like AWS Lambda or a dedicated image processing service.

        Args:
            file_path: Relative path to the original image
            width: Desired thumbnail width
            height: Desired thumbnail height

        Returns:
            Optional[str]: Path to the thumbnail if successful, None otherwise

        Raises:
            MediaStorageError: If thumbnail generation fails
        """
        if not self._client:
            await self.initialize()

        # Normalize file path
        if file_path.startswith("/"):
            file_path = file_path[1:]

        # Skip thumbnail generation for non-image files
        if not ThumbnailGenerator.can_generate_thumbnail(file_path):
            return None

        try:
            # Define thumbnail key in S3
            thumbnail_key = ThumbnailGenerator.get_thumbnail_path(
                file_path, width, height
            )

            # Check if thumbnail already exists
            if await self.file_exists(thumbnail_key):
                return thumbnail_key

            # Create a temporary directory for processing
            @asynccontextmanager
            async def temp_file() -> AsyncGenerator[Path, None]:
                with tempfile.NamedTemporaryFile(delete=False) as tmp:
                    tmp_path = Path(tmp.name)
                try:
                    yield tmp_path
                finally:
                    if tmp_path.exists():
                        tmp_path.unlink()

            # Download original image
            async with self._client as client:
                response = await client.get_object(
                    Bucket=self.bucket_name, Key=file_path
                )
                body = await response["Body"].read()

            # Process image locally
            async with temp_file() as original_path, temp_file() as thumbnail_path:
                # Save original image to temp file
                async with aiofiles.open(original_path, "wb") as f:
                    await f.write(body)

                # Generate thumbnail
                await ThumbnailGenerator.generate_thumbnail(
                    original_path, thumbnail_path, width, height
                )

                # Read the thumbnail file
                async with aiofiles.open(thumbnail_path, "rb") as f:
                    thumbnail_data = await f.read()

                # Upload thumbnail to S3
                async with self._client as client:
                    await client.put_object(
                        Bucket=self.bucket_name,
                        Key=thumbnail_key,
                        Body=thumbnail_data,
                        ContentType="image/jpeg",
                    )

            logger.info(
                "s3_thumbnail_generated",
                bucket=self.bucket_name,
                original_key=file_path,
                thumbnail_key=thumbnail_key,
                width=width,
                height=height,
            )
            return thumbnail_key

        except Exception as e:
            logger.error(
                "s3_thumbnail_generation_failed",
                bucket=self.bucket_name,
                original_key=file_path,
                error=str(e),
                exc_info=True,
            )
            if isinstance(e, (FileNotFoundError, MediaStorageError)):
                raise
            raise MediaStorageError(f"Failed to generate S3 thumbnail: {str(e)}") from e
