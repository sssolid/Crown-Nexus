# backend/app/services/cache/redis.py
"""Redis cache backend implementation.

This module provides a Redis implementation of the CacheBackend protocol,
suitable for production environments with distributed caching needs.
"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Union

import redis.asyncio as redis
from redis.asyncio.client import Redis
from redis.exceptions import RedisError

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class RedisCacheBackend:
    """Redis cache backend implementation."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        username: Optional[str] = None,
        password: Optional[str] = None,
        prefix: str = "cache:",
        default_ttl: int = 300,
        socket_timeout: int = 5,
        decode_responses: bool = True,
    ):
        """
        Initialize the Redis cache backend.

        Args:
            host: Redis host
            port: Redis port
            db: Redis database number
            username: Optional Redis username
            password: Optional Redis password
            prefix: Key prefix for all cache keys
            default_ttl: Default time-to-live in seconds
            socket_timeout: Socket timeout in seconds
            decode_responses: Whether to decode responses to strings
        """
        self.host = host
        self.port = port
        self.db = db
        self.username = username
        self.password = password
        self.prefix = prefix
        self.default_ttl = default_ttl
        self.socket_timeout = socket_timeout
        self.decode_responses = decode_responses

        # Client will be initialized in connect()
        self.client: Optional[Redis] = None

        logger.debug(
            f"RedisCacheBackend initialized (host={host}, port={port}, db={db})"
        )

    async def connect(self) -> None:
        """Connect to Redis server and initialize client."""
        if self.client is not None:
            return

        try:
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                username=self.username,
                password=self.password,
                socket_timeout=self.socket_timeout,
                decode_responses=self.decode_responses,
            )

            # Test connection
            await self.ping()
            logger.info(f"Connected to Redis: {self.host}:{self.port}/{self.db}")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {str(e)}")
            if self.client:
                await self.client.close()
                self.client = None
            raise

    async def _ensure_connected(self) -> None:
        """Ensure Redis client is connected."""
        if self.client is None:
            await self.connect()

    def _prefix_key(self, key: str) -> str:
        """Add prefix to a cache key."""
        return f"{self.prefix}{key}"

    async def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the cache.

        Args:
            key: Cache key
            default: Default value if key doesn't exist

        Returns:
            Cached value or default
        """
        try:
            await self._ensure_connected()
            prefixed_key = self._prefix_key(key)

            value = await self.client.get(prefixed_key)
            if value is None:
                return default

            try:
                # Try to deserialize JSON
                return json.loads(value)
            except (TypeError, json.JSONDecodeError):
                # Not JSON, return as is
                return value
        except Exception as e:
            logger.error(f"Redis get error for key {key}: {str(e)}")
            return default

    async def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """
        Set a value in the cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds

        Returns:
            True if successful, False otherwise
        """
        try:
            await self._ensure_connected()
            prefixed_key = self._prefix_key(key)

            # Serialize complex types to JSON
            if not isinstance(value, (str, int, float, bytes)):
                value = json.dumps(value)

            # Use provided TTL or default
            seconds = ttl if ttl is not None else self.default_ttl

            result = await self.client.set(prefixed_key, value, ex=seconds)
            return result is True
        except Exception as e:
            logger.error(f"Redis set error for key {key}: {str(e)}")
            return False

    async def delete(self, key: str) -> bool:
        """
        Delete a value from the cache.

        Args:
            key: Cache key

        Returns:
            True if key was deleted, False otherwise
        """
        try:
            await self._ensure_connected()
            prefixed_key = self._prefix_key(key)

            result = await self.client.delete(prefixed_key)
            return result > 0
        except Exception as e:
            logger.error(f"Redis delete error for key {key}: {str(e)}")
            return False

    async def exists(self, key: str) -> bool:
        """
        Check if a key exists in the cache.

        Args:
            key: Cache key

        Returns:
            True if key exists, False otherwise
        """
        try:
            await self._ensure_connected()
            prefixed_key = self._prefix_key(key)

            result = await self.client.exists(prefixed_key)
            return result > 0
        except Exception as e:
            logger.error(f"Redis exists error for key {key}: {str(e)}")
            return False

    async def clear(self) -> bool:
        """
        Clear all cached values with the current prefix.

        Returns:
            True if successful, False otherwise
        """
        try:
            await self._ensure_connected()

            # Find all keys with prefix
            pattern = f"{self.prefix}*"
            keys = await self.client.keys(pattern)

            if keys:
                # Delete all matched keys
                await self.client.delete(*keys)
                logger.debug(f"Cleared {len(keys)} keys with prefix {self.prefix}")

            return True
        except Exception as e:
            logger.error(f"Redis clear error: {str(e)}")
            return False

    async def get_many(self, keys: List[str]) -> Dict[str, Any]:
        """
        Get multiple values from the cache.

        Args:
            keys: List of cache keys

        Returns:
            Dictionary of key-value pairs for found keys
        """
        if not keys:
            return {}

        try:
            await self._ensure_connected()
            prefixed_keys = [self._prefix_key(key) for key in keys]

            # Use Redis MGET for efficient multi-get
            values = await self.client.mget(prefixed_keys)

            # Process results
            result = {}
            for i, value in enumerate(values):
                if value is not None:
                    original_key = keys[i]
                    try:
                        # Try to deserialize JSON
                        result[original_key] = json.loads(value)
                    except (TypeError, json.JSONDecodeError):
                        # Not JSON, store as is
                        result[original_key] = value

            return result
        except Exception as e:
            logger.error(f"Redis get_many error: {str(e)}")
            return {}

    async def set_many(self, mapping: Dict[str, Any], ttl: int = 300) -> bool:
        """
        Set multiple values in the cache.

        Args:
            mapping: Dictionary of key-value pairs
            ttl: Time-to-live in seconds

        Returns:
            True if successful, False otherwise
        """
        if not mapping:
            return True

        try:
            await self._ensure_connected()
            pipeline = self.client.pipeline()

            # Prepare values
            for key, value in mapping.items():
                prefixed_key = self._prefix_key(key)

                # Serialize complex types to JSON
                if not isinstance(value, (str, int, float, bytes)):
                    value = json.dumps(value)

                # Use provided TTL or default
                seconds = ttl if ttl is not None else self.default_ttl

                pipeline.set(prefixed_key, value, ex=seconds)

            # Execute pipeline
            await pipeline.execute()
            return True
        except Exception as e:
            logger.error(f"Redis set_many error: {str(e)}")
            return False

    async def delete_many(self, keys: List[str]) -> int:
        """
        Delete multiple values from the cache.

        Args:
            keys: List of cache keys

        Returns:
            Number of keys deleted
        """
        if not keys:
            return 0

        try:
            await self._ensure_connected()
            prefixed_keys = [self._prefix_key(key) for key in keys]

            # Use Redis DEL for efficient multi-delete
            result = await self.client.delete(*prefixed_keys)
            return result
        except Exception as e:
            logger.error(f"Redis delete_many error: {str(e)}")
            return 0

    async def incr(self, key: str, amount: int = 1) -> int:
        """
        Increment a value in the cache.

        Args:
            key: Cache key
            amount: Amount to increment by

        Returns:
            New value
        """
        try:
            await self._ensure_connected()
            prefixed_key = self._prefix_key(key)

            # Use Redis INCRBY
            result = await self.client.incrby(prefixed_key, amount)
            return result
        except Exception as e:
            logger.error(f"Redis incr error for key {key}: {str(e)}")
            return 0

    async def decr(self, key: str, amount: int = 1) -> int:
        """
        Decrement a value in the cache.

        Args:
            key: Cache key
            amount: Amount to decrement by

        Returns:
            New value
        """
        return await self.incr(key, -amount)

    async def ttl(self, key: str) -> Optional[int]:
        """
        Get the remaining time-to-live for a key.

        Args:
            key: Cache key

        Returns:
            Remaining TTL in seconds, or None if key doesn't exist
        """
        try:
            await self._ensure_connected()
            prefixed_key = self._prefix_key(key)

            # Use Redis TTL command
            result = await self.client.ttl(prefixed_key)

            # Redis returns -2 if key doesn't exist, -1 if no expiry
            if result < 0:
                return None

            return result
        except Exception as e:
            logger.error(f"Redis ttl error for key {key}: {str(e)}")
            return None

    async def expire(self, key: str, ttl: int) -> bool:
        """
        Set a new expiration time for a key.

        Args:
            key: Cache key
            ttl: New time-to-live in seconds

        Returns:
            True if successful, False otherwise
        """
        try:
            await self._ensure_connected()
            prefixed_key = self._prefix_key(key)

            # Use Redis EXPIRE command
            result = await self.client.expire(prefixed_key, ttl)
            return result > 0
        except Exception as e:
            logger.error(f"Redis expire error for key {key}: {str(e)}")
            return False

    async def ping(self) -> bool:
        """
        Check if the Redis server is available.

        Returns:
            True if available, False otherwise
        """
        try:
            if self.client is None:
                await self.connect()

            result = await self.client.ping()
            return result == "PONG" or result is True
        except Exception as e:
            logger.error(f"Redis ping error: {str(e)}")
            return False

    async def close(self) -> None:
        """Close the Redis client and release resources."""
        if self.client:
            await self.client.close()
            self.client = None
            logger.debug("Redis client closed")
