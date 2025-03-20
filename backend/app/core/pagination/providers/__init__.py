# /app/core/pagination/providers/__init__.py
from __future__ import annotations

"""Pagination provider implementations.

This package provides different implementations of the PaginationProvider protocol
for paginating data in various ways.
"""

from app.core.pagination.providers.cursor import CursorPaginationProvider
from app.core.pagination.providers.offset import OffsetPaginationProvider

__all__ = ["OffsetPaginationProvider", "CursorPaginationProvider"]
