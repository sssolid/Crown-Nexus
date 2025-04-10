from __future__ import annotations
'\nBase interfaces for data processors.\n\nThis module defines protocol classes for data processors that transform and validate\nraw data into structured formats suitable for importing into the application.\n'
from typing import Any, Dict, List, Protocol, TypeVar
T = TypeVar('T')
class Processor(Protocol[T]):
    async def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        ...
    async def validate(self, data: List[Dict[str, Any]]) -> List[T]:
        ...