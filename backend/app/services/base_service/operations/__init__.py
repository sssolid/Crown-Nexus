# /app/services/base_service/operations/__init__.py
from __future__ import annotations

"""Operations for the base service.

This package provides the core operations for CRUD functionality
that can be used by any service implementation.
"""

from app.services.base_service.operations.create_update import CreateUpdateOperations
from app.services.base_service.operations.read_delete import ReadDeleteOperations

__all__ = ["CreateUpdateOperations", "ReadDeleteOperations"]
