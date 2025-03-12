"""
Dependencies for the fitment module.

This module provides dependency injection functions for FastAPI endpoints.
"""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

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
    # Get configuration from environment variables
    vcdb_path = os.environ.get("VCDB_PATH")
    pcdb_path = os.environ.get("PCDB_PATH")
    sqlalchemy_url = os.environ.get("FITMENT_DB_URL")

    if not vcdb_path or not pcdb_path:
        raise ConfigurationError(
            "VCDB_PATH and PCDB_PATH environment variables must be set"
        )

    # Create and return the service
    return FitmentDBService(vcdb_path, pcdb_path, sqlalchemy_url)


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

    # Configure the engine if mapping file exists
    mapping_file = os.environ.get("MODEL_MAPPINGS_PATH")
    if mapping_file and os.path.isfile(mapping_file):
        engine.configure(mapping_file)

    return engine
