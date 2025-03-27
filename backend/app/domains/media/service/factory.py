# backend/app/services/media/factory.py
"""Factory module for creating media storage backends.

This module provides a factory for creating media storage backends based on
configuration settings, making it easy to switch between different storage
implementations.
"""
from __future__ import annotations

from typing import Optional

from app.domains.media.service.base import MediaStorageBackend, StorageBackendType
from app.domains.media.service.local import LocalMediaStorage
from app.domains.media.service.s3 import S3MediaStorage

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger("app.domains.media.service.factory")


class StorageBackendFactory:
    """Factory for creating media storage backends."""

    @staticmethod
    def get_backend(backend_type: Optional[str] = None) -> MediaStorageBackend:
        """
        Get a storage backend instance based on type.

        Args:
            backend_type: The type of backend to create.
                If None, will use the value from settings.MEDIA_STORAGE_TYPE.

        Returns:
            An instance of MediaStorageBackend.

        Raises:
            ValueError: If an unsupported backend type is specified.
        """
        # If no backend type provided, use from settings
        if backend_type is None:
            backend_type = settings.MEDIA_STORAGE_TYPE.lower()

        try:
            # Try to convert to enum for validation
            backend_enum = StorageBackendType(backend_type)
            backend_type = backend_enum.value
        except ValueError:
            valid_types = [t.value for t in StorageBackendType]
            logger.error(
                f"Invalid storage backend type: {backend_type}. "
                f"Valid types are: {', '.join(valid_types)}"
            )
            # Default to local storage if invalid type
            backend_type = StorageBackendType.LOCAL.value
            logger.warning(f"Defaulting to {backend_type} storage")

        # Create appropriate backend
        if backend_type == StorageBackendType.S3.value:
            logger.info("Creating S3 storage backend")
            return S3MediaStorage()
        elif backend_type == StorageBackendType.AZURE.value:
            # Not implemented yet
            logger.warning("Azure storage not implemented, using local storage instead")
            return LocalMediaStorage()
        else:
            # Default to local storage
            logger.info("Creating local storage backend")
            return LocalMediaStorage()
