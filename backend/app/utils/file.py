from __future__ import annotations

import os
import secrets
import uuid
from datetime import datetime
from pathlib import Path
from typing import BinaryIO, List, Optional, Set, Tuple, Union

from fastapi import HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError

from app.core.config import settings
from app.models.media import MediaType


# Allowed MIME types by media type
ALLOWED_MIME_TYPES = {
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
        "application/vnd.ms-powerpoint",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "text/plain",
        "text/csv",
    },
    MediaType.VIDEO: {
        "video/mp4",
        "video/mpeg",
        "video/webm",
        "video/quicktime",
    },
    MediaType.OTHER: {
        "application/zip",
        "application/x-zip-compressed",
        "application/octet-stream",
    },
}

# File size limits (in bytes)
MAX_FILE_SIZES = {
    MediaType.IMAGE: 5 * 1024 * 1024,  # 5MB
    MediaType.DOCUMENT: 20 * 1024 * 1024,  # 20MB
    MediaType.VIDEO: 100 * 1024 * 1024,  # 100MB
    MediaType.OTHER: 50 * 1024 * 1024,  # 50MB
}

# Image dimensions for thumbnails
THUMBNAIL_SIZE = (300, 300)


def get_media_type_from_mime(mime_type: str) -> MediaType:
    """
    Determine the media type from MIME type.

    Args:
        mime_type: MIME type of the file

    Returns:
        MediaType: Determined media type
    """
    for media_type, mime_types in ALLOWED_MIME_TYPES.items():
        if mime_type in mime_types:
            return media_type
    return MediaType.OTHER


def validate_file(
    file: UploadFile,
    allowed_types: Optional[Set[MediaType]] = None
) -> Tuple[MediaType, bool]:
    """
    Validate a file for upload.

    Args:
        file: Uploaded file
        allowed_types: Set of allowed media types (if None, all types are allowed)

    Returns:
        Tuple[MediaType, bool]: Media type and whether the file is an image

    Raises:
        HTTPException: If file is invalid
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided",
        )

    # Check file size (first byte read won't change file position)
    file_size = len(file.file.read())
    file.file.seek(0)  # Reset file position

    # Get MIME type and media type
    mime_type = file.content_type or "application/octet-stream"
    media_type = get_media_type_from_mime(mime_type)

    # Check if media type is allowed
    if allowed_types and media_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(t.value for t in allowed_types)}",
        )

    # Check if MIME type is allowed for the media type
    if mime_type not in ALLOWED_MIME_TYPES[media_type]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"MIME type {mime_type} not allowed for {media_type.value}",
        )

    # Check file size
    max_size = MAX_FILE_SIZES[media_type]
    if file_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size for {media_type.value} is {max_size // (1024 * 1024)}MB",
        )

    # Additional validation for images
    is_image = media_type == MediaType.IMAGE
    if is_image:
        try:
            img = Image.open(file.file)
            img.verify()
            file.file.seek(0)  # Reset file position after reading
        except UnidentifiedImageError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image file",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error validating image: {str(e)}",
            )

    return media_type, is_image


def save_upload_file(
    file: UploadFile,
    media_id: uuid.UUID,
    media_type: MediaType,
    is_image: bool
) -> Tuple[str, int, str]:
    """
    Save an uploaded file to disk.

    Args:
        file: Uploaded file
        media_id: ID of the media record
        media_type: Type of media
        is_image: Whether the file is an image

    Returns:
        Tuple[str, int, str]: File path, file size, and media hash
    """
    # Create directory structure if it doesn't exist
    upload_dir = Path(settings.MEDIA_ROOT) / str(media_type.value) / datetime.now().strftime("%Y/%m/%d")
    os.makedirs(upload_dir, exist_ok=True)

    # Generate secure filename
    original_ext = os.path.splitext(file.filename or "unknown")[1].lower()
    secure_filename = f"{media_id}{original_ext}"

    # Save the file
    file_path = upload_dir / secure_filename
    with open(file_path, "wb") as f:
        file_content = file.file.read()
        f.write(file_content)
        file_size = len(file_content)

    # Generate media hash
    media_hash = secrets.token_hex(16)

    # Create thumbnail for images
    if is_image:
        thumbnail_dir = Path(settings.MEDIA_ROOT) / "thumbnails" / datetime.now().strftime("%Y/%m/%d")
        os.makedirs(thumbnail_dir, exist_ok=True)

        try:
            with Image.open(file_path) as img:
                img.thumbnail(THUMBNAIL_SIZE)
                thumbnail_path = thumbnail_dir / secure_filename
                img.save(thumbnail_path)
        except Exception as e:
            # If thumbnail creation fails, log but continue
            print(f"Error creating thumbnail: {str(e)}")

    # Return relative path for storage in database
    relative_path = str(file_path.relative_to(settings.MEDIA_ROOT))
    return relative_path, file_size, media_hash


def get_file_path(file_path: str) -> Path:
    """
    Get the absolute path of a file.

    Args:
        file_path: Relative path from media root

    Returns:
        Path: Absolute path to the file
    """
    return Path(settings.MEDIA_ROOT) / file_path


def get_thumbnail_path(file_path: str) -> Optional[Path]:
    """
    Get the thumbnail path for an image.

    Args:
        file_path: Relative path from media root

    Returns:
        Optional[Path]: Absolute path to the thumbnail, or None if not found
    """
    # Replace the media type directory with 'thumbnails'
    parts = Path(file_path).parts
    if len(parts) > 1:
        thumbnail_path = Path(settings.MEDIA_ROOT) / "thumbnails" / "/".join(parts[1:])
        if thumbnail_path.exists():
            return thumbnail_path

    return None
