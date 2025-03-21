from __future__ import annotations
'Pagination provider implementations.\n\nThis package provides different implementations of the PaginationProvider protocol\nfor paginating data in various ways.\n'
from app.core.pagination.providers.cursor import CursorPaginationProvider
from app.core.pagination.providers.offset import OffsetPaginationProvider
__all__ = ['OffsetPaginationProvider', 'CursorPaginationProvider']