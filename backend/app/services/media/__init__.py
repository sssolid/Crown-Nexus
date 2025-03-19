# backend/app/services/media/__init__.py
"""Media service package for handling file storage operations.

This package provides services for storing, retrieving, and managing media files
using various storage backends (local filesystem, S3, etc.).
"""
from __future__ import annotations

from app.services.media.service import MediaService


# Factory function for dependency injection
def get_media_service():
    """Factory function to get MediaService"""
    return MediaService()


__all__ = ["get_media_service", "MediaService"]
