from __future__ import annotations

"""Autocare domain initialization.

This module serves as the public interface for the Autocare database integration.
It exports key functionality while hiding implementation details for interacting
with Auto Care Association standards and databases (VCdb, PCdb, PAdb, Qdb, ACES, PIES).
"""

# Re-export public interfaces from sub-domains
from app.domains.autocare.vcdb.service import VCdbService
from app.domains.autocare.pcdb.service import PCdbService
from app.domains.autocare.padb.service import PAdbService
from app.domains.autocare.qdb.service import QdbService
from app.domains.autocare.fitment.service import FitmentMappingService

# Core schemas and models
from app.domains.autocare.schemas import (
    AutocareImportParams,
    AutocareExportParams,
    FitmentSearchParams,
)

# Exceptions
from app.domains.autocare.exceptions import (
    AutocareException,
    InvalidVehicleDataException,
    InvalidPartDataException,
    MappingNotFoundException,
    ImportException,
    ExportException,
)

# Initialize domain event handlers
from app.domains.autocare import handlers

__all__ = [
    # Services
    "VCdbService",
    "PCdbService",
    "PAdbService",
    "QdbService",
    "FitmentMappingService",
    
    # Schemas
    "AutocareImportParams",
    "AutocareExportParams",
    "FitmentSearchParams",
    
    # Exceptions
    "AutocareException",
    "InvalidVehicleDataException",
    "InvalidPartDataException",
    "MappingNotFoundException",
    "ImportException",
    "ExportException",
]
