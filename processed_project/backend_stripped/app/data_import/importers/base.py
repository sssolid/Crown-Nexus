from __future__ import annotations
'\nBase interfaces for data importers.\n\nThis module defines protocol classes for data importers that insert or update\ndata in the application database.\n'
from typing import Any, Dict, List, Protocol, TypeVar
T = TypeVar('T')
class Importer(Protocol[T]):
    async def import_data(self, data: List[T]) -> Dict[str, Any]:
        ...