# backend/app/utils/file.py
"""
File handling utilities.

This module provides functions for handling files within the application:
- File validation
- File uploads and storage
- Path resolution
- Thumbnail generation

These utilities ensure consistent and secure handling of user-uploaded
files across the application.
"""

from __future__ import annotations

import os
import secrets
import uuid
from datetime import datetime
from pathlib import Path
from typing import BinaryIO, Dict, List, Optional, Set, Tuple, Union

from fastapi import HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError

from app.core.config import Environment, settings
from app.models.media import MediaType


# Allowed MIME types by media type
ALLOWED_MIME_TYPES: Dict[MediaType, Set[str]] = {
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
MAX_FILE_SIZES: Dict[MediaType, int] = {
    MediaType.IMAGE: 5 * 1024 * 1024,  # 5MB
    MediaType.DOCUMENT: 20 * 1024 * 1024,  # 20MB
    MediaType.VIDEO: 100 * 1024 * 1024,  # 100MB
    MediaType.OTHER: 50 * 1024 * 1024,  # 50MB
}

# Image dimensions for thumbnails
THUMBNAIL_SIZE: Tuple[int, int] = (300, 300)


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

    Performs various validations on the uploaded file:
    - Filename presence
    - File size within limits
    - MIME type allowed for the media type
    - Image validity for image files

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
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
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
            file.file.seek(0)  # Reset file position before reading
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

    Handles saving the file to the appropriate directory and creating
    thumbnails for images.

    Args:
        file: Uploaded file
        media_id: ID of the media record
        media_type: Type of media
        is_image: Whether the file is an image

    Returns:
        Tuple[str, int, str]: File path, file size, and media hash

    Raises:
        IOError: If file saving fails
    """
    # Create directory structure if it doesn't exist
    upload_dir = Path(settings.MEDIA_ROOT) / str(media_type.value) / datetime.now().strftime("%Y/%m/%d")
    os.makedirs(upload_dir, exist_ok=True)

    # Generate secure filename
    original_ext = os.path.splitext(file.filename or "unknown")[1].lower()
    secure_filename = f"{media_id}{original_ext}"

    # Save the file
    file_path = upload_dir / secure_filename
    file.file.seek(0)  # Ensure we're at the start of the file

    try:
        with open(file_path, "wb") as f:
            file_content = file.file.read()
            f.write(file_content)
            file_size = len(file_content)
    except IOError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file: {str(e)}",
        )

    # Generate media hash for integrity checking
    media_hash = secrets.token_hex(16)

    # Create thumbnail for images
    if is_image:
        thumbnail_dir = Path(settings.MEDIA_ROOT) / "thumbnails" / datetime.now().strftime("%Y/%m/%d")
        os.makedirs(thumbnail_dir, exist_ok=True)

        try:
            with Image.open(file_path) as img:
                # Convert to RGB if necessary (e.g., for PNG with alpha channel)
                if img.mode in ['RGBA', 'LA']:
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    rgb_img.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else img.split()[1])
                    img = rgb_img
                elif img.mode != 'RGB':
                    img = img.convert('RGB')

                # Create thumbnail
                img.thumbnail(THUMBNAIL_SIZE)
                thumbnail_path = thumbnail_dir / secure_filename
                img.save(thumbnail_path, quality=85, optimize=True)
        except Exception as e:
            # Log but don't fail if thumbnail creation fails
            print(f"Error creating thumbnail: {str(e)}")

    # Return relative path for storage in database
    relative_path = str(file_path.relative_to(settings.MEDIA_ROOT))
    return relative_path, file_size, media_hash


def get_file_path(file_path: str) -> Path:
    """
    Get the absolute path of a file.

    Args:
        file_path: Relative path from media root or full URL

    Returns:
        Path: Absolute path to the file
    """
    # Handle URLs - extract the path part
    if file_path.startswith(('http://', 'https://')):
        # If it's a fully qualified URL (e.g., from CDN), find the path part
        # Extract the path component from a URL like https://cdn.example.com/media/path/to/file.jpg
        from urllib.parse import urlparse
        parsed_url = urlparse(file_path)
        file_path = parsed_url.path

    # Handle media URL paths
    if file_path.startswith(settings.MEDIA_URL):
        file_path = file_path[len(settings.MEDIA_URL):]
    elif settings.MEDIA_CDN_URL and file_path.startswith(settings.MEDIA_CDN_URL):
        file_path = file_path[len(settings.MEDIA_CDN_URL):]

    # Remove leading slash if present
    if file_path.startswith('/'):
        file_path = file_path[1:]

    # Return the absolute path
    return Path(settings.MEDIA_ROOT) / file_path


def get_thumbnail_path(file_path: str) -> Optional[Path]:
    """
    Get the thumbnail path for an image.

    Args:
        file_path: Relative path from media root or full URL

    Returns:
        Optional[Path]: Absolute path to the thumbnail, or None if not found
    """
    # Convert to a clean path first
    clean_path = str(get_file_path(file_path))

    # If the path doesn't exist within MEDIA_ROOT, it might be external
    if not clean_path.startswith(str(settings.MEDIA_ROOT)):
        return None

    # Extract parts relative to media root
    rel_path = Path(clean_path).relative_to(settings.MEDIA_ROOT)

    # Replace the media type directory with 'thumbnails'
    parts = rel_path.parts
    if len(parts) > 1:
        thumbnail_path = Path(settings.MEDIA_ROOT) / "thumbnails" / "/".join(parts[1:])
        if thumbnail_path.exists():
            return thumbnail_path

        # Try alternative format with thumb_ prefix
        filename = parts[-1]
        thumbnail_alt = Path(settings.MEDIA_ROOT) / "thumbnails" / f"thumb_{filename}"
        if thumbnail_alt.exists():
            return thumbnail_alt

    return None


def get_file_url(file_path: str) -> str:
    """
    Get the URL for a file path, taking environment into account.

    Args:
        file_path: Relative path from media root

    Returns:
        str: Full URL to access the file
    """
    # Remove leading slash if present
    if file_path.startswith('/'):
        file_path = file_path[1:]

    # Use the environment-aware media_base_url property
    return f"{settings.media_base_url}{file_path}"


def get_file_extension(filename: str) -> str:
    """
    Get the file extension from a filename.

    Args:
        filename: Filename to extract extension from

    Returns:
        str: File extension (lowercase, without leading period)
    """
    if not filename or '.' not in filename:
        return ""

    return filename.rsplit('.', 1)[1].lower()


def is_safe_filename(filename: str) -> bool:
    """
    Check if a filename is safe to use.

    Validates that the filename doesn't contain any potentially
    dangerous characters or path traversal attempts.

    Args:
        filename: Filename to check

    Returns:
        bool: True if filename is safe, False otherwise
    """
    # Basic check for path traversal
    if '..' in filename or '/' in filename or '\\' in filename:
        return False

    # Check for starting with a period (hidden file)
    if filename.startswith('.'):
        return False

    # Check length
    if len(filename) > 255:
        return False

    # Add more checks as needed

    return True


def sanitize_filename(filename: str) -> str:
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
    safe_name = ''.join(c for c in name if c in safe_chars)

    # If the name becomes empty, use a default
    if not safe_name:
        safe_name = "file"

    # Return the sanitized name with the original extension
    return safe_name + ext.lower()
