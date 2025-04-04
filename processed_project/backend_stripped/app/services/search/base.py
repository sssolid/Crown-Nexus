from __future__ import annotations
'Base interfaces and types for the search system.\n\nThis module defines common types, protocols, and interfaces\nused throughout the search service components.\n'
from typing import Any, Dict, Optional, Protocol, TypeVar
T = TypeVar('T')
class SearchProvider(Protocol):
    async def search(self, search_term: Optional[str], filters: Dict[str, Any], page: int, page_size: int, **kwargs: Any) -> Dict[str, Any]:
        ...
    async def initialize(self) -> None:
        ...
    async def shutdown(self) -> None:
        ...
class SearchResult(Dict[str, Any]):
    pass