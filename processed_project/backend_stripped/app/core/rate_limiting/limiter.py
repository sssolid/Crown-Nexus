from __future__ import annotations
from app.core.metrics import MetricName
'\nRate limiter implementation.\n\nThis module provides the core rate limiting functionality, supporting both\nin-memory and Redis-based rate limiting with configurable strategies.\n'
import time
from typing import Dict, Optional, Tuple
from fastapi import Request
from app.core.config import settings
from app.logging import get_logger
from app.core.rate_limiting.models import RateLimitRule, RateLimitStrategy
from app.utils.redis_manager import get_redis_client, increment_counter
logger = get_logger('app.core.rate_limiting.limiter')
try:
    from app.core.dependency_manager import get_dependency
    HAS_METRICS = True
except ImportError:
    HAS_METRICS = False
class RateLimiter:
    def __init__(self, use_redis: Optional[bool]=None, prefix: str='ratelimit', default_rule: Optional[RateLimitRule]=None) -> None:
        self.use_redis: bool = use_redis if use_redis is not None else settings.RATE_LIMIT_STORAGE == 'redis' and settings.REDIS_HOST is not None
        self.prefix: str = prefix
        self.default_rule: RateLimitRule = default_rule or RateLimitRule(requests_per_window=settings.RATE_LIMIT_REQUESTS_PER_MINUTE * settings.RATE_LIMIT_BURST_MULTIPLIER, window_seconds=60)
        self._counters: Dict[str, Dict[float, int]] = {}
        logger.info('RateLimiter initialized', strategy=self.default_rule.strategy, limit=self.default_rule.requests_per_window, window_seconds=self.default_rule.window_seconds, use_redis=self.use_redis)
    async def is_rate_limited(self, key: str, rule: Optional[RateLimitRule]=None) -> Tuple[bool, int, int]:
        metrics_service = None
        start_time = time.monotonic()
        error = None
        try:
            if HAS_METRICS:
                try:
                    metrics_service = get_dependency('metrics_service')
                except Exception as e:
                    logger.debug(f'Could not get metrics service: {str(e)}')
            rule = rule or self.default_rule
            window_key: str = self._get_window_key(key, rule)
            if self.use_redis:
                try:
                    redis_client = await get_redis_client()
                    current_count = await increment_counter(window_key, 1, rule.window_seconds)
                    if current_count is None:
                        logger.warning('Redis rate limiting failed, using in-memory fallback')
                        return await self._check_in_memory(key, rule)
                    is_limited = current_count > rule.requests_per_window
                    if is_limited:
                        logger.warning('Rate limit exceeded (Redis)', key=key, current_count=current_count, limit=rule.requests_per_window, window_seconds=rule.window_seconds)
                    else:
                        logger.debug('Rate limit checked (Redis)', key=key, current_count=current_count, limit=rule.requests_per_window, remaining=rule.requests_per_window - current_count)
                    return (is_limited, current_count, rule.requests_per_window)
                except Exception as e:
                    logger.error(f'Redis rate limiting error: {str(e)}', exc_info=True)
                    return await self._check_in_memory(key, rule)
            return await self._check_in_memory(key, rule)
        except Exception as e:
            error = type(e).__name__
            raise
        finally:
            if metrics_service and HAS_METRICS:
                duration = time.monotonic() - start_time
                try:
                    metrics_service.observe_histogram(MetricName.RATE_LIMITING_CHECK_DURATION_SECONDS.value, duration, {'cache_backend': 'redis' if self.use_redis else 'memory', 'error_type': str(error or '')})
                    metrics_service.increment_counter('rate_limiting_checks_total', 1, {'storage': 'redis' if self.use_redis else 'memory', 'error': str(error or '')})
                except Exception as metrics_err:
                    logger.warning(f'Failed to record rate limiting metrics: {str(metrics_err)}', exc_info=metrics_err)
    async def _check_in_memory(self, key: str, rule: RateLimitRule) -> Tuple[bool, int, int]:
        now: float = time.time()
        window_start: float = now - rule.window_seconds
        if key not in self._counters:
            self._counters[key] = {}
        self._counters[key] = {ts: count for ts, count in self._counters[key].items() if ts > window_start}
        timestamp: float = now
        if timestamp in self._counters[key]:
            self._counters[key][timestamp] += 1
        else:
            self._counters[key][timestamp] = 1
        current_count: int = sum(self._counters[key].values())
        is_limited: bool = current_count > rule.requests_per_window
        if is_limited:
            logger.warning('Rate limit exceeded (memory)', key=key, current_count=current_count, limit=rule.requests_per_window, window_seconds=rule.window_seconds)
        else:
            logger.debug('Rate limit checked (memory)', key=key, current_count=current_count, limit=rule.requests_per_window, remaining=rule.requests_per_window - current_count)
        return (is_limited, current_count, rule.requests_per_window)
    def get_key_for_request(self, request: Request, rule: RateLimitRule) -> str:
        client_host = getattr(request.client, 'host', 'unknown')
        if rule.strategy == RateLimitStrategy.IP:
            return f'{self.prefix}:ip:{client_host}'
        if rule.strategy == RateLimitStrategy.USER:
            user_id: str = getattr(request.state, 'user_id', 'anonymous')
            return f'{self.prefix}:user:{user_id}'
        if rule.strategy == RateLimitStrategy.COMBINED:
            user_id: str = getattr(request.state, 'user_id', 'anonymous')
            return f'{self.prefix}:combined:{client_host}:{user_id}'
        return f'{self.prefix}:ip:{client_host}'
    def _get_window_key(self, key: str, rule: RateLimitRule) -> str:
        window: int = int(time.time() / rule.window_seconds)
        return f'{key}:{window}'