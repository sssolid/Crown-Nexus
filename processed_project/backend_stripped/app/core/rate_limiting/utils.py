from __future__ import annotations
import time
from typing import Tuple
from app.logging import get_logger
from app.utils.redis_manager import get_key, set_key
logger = get_logger('app.core.rate_limiting.utils')
async def check_rate_limit(key: str, max_requests: int, window_seconds: int) -> Tuple[bool, int, int]:
    rate_limit_prefix = 'rate_limit:'
    window_start = int(time.time() / window_seconds) * window_seconds
    cache_key = f'{rate_limit_prefix}{key}:{window_start}'
    current = await get_key(cache_key)
    if current is None:
        count = 1
        await set_key(cache_key, count, window_seconds)
        reset_seconds = window_seconds
        return (False, count, reset_seconds)
    count = int(current) + 1
    remaining_ttl = await get_ttl(cache_key)
    if remaining_ttl > 0:
        await set_key(cache_key, count, remaining_ttl)
        reset_seconds = remaining_ttl
    else:
        count = 1
        await set_key(cache_key, count, window_seconds)
        reset_seconds = window_seconds
    is_limited = count > max_requests
    if is_limited:
        logger.warning('Rate limit exceeded', extra={'key': key, 'count': count, 'max_requests': max_requests, 'reset_seconds': reset_seconds})
    return (is_limited, count, reset_seconds)
async def get_ttl(key: str) -> int:
    try:
        import redis.asyncio as redis
        from app.core.cache.manager import get_redis_pool
        redis_conn = redis.Redis(connection_pool=get_redis_pool())
        ttl = await redis_conn.ttl(key)
        if ttl < 0:
            return 0
        return ttl
    except Exception as e:
        logger.error(f'Error getting TTL: {str(e)}')
        return 0