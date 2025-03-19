from __future__ import annotations
from typing import Dict, Any

from app.core.cache.backends.memory import MemoryCacheBackend
from app.core.cache.backends.redis import RedisCacheBackend
from app.core.cache.backends.null import NullCacheBackend

# Export backend classes
__all__ = ["MemoryCacheBackend", "RedisCacheBackend", "NullCacheBackend", "get_backend"]

# Backend registry
_backends: Dict[str, Any] = {
    "memory": MemoryCacheBackend,
    "redis": RedisCacheBackend,
    "null": NullCacheBackend,
}


def get_backend(name: str) -> Any:
    """Get cache backend by name."""
    if name not in _backends:
        raise ValueError(f"Unknown cache backend: {name}")
    return _backends[name]
