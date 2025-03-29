from __future__ import annotations
'Operations for the base service.\n\nThis package provides the core operations for CRUD functionality\nthat can be used by any service implementation.\n'
from app.services.base_service.operations.create_update import CreateUpdateOperations
from app.services.base_service.operations.read_delete import ReadDeleteOperations
__all__ = ['CreateUpdateOperations', 'ReadDeleteOperations']