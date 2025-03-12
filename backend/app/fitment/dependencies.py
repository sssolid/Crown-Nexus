"""
Dependencies for the fitment module.

This module provides dependency injection functions for FastAPI endpoints.
"""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from app.core.config import settings as app_settings
from .db import FitmentDBService
from .exceptions import ConfigurationError
from .mapper import FitmentMappingEngine


@lru_cache(maxsize=1)
def get_fitment_db_service() -> FitmentDBService:
    """
    Get a singleton instance of the FitmentDBService.

    Returns:
        FitmentDBService instance

    Raises:
        ConfigurationError: If required configuration is missing
    """
    # Get configuration from main app settings
    vcdb_path = app_settings.VCDB_PATH
    pcdb_path = app_settings.PCDB_PATH

    # For database URL, check for fitment-specific setting first,
    # then fall back to main app database
    sqlalchemy_url = getattr(app_settings, "FITMENT_DB_URL", None) or str(app_settings.SQLALCHEMY_DATABASE_URI)

    if not vcdb_path or not pcdb_path:
        raise ConfigurationError(
            "VCDB_PATH and PCDB_PATH environment variables must be set"
        )

    # Try to resolve file paths if they don't exist
    vcdb_path = _resolve_file_path(vcdb_path)
    pcdb_path = _resolve_file_path(pcdb_path)

    # Create and return the service
    return FitmentDBService(vcdb_path, pcdb_path, sqlalchemy_url)


def _resolve_file_path(file_path: str) -> str:
    """
    Resolve a file path to an absolute path, trying several common locations.

    Args:
        file_path: The file path to resolve

    Returns:
        The resolved absolute file path

    Raises:
        ConfigurationError: If the file cannot be found
    """
    # If it's already an absolute path and exists
    if os.path.isabs(file_path) and os.path.isfile(file_path):
        return file_path

    # If it exists as is (relative to current directory)
    if os.path.isfile(file_path):
        return os.path.abspath(file_path)

    # Try relative to project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    abs_path = os.path.join(project_root, file_path)
    if os.path.isfile(abs_path):
        return abs_path

    # Try in data directory in project root
    data_path = os.path.join(project_root, "data", os.path.basename(file_path))
    if os.path.isfile(data_path):
        return data_path

    raise ConfigurationError(f"Could not find file: {file_path}")


@lru_cache(maxsize=1)
def get_fitment_mapping_engine() -> FitmentMappingEngine:
    """
    Get a singleton instance of the FitmentMappingEngine.

    Returns:
        FitmentMappingEngine instance

    Raises:
        ConfigurationError: If required configuration is missing
    """
    # Get the DB service
    db_service = get_fitment_db_service()

    # Create the mapping engine
    engine = FitmentMappingEngine(db_service)

    return engine


async def initialize_mapping_engine() -> None:
    """
    Initialize the mapping engine with database mappings.

    This should be called during application startup.
    """
    engine = get_fitment_mapping_engine()

    # Try to configure from database
    try:
        await engine.configure_from_database()
        return
    except Exception as e:
        # Log the error but continue to try file-based configuration
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Failed to load model mappings from database: {str(e)}")

    # If database loading fails or is not available, try file-based configuration
    mapping_file = getattr(app_settings, "MODEL_MAPPINGS_PATH", None)
    if mapping_file and os.path.isfile(_resolve_file_path(mapping_file)):
        try:
            resolved_path = _resolve_file_path(mapping_file)
            engine.configure_from_file(resolved_path)

            # Try to import mappings to database if database is available
            try:
                await engine.db_service.import_mappings_from_json(engine.model_mappings)
                import logging
                logger = logging.getLogger(__name__)
                logger.info("Successfully imported mappings from file to database")
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Failed to import mappings to database: {str(e)}")
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to load model mappings from file: {str(e)}")
            raise ConfigurationError(f"Failed to configure mapping engine: {str(e)}") from e
