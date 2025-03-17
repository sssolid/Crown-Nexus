# /backend/app/core/cache/redis.py
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

logger = get_logger("app.core.cache.redis")

class RedisCacheBackend(CacheBackend[T]):
    """Redis cache backend implementation.
    
    This backend stores cached values in Redis, with optional TTL expiration.
    It's suitable for production environments where persistence and distributed
    caching are required.
    """
    
    def __init__(
        self,
        redis_url: Optional[str] = None,
        serializer: str = "pickle",
        prefix: str = "cache:",
        **redis_options: Any
    ) -> None:
        """Initialize the Redis cache backend.
        
        Args:
            redis_url: Redis connection URL
            serializer: Serializer to use (pickle or json)
            prefix: Key prefix for all cache keys
            **redis_options: Additional Redis client options
        """
        self.redis_url = redis_url or settings.redis.uri
        self.serializer = serializer
        self.prefix = prefix
        self.redis_options = redis_options
        self.client: Optional[Redis] = None
        
    async def _get_client(self) -> Redis:
        """Get the Redis client instance.
        
        Returns:
            Redis: Redis client
        """
        if self.client is None:
            self.client = redis.from_url(
                self.redis_url,
                decode_responses=False,
                **self.redis_options
            )
            
        return self.client
    
    async def get(self, key: str) -> Optional[T]:
        """Get a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            Optional[T]: Cached value or None if not found
        """
        client = await self._get_client()
        prefixed_key = f"{self.prefix}{key}"
        
        try:
            # Get value from Redis
            value = await client.get(prefixed_key)
            
            # Return None if value not found
            if value is None:
                return None
                
            # Deserialize value
            return self._deserialize(value)
        except Exception as e:
            logger.error(f"Error getting key {key} from Redis: {str(e)}")
            return None
    
    async def set(
        self,
        key: str,
        value: T,
        ttl: Optional[int] = None
    ) -> bool:
        """Set a value in the cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds
            
        Returns:
            bool: True if successful, False otherwise
        """
        client = await self._get_client()
        prefixed_key = f"{self.prefix}{key}"
        
        try:
            # Serialize value
            serialized = self._serialize(value)
            
            # Set value in Redis with TTL if provided
            if ttl is not None:
                await client.setex(prefixed_key, ttl, serialized)
            else:
                await client.set(prefixed_key, serialized)
                
            return True
        except Exception as e:
            logger.error(f"Error setting key {key} in Redis: {str(e)}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            bool: True if key was deleted, False if key wasn't found
        """
        client = await self._get_client()
        prefixed_key = f"{self.prefix}{key}"
        
        try:
            # Delete key from Redis
            result = await client.delete(prefixed_key)
            return result > 0
        except Exception as e:
            logger.error(f"Error deleting key {key} from Redis: {str(e)}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if a key exists in the cache.
        
        Args:
            key: Cache key
            
        Returns:
            bool: True if key exists, False otherwise
        """
        client = await self._get_client()
        prefixed_key = f"{self.prefix}{key}"
        
        try:
            # Check if key exists in Redis
            return await client.exists(prefixed_key) > 0
        except Exception as e:
            logger.error(f"Error checking if key {key} exists in Redis: {str(e)}")
            return False
    
    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching a pattern.
        
        Args:
            pattern: Key pattern to match
            
        Returns:
            int: Number of keys invalidated
        """
        client = await self._get_client()
        prefixed_pattern = f"{self.prefix}{pattern}"
        
        try:
            # Find keys matching pattern
            keys = await client.keys(prefixed_pattern)
            
            if not keys:
                return 0
                
            # Delete matching keys
            return await client.delete(*keys)
        except Exception as e:
            logger.error(f"Error invalidating pattern {pattern} in Redis: {str(e)}")
            return 0
    
    async def clear(self) -> bool:
        """Clear all cached values.
        
        Returns:
            bool: True if successful, False otherwise
        """
        client = await self._get_client()
        pattern = f"{self.prefix}*"
        
        try:
            # Find all keys with prefix
            keys = await client.keys(pattern)
            
            if not keys:
                return True
                
            # Delete all keys
            await client.delete(*keys)
            return True
        except Exception as e:
            logger.error(f"Error clearing Redis cache: {str(e)}")
            return False
    
    async def get_many(self, keys: List[str]) -> Dict[str, Optional[T]]:
        """Get multiple values from the cache.
        
        Args:
            keys: List of cache keys
            
        Returns:
            Dict[str, Optional[T]]: Dictionary of key-value pairs
        """
        if not keys:
            return {}
            
        client = await self._get_client()
        prefixed_keys = [f"{self.prefix}{key}" for key in keys]
        
        try:
            # Get multiple values from Redis
            values = await client.mget(prefixed_keys)
            
            # Deserialize values and create result dictionary
            result = {}
            for i, key in enumerate(keys):
                value = values[i]
                result[key] = self._deserialize(value) if value is not None else None
                
            return result
        except Exception as e:
            logger.error(f"Error getting multiple keys from Redis: {str(e)}")
            return {key: None for key in keys}
    
    async def set_many(
        self,
        mapping: Dict[str, T],
        ttl: Optional[int] = None
    ) -> bool:
        """Set multiple values in the cache.
        
        Args:
            mapping: Dictionary of key-value pairs to cache
            ttl: Time-to-live in seconds
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not mapping:
            return True
            
        client = await self._get_client()
        prefixed_mapping = {
            f"{self.prefix}{key}": self._serialize(value)
            for key, value in mapping.items()
        }
        
        try:
            # Use pipeline for better performance
            pipeline = client.pipeline()
            
            # Set multiple values
            pipeline.mset(prefixed_mapping)
            
            # Set TTL if provided
            if ttl is not None:
                for key in prefixed_mapping.keys():
                    pipeline.expire(key, ttl)
                    
            # Execute pipeline
            await pipeline.execute()
            
            return True
        except Exception as e:
            logger.error(f"Error setting multiple keys in Redis: {str(e)}")
            return False
    
    async def delete_many(self, keys: List[str]) -> int:
        """Delete multiple values from the cache.
        
        Args:
            keys: List of cache keys
            
        Returns:
            int: Number of keys deleted
        """
        if not keys:
            return 0
            
        client = await self._get_client()
        prefixed_keys = [f"{self.prefix}{key}" for key in keys]
        
        try:
            # Delete multiple keys from Redis
            return await client.delete(*prefixed_keys)
        except Exception as e:
            logger.error(f"Error deleting multiple keys from Redis: {str(e)}")
            return 0
    
    async def incr(
        self,
        key: str,
        amount: int = 1,
        default: int = 0,
        ttl: Optional[int] = None
    ) -> int:
        """Increment a counter in the cache.
        
        Args:
            key: Cache key
            amount: Amount to increment by
            default: Default value if key doesn't exist
            ttl: Time-to-live in seconds
            
        Returns:
            int: New counter value
        """
        client = await self._get_client()
        prefixed_key = f"{self.prefix}{key}"
        
        try:
            # Check if key exists
            exists = await client.exists(prefixed_key)
            
            if not exists:
                # Set default value
                await client.set(prefixed_key, default)
                if ttl is not None:
                    await client.expire(prefixed_key, ttl)
                # Set initial value
                value = default
            else:
                # Increment value
                value = await client.incrby(prefixed_key, amount)
                # Refresh TTL if provided
                if ttl is not None:
                    await client.expire(prefixed_key, ttl)
                    
            return value
        except Exception as e:
            logger.error(f"Error incrementing key {key} in Redis: {str(e)}")
            return default
    
    async def decr(
        self,
        key: str,
        amount: int = 1,
        default: int = 0,
        ttl: Optional[int] = None
    ) -> int:
        """Decrement a counter in the cache.
        
        Args:
            key: Cache key
            amount: Amount to decrement by
            default: Default value if key doesn't exist
            ttl: Time-to-live in seconds
            
        Returns:
            int: New counter value
        """
        return await self.incr(key, -amount, default, ttl)
    
    def _serialize(self, value: T) -> bytes:
        """Serialize a value for storage in Redis.
        
        Args:
            value: Value to serialize
            
        Returns:
            bytes: Serialized value
        """
        if self.serializer == "json":
            return json.dumps(value).encode("utf-8")
        else:
            return pickle.dumps(value)
    
    def _deserialize(self, value: bytes) -> T:
        """Deserialize a value from Redis.
        
        Args:
            value: Serialized value
            
        Returns:
            T: Deserialized value
        """
        if value is None:
            return cast(T, None)
            
        if self.serializer == "json":
            return cast(T, json.loads(value.decode("utf-8")))
        else:
            return cast(T, pickle.loads(value))
