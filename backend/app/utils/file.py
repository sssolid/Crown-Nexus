# app/utils/file.py
"""
File handling utilities for secure file operations and validation.

This module provides functions for file validation, upload handling, path manipulation,
and security checks related to files. It includes utilities for:
- Validating file types and sizes
- Handling file uploads securely
- Generating thumbnails for image files
- Sanitizing filenames to prevent path traversal attacks
- Retrieving file paths and URLs

All functions include proper error handling, logging, and security checks to ensure
file operations are performed safely and securely.
"""

from __future__ import annotations

import os
import secrets
import uuid
from datetime import datetime
from pathlib import Path
from typing import (
    BinaryIO,
    Dict,
    List,
    Literal,
    Optional,
    Protocol,
    Set,
    Tuple,
    Union,
    cast,
)

from fastapi import HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError

from app.core.config import settings
from app.core.exceptions import (
    ErrorCode,
    SecurityException,
    ValidationException,
)
from app.core.logging import get_logger
from app.models.media import MediaType

# Initialize structured logger
logger = get_logger("app.utils.file")


class ImageProcessor(Protocol):
    """Protocol defining interface for image processing operations."""

    def open(self, path: Union[str, Path]) -> "Image.Image":
        """Open an image file.

        Args:
            path: Path to the image file

        Returns:
            Image object
        """
        ...


# Type definitions for media constraints
MediaConstraints = Dict[MediaType, Set[str]]
SizeConstraints = Dict[MediaType, int]
DimensionsTuple = Tuple[int, int]


