from __future__ import annotations
'\nBase interfaces for data source connectors.\n\nThis module defines protocol classes for data source connectors that extract\ndata from various sources like databases, files, and APIs.\n'
from typing import Any, Dict, List, Protocol, TypeVar, Optional
T = TypeVar('T')
class Connector(Protocol):
    async def connect(self) -> None:
        ...
    async def extract(self, query: str, limit: Optional[int]=None, **params: Any) -> List[Dict[str, Any]]:
        ...
    async def close(self) -> None:
        ...