from __future__ import annotations
'Base service package for standardized CRUD operations.\n\nThis package provides a base service implementation that can be extended\nby domain-specific services to provide standardized CRUD operations,\npermission checking, and lifecycle hooks.\n'
from app.services.base_service.contracts import BaseServiceProtocol
from app.services.base_service.permissions import PermissionHelper
from app.services.base_service.service import BaseService
__all__ = ['BaseService', 'BaseServiceProtocol', 'PermissionHelper']