from __future__ import annotations
from typing import Dict, Any
from app.core.cache.backends.memory import MemoryCacheBackend
from app.core.cache.backends.null import NullCacheBackend
from app.core.cache.backends.redis import RedisCacheBackend
__all__ = ['MemoryCacheBackend', 'RedisCacheBackend', 'NullCacheBackend', 'get_backend']
_backends: Dict[str, Any] = {'memory': MemoryCacheBackend, 'redis': RedisCacheBackend, 'null': NullCacheBackend}
def get_backend(name: str) -> Any:
    if name not in _backends:
        raise ValueError(f'Unknown cache backend: {name}')
    return _backends[name]