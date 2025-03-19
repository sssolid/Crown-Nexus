# backend/app/services/media/__init__.py
"""Media service package for handling file storage operations.

This package provides services for storing, retrieving, and managing media files
using various storage backends (local filesystem, S3, etc.).
"""
from __future__ import annotations

from typing import Optional

from app.core.dependency_manager import dependency_manager
from app.services.media.service import MediaService

# Create a singleton instance
media_service = MediaService()

# Register with dependency manager
dependency_manager.register_dependency("media_service", media_service)

__all__ = ["media_service", "MediaService"]
