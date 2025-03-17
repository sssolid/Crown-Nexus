from __future__ import annotations
import json
import pickle
from typing import Any, Dict, List, Optional, Pattern, Set, TypeVar, Union, cast
import redis.asyncio as redis
from redis.asyncio import Redis
from app.core.cache.base import CacheBackend
from app.core.config import settings
from app.core.logging import get_logger
T = TypeVar('T')
logger = get_logger('app.core.cache.redis')
class RedisCacheBackend(CacheBackend[T]):
    def __init__(self, redis_url: Optional[str]=None, serializer: str='pickle', prefix: str='cache:', **redis_options: Any) -> None:
        self.redis_url = redis_url or settings.redis.uri
        self.serializer = serializer
        self.prefix = prefix
        self.redis_options = redis_options
        self.client: Optional[Redis] = None
    async def _get_client(self) -> Redis:
        if self.client is None:
            self.client = redis.from_url(self.redis_url, decode_responses=False, **self.redis_options)
        return self.client
    async def get(self, key: str) -> Optional[T]:
        client = await self._get_client()
        prefixed_key = f'{self.prefix}{key}'
        try:
            value = await client.get(prefixed_key)
            if value is None:
                return None
            return self._deserialize(value)
        except Exception as e:
            logger.error(f'Error getting key {key} from Redis: {str(e)}')
            return None
    async def set(self, key: str, value: T, ttl: Optional[int]=None) -> bool:
        client = await self._get_client()
        prefixed_key = f'{self.prefix}{key}'
        try:
            serialized = self._serialize(value)
            if ttl is not None:
                await client.setex(prefixed_key, ttl, serialized)
            else:
                await client.set(prefixed_key, serialized)
            return True
        except Exception as e:
            logger.error(f'Error setting key {key} in Redis: {str(e)}')
            return False
    async def delete(self, key: str) -> bool:
        client = await self._get_client()
        prefixed_key = f'{self.prefix}{key}'
        try:
            result = await client.delete(prefixed_key)
            return result > 0
        except Exception as e:
            logger.error(f'Error deleting key {key} from Redis: {str(e)}')
            return False
    async def exists(self, key: str) -> bool:
        client = await self._get_client()
        prefixed_key = f'{self.prefix}{key}'
        try:
            return await client.exists(prefixed_key) > 0
        except Exception as e:
            logger.error(f'Error checking if key {key} exists in Redis: {str(e)}')
            return False
    async def invalidate_pattern(self, pattern: str) -> int:
        client = await self._get_client()
        prefixed_pattern = f'{self.prefix}{pattern}'
        try:
            keys = await client.keys(prefixed_pattern)
            if not keys:
                return 0
            return await client.delete(*keys)
        except Exception as e:
            logger.error(f'Error invalidating pattern {pattern} in Redis: {str(e)}')
            return 0
    async def clear(self) -> bool:
        client = await self._get_client()
        pattern = f'{self.prefix}*'
        try:
            keys = await client.keys(pattern)
            if not keys:
                return True
            await client.delete(*keys)
            return True
        except Exception as e:
            logger.error(f'Error clearing Redis cache: {str(e)}')
            return False
    async def get_many(self, keys: List[str]) -> Dict[str, Optional[T]]:
        if not keys:
            return {}
        client = await self._get_client()
        prefixed_keys = [f'{self.prefix}{key}' for key in keys]
        try:
            values = await client.mget(prefixed_keys)
            result = {}
            for i, key in enumerate(keys):
                value = values[i]
                result[key] = self._deserialize(value) if value is not None else None
            return result
        except Exception as e:
            logger.error(f'Error getting multiple keys from Redis: {str(e)}')
            return {key: None for key in keys}
    async def set_many(self, mapping: Dict[str, T], ttl: Optional[int]=None) -> bool:
        if not mapping:
            return True
        client = await self._get_client()
        prefixed_mapping = {f'{self.prefix}{key}': self._serialize(value) for key, value in mapping.items()}
        try:
            pipeline = client.pipeline()
            pipeline.mset(prefixed_mapping)
            if ttl is not None:
                for key in prefixed_mapping.keys():
                    pipeline.expire(key, ttl)
            await pipeline.execute()
            return True
        except Exception as e:
            logger.error(f'Error setting multiple keys in Redis: {str(e)}')
            return False
    async def delete_many(self, keys: List[str]) -> int:
        if not keys:
            return 0
        client = await self._get_client()
        prefixed_keys = [f'{self.prefix}{key}' for key in keys]
        try:
            return await client.delete(*prefixed_keys)
        except Exception as e:
            logger.error(f'Error deleting multiple keys from Redis: {str(e)}')
            return 0
    async def incr(self, key: str, amount: int=1, default: int=0, ttl: Optional[int]=None) -> int:
        client = await self._get_client()
        prefixed_key = f'{self.prefix}{key}'
        try:
            exists = await client.exists(prefixed_key)
            if not exists:
                await client.set(prefixed_key, default)
                if ttl is not None:
                    await client.expire(prefixed_key, ttl)
                value = default
            else:
                value = await client.incrby(prefixed_key, amount)
                if ttl is not None:
                    await client.expire(prefixed_key, ttl)
            return value
        except Exception as e:
            logger.error(f'Error incrementing key {key} in Redis: {str(e)}')
            return default
    async def decr(self, key: str, amount: int=1, default: int=0, ttl: Optional[int]=None) -> int:
        return await self.incr(key, -amount, default, ttl)
    def _serialize(self, value: T) -> bytes:
        if self.serializer == 'json':
            return json.dumps(value).encode('utf-8')
        else:
            return pickle.dumps(value)
    def _deserialize(self, value: bytes) -> T:
        if value is None:
            return cast(T, None)
        if self.serializer == 'json':
            return cast(T, json.loads(value.decode('utf-8')))
        else:
            return cast(T, pickle.loads(value))