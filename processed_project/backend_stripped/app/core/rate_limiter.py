from __future__ import annotations
import asyncio
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
from fastapi import HTTPException, Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.core.exceptions import RateLimitException
from app.core.logging import get_logger
from app.utils.redis_manager import get_redis_client, increment_counter
logger = get_logger('app.core.rate_limiter')
class RateLimitStrategy(str, Enum):
    IP = 'ip'
    USER = 'user'
    COMBINED = 'combined'
@dataclass
class RateLimitRule:
    requests_per_window: int
    window_seconds: int
    strategy: RateLimitStrategy = RateLimitStrategy.IP
    burst_multiplier: float = 1.5
    path_pattern: Optional[str] = None
    exclude_paths: List[str] = field(default_factory=list)
class RateLimiter:
    def __init__(self, use_redis: Optional[bool]=None, prefix: str='ratelimit', default_rule: Optional[RateLimitRule]=None) -> None:
        self.use_redis: bool = use_redis if use_redis is not None else settings.security.RATE_LIMIT_STORAGE == 'redis' and settings.redis.REDIS_HOST is not None
        self.prefix: str = prefix
        self.default_rule: RateLimitRule = default_rule or RateLimitRule(requests_per_window=settings.security.RATE_LIMIT_REQUESTS_PER_MINUTE, window_seconds=60)
        self._counters: Dict[str, Dict[float, int]] = {}
        logger.info(f'RateLimiter initialized with strategy={self.default_rule.strategy}, limit={self.default_rule.requests_per_window} requests per {self.default_rule.window_seconds}s')
    async def is_rate_limited(self, key: str, rule: Optional[RateLimitRule]=None) -> Tuple[bool, int, int]:
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
                return (is_limited, current_count, rule.requests_per_window)
            except Exception as e:
                logger.error(f'Redis rate limiting error: {str(e)}')
                return await self._check_in_memory(key, rule)
        return await self._check_in_memory(key, rule)
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
        return (is_limited, current_count, rule.requests_per_window)
    def get_key_for_request(self, request: Request, rule: RateLimitRule) -> str:
        if rule.strategy == RateLimitStrategy.IP:
            return f'{self.prefix}:ip:{request.client.host}'
        if rule.strategy == RateLimitStrategy.USER:
            user_id: str = getattr(request.state, 'user_id', 'anonymous')
            return f'{self.prefix}:user:{user_id}'
        if rule.strategy == RateLimitStrategy.COMBINED:
            user_id: str = getattr(request.state, 'user_id', 'anonymous')
            return f'{self.prefix}:combined:{request.client.host}:{user_id}'
        return f'{self.prefix}:ip:{request.client.host}'
    def _get_window_key(self, key: str, rule: RateLimitRule) -> str:
        window: int = int(time.time() / rule.window_seconds)
        return f'{key}:{window}'
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: Any, rules: Optional[List[RateLimitRule]]=None, use_redis: bool=True, enable_headers: bool=True, block_exceeding_requests: bool=True) -> None:
        super().__init__(app)
        self.rules: List[RateLimitRule] = rules or [RateLimitRule(requests_per_window=settings.security.RATE_LIMIT_REQUESTS_PER_MINUTE, window_seconds=60)]
        self.rate_limiter: RateLimiter = RateLimiter(use_redis=use_redis)
        self.enable_headers: bool = enable_headers
        self.block_exceeding_requests: bool = block_exceeding_requests
        logger.info('RateLimitMiddleware initialized')
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        path: str = request.url.path
        if any((path.startswith(excluded) for rule in self.rules for excluded in rule.exclude_paths)):
            return await call_next(request)
        applicable_rules: List[RateLimitRule] = [rule for rule in self.rules if rule.path_pattern is None or path.startswith(rule.path_pattern)]
        if not applicable_rules:
            applicable_rules = [self.rules[0]]
        is_limited: bool = False
        headers: Dict[str, str] = {}
        for rule in applicable_rules:
            key: str = self.rate_limiter.get_key_for_request(request, rule)
            limited, count, limit = await self.rate_limiter.is_rate_limited(key, rule)
            if limited:
                is_limited = True
            if self.enable_headers:
                headers['X-RateLimit-Limit'] = str(limit)
                headers['X-RateLimit-Remaining'] = str(max(0, limit - count))
                headers['X-RateLimit-Reset'] = str(rule.window_seconds)
        if is_limited and self.block_exceeding_requests:
            headers['Retry-After'] = str(applicable_rules[0].window_seconds)
            logger.warning(f'Rate limit exceeded for {request.client.host}')
            raise RateLimitException(message='Rate limit exceeded', details={'ip': request.client.host}, headers=headers)
        response: Response = await call_next(request)
        if self.enable_headers:
            for header, value in headers.items():
                response.headers[header] = value
        return response