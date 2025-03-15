from __future__ import annotations
import json
import logging
from typing import Any, Dict, List, Optional, TypeVar, cast
import redis.asyncio as redis
from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool
from app.core.config import settings
logger = logging.getLogger(__name__)
T = TypeVar('T')
_redis_pool: Optional[ConnectionPool] = None
async def get_redis_pool() -> ConnectionPool:
    global _redis_pool
    if _redis_pool is None:
        _redis_pool = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, password=settings.REDIS_PASSWORD, decode_responses=True, max_connections=settings.REDIS_MAX_CONNECTIONS)
        logger.info(f'Created Redis connection pool to {settings.REDIS_HOST}:{settings.REDIS_PORT}')
    return _redis_pool
async def get_redis_client() -> Redis:
    pool = await get_redis_pool()
    return redis.Redis(connection_pool=pool)
async def set_key(key: str, value: Any, ttl: Optional[int]=None) -> bool:
    try:
        client = await get_redis_client()
        serialized = json.dumps(value)
        if ttl:
            await client.setex(key, ttl, serialized)
        else:
            await client.set(key, serialized)
        return True
    except Exception as e:
        logger.error(f'Redis set error: {e}')
        return False
async def get_key(key: str, default: Optional[T]=None) -> Optional[T]:
    try:
        client = await get_redis_client()
        value = await client.get(key)
        if value is None:
            return default
        return cast(T, json.loads(value))
    except Exception as e:
        logger.error(f'Redis get error: {e}')
        return default
async def delete_key(key: str) -> bool:
    try:
        client = await get_redis_client()
        return await client.delete(key) > 0
    except Exception as e:
        logger.error(f'Redis delete error: {e}')
        return False
async def increment_counter(key: str, amount: int=1, ttl: Optional[int]=None) -> Optional[int]:
    try:
        client = await get_redis_client()
        value = await client.incrby(key, amount)
        if ttl:
            await client.expire(key, ttl)
        return value
    except Exception as e:
        logger.error(f'Redis increment error: {e}')
        return None
async def rate_limit_check(key: str, limit: int, window: int) -> tuple[bool, int]:
    try:
        client = await get_redis_client()
        current = await client.get(key)
        if current is None:
            await client.setex(key, window, 1)
            return (False, 1)
        count = await client.incr(key)
        if count > limit:
            return (True, count)
        return (False, count)
    except Exception as e:
        logger.error(f'Redis rate limit error: {e}')
        return (False, 0)
async def publish_message(channel: str, message: Dict[str, Any]) -> bool:
    try:
        client = await get_redis_client()
        receivers = await client.publish(channel, json.dumps(message))
        return receivers > 0
    except Exception as e:
        logger.error(f'Redis publish error: {e}')
        return False
async def cache_get_or_set(key: str, callback: callable, ttl: int=3600, force_refresh: bool=False) -> Any:
    if not force_refresh:
        cached = await get_key(key)
        if cached is not None:
            return cached
    value = await callback()
    await set_key(key, value, ttl)
    return value