# backend/app/utils/redis_manager.py
"""
Redis connection manager.

This module provides utilities for Redis connections and operations:
- Connection pooling
- Common Redis operations
- Caching abstractions
- Pub/Sub functionality

These utilities provide a consistent interface for Redis usage
throughout the application.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional, TypeVar, cast

import redis.asyncio as redis
from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool

from app.core.config import settings


logger = logging.getLogger(__name__)

# Type variable for the return value
T = TypeVar('T')

# Redis connection pool
_redis_pool: Optional[ConnectionPool] = None


async def get_redis_pool() -> ConnectionPool:
    """
    Get or create the Redis connection pool.
    
    Returns:
        ConnectionPool: Redis connection pool
    """
    global _redis_pool
    
    if _redis_pool is None:
        _redis_pool = redis.ConnectionPool(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
            max_connections=settings.REDIS_MAX_CONNECTIONS,
        )
        logger.info(f"Created Redis connection pool to {settings.REDIS_HOST}:{settings.REDIS_PORT}")
    
    return _redis_pool


async def get_redis_client() -> Redis:
    """
    Get a Redis client using the connection pool.
    
    Returns:
        Redis: Redis client
    """
    pool = await get_redis_pool()
    return redis.Redis(connection_pool=pool)


async def set_key(key: str, value: Any, ttl: Optional[int] = None) -> bool:
    """
    Set a value in Redis.
    
    Args:
        key: Redis key
        value: Value to store (will be JSON serialized)
        ttl: Time-to-live in seconds (optional)
        
    Returns:
        bool: Success status
    """
    try:
        client = await get_redis_client()
        serialized = json.dumps(value)
        if ttl:
            await client.setex(key, ttl, serialized)
        else:
            await client.set(key, serialized)
        return True
    except Exception as e:
        logger.error(f"Redis set error: {e}")
        return False


async def get_key(key: str, default: Optional[T] = None) -> Optional[T]:
    """
    Get a value from Redis.
    
    Args:
        key: Redis key
        default: Default value if key doesn't exist
        
    Returns:
        Any: Deserialized value or default
    """
    try:
        client = await get_redis_client()
        value = await client.get(key)
        if value is None:
            return default
        return cast(T, json.loads(value))
    except Exception as e:
        logger.error(f"Redis get error: {e}")
        return default


async def delete_key(key: str) -> bool:
    """
    Delete a key from Redis.
    
    Args:
        key: Redis key
        
    Returns:
        bool: Success status
    """
    try:
        client = await get_redis_client()
        return await client.delete(key) > 0
    except Exception as e:
        logger.error(f"Redis delete error: {e}")
        return False


async def increment_counter(key: str, amount: int = 1, ttl: Optional[int] = None) -> Optional[int]:
    """
    Increment a counter in Redis.
    
    Args:
        key: Redis key
        amount: Amount to increment by
        ttl: Time-to-live in seconds (optional)
        
    Returns:
        Optional[int]: New counter value or None on error
    """
    try:
        client = await get_redis_client()
        value = await client.incrby(key, amount)
        if ttl:
            await client.expire(key, ttl)
        return value
    except Exception as e:
        logger.error(f"Redis increment error: {e}")
        return None


async def rate_limit_check(
    key: str, 
    limit: int, 
    window: int
) -> tuple[bool, int]:
    """
    Check if a rate limit has been exceeded.
    
    Args:
        key: Redis key for the rate limit
        limit: Maximum number of operations
        window: Time window in seconds
        
    Returns:
        tuple[bool, int]: (is_limited, current_count)
    """
    try:
        client = await get_redis_client()
        current = await client.get(key)
        
        # Initialize counter if it doesn't exist
        if current is None:
            await client.setex(key, window, 1)
            return False, 1
        
        # Increment counter
        count = await client.incr(key)
        
        # Check if limit exceeded
        if count > limit:
            return True, count
        
        return False, count
    except Exception as e:
        logger.error(f"Redis rate limit error: {e}")
        # Fail open to avoid blocking legitimate requests
        return False, 0


async def publish_message(channel: str, message: Dict[str, Any]) -> bool:
    """
    Publish a message to a Redis channel.
    
    Args:
        channel: Redis channel name
        message: Message data to publish
        
    Returns:
        bool: Success status
    """
    try:
        client = await get_redis_client()
        receivers = await client.publish(channel, json.dumps(message))
        return receivers > 0
    except Exception as e:
        logger.error(f"Redis publish error: {e}")
        return False


async def cache_get_or_set(
    key: str,
    callback: callable,
    ttl: int = 3600,
    force_refresh: bool = False
) -> Any:
    """
    Get a value from cache or compute and store it.
    
    Args:
        key: Cache key
        callback: Function to compute the value if not cached
        ttl: Time-to-live in seconds
        force_refresh: Force cache refresh
        
    Returns:
        Any: Cached or computed value
    """
    if not force_refresh:
        # Try to get from cache
        cached = await get_key(key)
        if cached is not None:
            return cached
    
    # Compute value
    value = await callback()
    
    # Store in cache
    await set_key(key, value, ttl)
    
    return value
