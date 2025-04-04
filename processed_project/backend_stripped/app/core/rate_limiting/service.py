from __future__ import annotations
'\nRate limiting service implementation.\n\nThis module provides a service wrapper around the rate limiting system,\nmaking it available through the dependency manager.\n'
from typing import Dict, Optional, Tuple
from fastapi import Request
from app.logging import get_logger
from app.core.rate_limiting.limiter import RateLimiter
from app.core.rate_limiting.models import RateLimitRule, RateLimitStrategy
from app.core.config import settings
logger = get_logger('app.core.rate_limiting.service')
class RateLimitingService:
    def __init__(self) -> None:
        self._initialized = False
        self._limiter: Optional[RateLimiter] = None
    async def initialize(self) -> None:
        if self._initialized:
            logger.debug('Rate limiting service already initialized, skipping')
            return
        logger.info('Initializing rate limiting service')
        self._limiter = RateLimiter(use_redis=settings.RATE_LIMIT_STORAGE == 'redis', prefix='ratelimit', default_rule=RateLimitRule(requests_per_window=settings.RATE_LIMIT_REQUESTS_PER_MINUTE, window_seconds=60))
        self._initialized = True
        logger.info('Rate limiting service initialized')
    async def shutdown(self) -> None:
        if not self._initialized:
            return
        logger.info('Shutting down rate limiting service')
        self._limiter = None
        self._initialized = False
        logger.info('Rate limiting service shut down')
    async def is_rate_limited(self, key: str, rule: Optional[RateLimitRule]=None) -> Tuple[bool, int, int]:
        self._ensure_initialized()
        return await self._limiter.is_rate_limited(key, rule)
    def get_key_for_request(self, request: Request, rule: RateLimitRule) -> str:
        self._ensure_initialized()
        return self._limiter.get_key_for_request(request, rule)
    def _ensure_initialized(self) -> None:
        if not self._initialized or self._limiter is None:
            from app.core.rate_limiting.exceptions import RateLimitingServiceException
            logger.error('Rate limiting service accessed before initialization')
            raise RateLimitingServiceException('Rate limiting service not initialized')
_rate_limiting_service: Optional[RateLimitingService] = None
def get_rate_limiting_service() -> RateLimitingService:
    global _rate_limiting_service
    if _rate_limiting_service is None:
        _rate_limiting_service = RateLimitingService()
    return _rate_limiting_service