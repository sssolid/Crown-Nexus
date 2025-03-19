# backend/app/services/media/thumbnails.py
"""Thumbnail generation utilities.

This module provides utilities for generating thumbnails from image files,
designed to be used by different storage backend implementations.
"""
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Optional, Tuple

from app.core.logging import get_logger
from app.services.media.base import FileNotFoundError, MediaStorageError

logger = get_logger(__name__)


class ThumbnailGenerator:
    """Utility class for generating thumbnails from images."""

    @staticmethod
    async def generate_thumbnail(
        file_path: Path,
        output_path: Path,
        width: int = 200,
        height: int = 200,
        quality: int = 90,
    ) -> None:
        """
        Generate a thumbnail for an image file.

        Args:
            file_path: Path to the original image
            output_path: Path where the thumbnail should be saved
            width: Desired thumbnail width
            height: Desired thumbnail height
            quality: JPEG quality (1-100)

        Raises:
            FileNotFoundError: If the original file doesn't exist
            MediaStorageError: If thumbnail generation fails
        """
        # Check if file exists
        if not file_path.exists():
            raise FileNotFoundError(f"Original image not found: {file_path}")

        # Run CPU-intensive image processing in a thread pool
        await asyncio.to_thread(
            ThumbnailGenerator._generate_thumbnail_sync,
            file_path,
            output_path,
            width,
            height,
            quality,
        )

    @staticmethod
    def _generate_thumbnail_sync(
        file_path: Path, output_path: Path, width: int, height: int, quality: int
    ) -> None:
        """
        Generate a thumbnail synchronously (to be run in a thread pool).

        Args:
            file_path: Path to the original image
            output_path: Path where the thumbnail should be saved
            width: Desired thumbnail width
            height: Desired thumbnail height
            quality: JPEG quality (1-100)

        Raises:
            MediaStorageError: If thumbnail generation fails
        """
        try:
            # Import Pillow library only when needed
            from PIL import Image, UnidentifiedImageError
        except ImportError:
            raise MediaStorageError(
                "Pillow library not installed. Please install with 'pip install Pillow'"
            )

        try:
            # Create output directory if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Generate thumbnail
            with Image.open(file_path) as img:
                # Handle different image modes
                if img.mode in ["RGBA", "LA"]:
                    # Convert transparent images to RGB with white background
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    background.paste(
                        img,
                        mask=img.split()[3] if img.mode == "RGBA" else img.split()[1],
                    )
                    img = background
                elif img.mode != "RGB":
                    img = img.convert("RGB")

                # Create thumbnail with high quality
                img.thumbnail((width, height), Image.LANCZOS)
                img.save(output_path, format="JPEG", quality=quality, optimize=True)

            logger.info(
                "thumbnail_generated",
                original=str(file_path),
                thumbnail=str(output_path),
                width=width,
                height=height,
            )

        except UnidentifiedImageError:
            raise MediaStorageError(f"Not a valid image file: {file_path}")
        except Exception as e:
            raise MediaStorageError(f"Error generating thumbnail: {str(e)}") from e

    @staticmethod
    def get_supported_formats() -> Tuple[str, ...]:
        """
        Get a list of supported image formats for thumbnail generation.

        Returns:
            Tuple of supported file extensions (lowercase, with dot)
        """
        return (".jpg", ".jpeg", ".png", ".gif", ".webp")

    @staticmethod
    def can_generate_thumbnail(file_path: str) -> bool:
        """
        Check if a thumbnail can be generated for a file based on its extension.

        Args:
            file_path: Path to the file

        Returns:
            bool: True if a thumbnail can be generated, False otherwise
        """
        return any(
            file_path.lower().endswith(ext)
            for ext in ThumbnailGenerator.get_supported_formats()
        )

    @staticmethod
    def get_thumbnail_path(
        original_path: str,
        width: int = 200,
        height: int = 200,
        thumbnails_dir: str = "thumbnails",
    ) -> str:
        """
        Get the path where a thumbnail should be stored.

        Args:
            original_path: Path to the original image
            width: Thumbnail width
            height: Thumbnail height
            thumbnails_dir: Directory for storing thumbnails

        Returns:
            str: Path to the thumbnail
        """
        filename = Path(original_path).name
        thumbnail_name = f"thumb_{width}x{height}_{filename}"
        return f"{thumbnails_dir}/{thumbnail_name}"
