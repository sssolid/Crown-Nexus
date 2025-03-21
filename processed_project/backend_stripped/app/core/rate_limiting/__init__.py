from __future__ import annotations
from app.core.rate_limiting.models import RateLimitRule, RateLimitStrategy
from app.core.rate_limiting.limiter import RateLimiter
from app.core.rate_limiting.utils import check_rate_limit, get_ttl
from app.core.logging import get_logger
logger = get_logger('app.core.rate_limiting')
async def initialize() -> None:
    logger.info('Initializing rate limiting system')
async def shutdown() -> None:
    logger.info('Shutting down rate limiting system')
__all__ = ['RateLimitRule', 'RateLimitStrategy', 'initialize', 'shutdown', 'RateLimiter', 'check_rate_limit', 'get_ttl']