# Define allowed MIME types for each media type
ALLOWED_MIME_TYPES: MediaConstraints = {
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

# Define maximum file sizes for each media type (in bytes)
MAX_FILE_SIZES: SizeConstraints = {
    MediaType.IMAGE: 5 * 1024 * 1024,  # 5MB
    MediaType.DOCUMENT: 20 * 1024 * 1024,  # 20MB
    MediaType.VIDEO: 100 * 1024 * 1024,  # 100MB
    MediaType.OTHER: 50 * 1024 * 1024,  # 50MB
}

# Define thumbnail size
THUMBNAIL_SIZE: DimensionsTuple = (300, 300)


class FileSecurityError(SecurityException):
    """Exception raised for file security validation failures."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.SECURITY_ERROR,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize FileSecurityError.

        Args:
            message: Human-readable error description
            code: Error code from ErrorCode enum
            details: Additional error context
        """
        super().__init__(
            message=message,
            code=code,
            details=details or {},
            status_code=400,
        )


class FileValidationError(ValidationException):
    """Exception raised for file validation failures."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.VALIDATION_ERROR,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize FileValidationError.

        Args:
            message: Human-readable error description
            code: Error code from ErrorCode enum
            details: Additional error context
        """
        super().__init__(
            message=message,
            code=code,
            details=details or {},
            status_code=400,
        )


def get_media_type_from_mime(mime_type: str) -> MediaType:
    """Determine media type from MIME type.

    Args:
        mime_type: MIME type string (e.g., 'image/jpeg')

    Returns:
        MediaType: Appropriate MediaType enum value
    """
    for media_type, mime_types in ALLOWED_MIME_TYPES.items():
        if mime_type in mime_types:
            return media_type

    logger.debug(f"Unrecognized MIME type: {mime_type}, defaulting to OTHER")
    return MediaType.OTHER


def validate_file(
    file: UploadFile, allowed_types: Optional[Set[MediaType]] = None
) -> Tuple[MediaType, bool]:
    """Validate file type, size, and content.

    Performs comprehensive validation on the uploaded file including:
    - Filename validation
    - Size limits checking
    - MIME type verification
    - For images: additional image content validation

    Args:
        file: FastAPI UploadFile object
        allowed_types: Set of allowed MediaType values, if None all types are allowed

    Returns:
        Tuple containing:
        - MediaType: Detected media type
        - bool: True if file is an image, False otherwise

    Raises:
        FileValidationError: If validation fails
    """
    try:
        if not file.filename:
            logger.warning("Upload rejected: No filename provided")
            raise FileValidationError(
                message="No filename provided", details={"reason": "missing_filename"}
            )

        # Check if filename is safe (basic security check)
        if not is_safe_filename(file.filename):
            logger.warning(f"Upload rejected: Unsafe filename: {file.filename}")
            raise FileSecurityError(
                message="Filename contains unsafe characters",
                details={"filename": file.filename},
            )

        # Get file size
        file.file.seek(0, os.SEEK_END)
        file_size = file.file.tell()
        file.file.seek(0)

        # Determine MIME type and media type
        mime_type = file.content_type or "application/octet-stream"
        media_type = get_media_type_from_mime(mime_type)

        # Check if media type is allowed
        if allowed_types and media_type not in allowed_types:
            allowed_types_str = ", ".join([t.value for t in allowed_types])
            logger.warning(
                f"Upload rejected: Media type {media_type.value} not allowed",
                allowed_types=allowed_types_str,
            )
            raise FileValidationError(
                message=f"File type not allowed. Allowed types: {allowed_types_str}",
                details={
                    "detected_type": media_type.value,
                    "allowed_types": allowed_types_str,
                },
            )

        # Check if MIME type is allowed for the media type
        if mime_type not in ALLOWED_MIME_TYPES[media_type]:
            allowed_mimes = ", ".join(ALLOWED_MIME_TYPES[media_type])
            logger.warning(
                f"Upload rejected: MIME type {mime_type} not allowed for {media_type.value}",
                allowed_mimes=allowed_mimes,
            )
            raise FileValidationError(
                message=f"MIME type {mime_type} not allowed for {media_type.value}",
                details={
                    "mime_type": mime_type,
                    "media_type": media_type.value,
                    "allowed_mimes": allowed_mimes,
                },
            )

        # Check file size
        max_size = MAX_FILE_SIZES[media_type]
        if file_size > max_size:
            max_size_mb = max_size // (1024 * 1024)
            logger.warning(
                f"Upload rejected: File too large ({file_size} bytes)",
                max_size=max_size,
                media_type=media_type.value,
            )
            raise FileValidationError(
                message=f"File too large. Maximum size for {media_type.value} is {max_size_mb}MB",
                details={
                    "file_size": file_size,
                    "max_size": max_size,
                    "media_type": media_type.value,
                },
            )

        # Additional validation for images
        is_image = media_type == MediaType.IMAGE
        if is_image:
            try:
                file.file.seek(0)
                img = Image.open(file.file)
                img.verify()  # Verify image integrity
                file.file.seek(0)
                logger.debug(
                    f"Image verified successfully: {file.filename}",
                    size=file_size,
                    mime=mime_type,
                )
            except UnidentifiedImageError:
                logger.warning(f"Upload rejected: Invalid image file: {file.filename}")
                raise FileValidationError(
                    message="Invalid image file", details={"filename": file.filename}
                )
            except Exception as e:
                logger.error(
                    f"Image validation error: {str(e)}",
                    filename=file.filename,
                    exc_info=True,
                )
                raise FileValidationError(
                    message=f"Error validating image: {str(e)}",
                    details={"filename": file.filename, "error": str(e)},
                ) from e

        logger.info(
            f"File validated successfully: {file.filename}",
            media_type=media_type.value,
            size=file_size,
            mime=mime_type,
        )
        return (media_type, is_image)

    except (FileValidationError, FileSecurityError):
        # Re-raise validation errors
        raise
    except Exception as e:
        # Log and convert other exceptions to validation errors
        logger.error(f"Unexpected error validating file: {str(e)}", exc_info=True)
        raise FileValidationError(
            message=f"File validation failed: {str(e)}", details={"error": str(e)}
        ) from e


def save_upload_file(
    file: UploadFile, media_id: uuid.UUID, media_type: MediaType, is_image: bool
) -> Tuple[str, int, str]:
    """Save uploaded file to disk with secure naming.

    Args:
        file: FastAPI UploadFile object
        media_id: UUID for the media record
        media_type: MediaType enum value
        is_image: Whether the file is an image

    Returns:
        Tuple containing:
        - str: Relative path to saved file
        - int: File size in bytes
        - str: Generated media hash

    Raises:
        HTTPException: If file saving fails
    """
    try:
        # Create date-based directory structure
        upload_dir = (
            Path(settings.MEDIA_ROOT)
            / str(media_type.value)
            / datetime.now().strftime("%Y/%m/%d")
        )
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Generate secure filename using media_id
        original_ext = os.path.splitext(file.filename or "unknown")[1].lower()
        secure_filename = f"{media_id}{original_ext}"
        file_path = upload_dir / secure_filename

        # Read and save file content
        file.file.seek(0)
        with open(file_path, "wb") as f:
            file_content = file.file.read()
            f.write(file_content)
            file_size = len(file_content)

        # Generate security hash
        media_hash = secrets.token_hex(16)

        # Create thumbnail if it's an image
        if is_image:
            thumbnail_dir = (
                Path(settings.MEDIA_ROOT)
                / "thumbnails"
                / datetime.now().strftime("%Y/%m/%d")
            )
            thumbnail_dir.mkdir(parents=True, exist_ok=True)

            try:
                with Image.open(file_path) as img:
                    # Handle transparency
                    if img.mode in ["RGBA", "LA"]:
                        rgb_img = Image.new("RGB", img.size, (255, 255, 255))
                        rgb_img.paste(
                            img,
                            mask=(
                                img.split()[3] if img.mode == "RGBA" else img.split()[1]
                            ),
                        )
                        img = rgb_img
                    elif img.mode != "RGB":
                        img = img.convert("RGB")

                    # Create thumbnail
                    img.thumbnail(THUMBNAIL_SIZE)
                    thumbnail_path = thumbnail_dir / secure_filename
                    img.save(thumbnail_path, quality=85, optimize=True)

                    logger.debug(
                        f"Created thumbnail for {file_path}",
                        thumbnail_path=str(thumbnail_path),
                    )
            except Exception as e:
                # Log but don't fail if thumbnail creation fails
                logger.error(
                    f"Error creating thumbnail: {str(e)}",
                    file_path=str(file_path),
                    exc_info=True,
                )

        relative_path = str(file_path.relative_to(settings.MEDIA_ROOT))
        logger.info(
            f"File saved successfully: {relative_path}",
            size=file_size,
            media_id=str(media_id),
            media_type=media_type.value,
        )

        return (relative_path, file_size, media_hash)

    except Exception as e:
        logger.error(
            f"Error saving file: {str(e)}",
            media_id=str(media_id),
            filename=file.filename,
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file: {str(e)}",
        ) from e


def get_file_path(file_path: str) -> Path:
    """Convert URL or relative path to absolute file path.

    Args:
        file_path: URL, absolute, or relative file path

    Returns:
        Path: Absolute path to the file
    """
    # Handle URL paths
    if file_path.startswith(("http://", "https://")):
        from urllib.parse import urlparse

        parsed_url = urlparse(file_path)
        file_path = parsed_url.path

    # Remove media URL prefix if present
    if file_path.startswith(settings.MEDIA_URL):
        file_path = file_path[len(settings.MEDIA_URL) :]
    elif settings.MEDIA_CDN_URL and file_path.startswith(settings.MEDIA_CDN_URL):
        file_path = file_path[len(settings.MEDIA_CDN_URL) :]

    # Remove leading slash if present
    if file_path.startswith("/"):
        file_path = file_path[1:]

    logger.debug(f"Resolved file path: {file_path}")
    return Path(settings.MEDIA_ROOT) / file_path


def get_thumbnail_path(file_path: str) -> Optional[Path]:
    """Get thumbnail path for a given file path.

    Args:
        file_path: Path to the original file

    Returns:
        Optional[Path]: Path to thumbnail if exists, None otherwise
    """
    clean_path = str(get_file_path(file_path))

    # Ensure path is within media root for security
    if not clean_path.startswith(str(settings.MEDIA_ROOT)):
        logger.warning(f"Thumbnail path outside media root: {clean_path}")
        return None

    rel_path = Path(clean_path).relative_to(settings.MEDIA_ROOT)
    parts = rel_path.parts

    if len(parts) > 1:
        # Try standard thumbnail location
        thumbnail_path = Path(settings.MEDIA_ROOT) / "thumbnails" / "/".join(parts[1:])
        if thumbnail_path.exists():
            return thumbnail_path

        # Try alternative naming convention
        filename = parts[-1]
        thumbnail_alt = Path(settings.MEDIA_ROOT) / "thumbnails" / f"thumb_{filename}"
        if thumbnail_alt.exists():
            return thumbnail_alt

    logger.debug(f"No thumbnail found for: {file_path}")
    return None


def get_file_url(file_path: str) -> str:
    """Get public URL for a file path.

    Args:
        file_path: Path to the file

    Returns:
        str: URL to access the file
    """
    if file_path.startswith("/"):
        file_path = file_path[1:]

    return f"{settings.media_base_url}{file_path}"


def get_file_extension(filename: str) -> str:
    """Extract file extension from filename.

    Args:
        filename: Name of the file

    Returns:
        str: Extension without dot or empty string if none
    """
    if not filename or "." not in filename:
        return ""

    return filename.rsplit(".", 1)[1].lower()


def is_safe_filename(filename: str) -> bool:
    """Check if filename is safe (no path traversal).

    Args:
        filename: Name of the file to check

    Returns:
        bool: True if filename is safe, False otherwise
    """
    # Check for path traversal attempts
    if ".." in filename or "/" in filename or "\\" in filename:
        return False

    # Check for hidden files
    if filename.startswith("."):
        return False

    # Check length limit
    if len(filename) > 255:
        return False

    return True


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to remove unsafe characters.

    Args:
        filename: Original filename

    Returns:
        str: Sanitized filename
    """
    safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_."

    # Split name and extension
    name, ext = os.path.splitext(filename)

    # Filter characters
    safe_name = "".join(c for c in name if c in safe_chars)

    # Use default name if empty
    if not safe_name:
        safe_name = "file"

    # Return with lowercase extension
    sanitized = safe_name + ext.lower()
    logger.debug(f"Sanitized filename: {filename} -> {sanitized}")

    return sanitized
