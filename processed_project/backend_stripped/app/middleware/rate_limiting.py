from __future__ import annotations
'\nRate limiting middleware for FastAPI applications.\n\nThis middleware applies rate limiting to incoming requests based on configurable\nrules and strategies. It supports both Redis-backed and in-memory rate limiting.\n'
import time
from typing import Any, Callable, Dict, List, Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.core.exceptions import RateLimitException
from app.logging import get_logger
from app.core.rate_limiting.limiter import RateLimiter
from app.core.rate_limiting.models import RateLimitRule
from app.core.rate_limiting.exceptions import RateLimitExceededException
logger = get_logger('app.middleware.rate_limiting')
try:
    from app.core.dependency_manager import get_dependency
    HAS_METRICS = True
except ImportError:
    HAS_METRICS = False
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: Any, rules: Optional[List[RateLimitRule]]=None, use_redis: bool=True, enable_headers: bool=True, block_exceeding_requests: bool=True) -> None:
        super().__init__(app)
        self.rules: List[RateLimitRule] = rules or [RateLimitRule(requests_per_window=settings.RATE_LIMIT_REQUESTS_PER_MINUTE, window_seconds=60)]
        self.rate_limiter: RateLimiter = RateLimiter(use_redis=use_redis)
        self.enable_headers: bool = enable_headers
        self.block_exceeding_requests: bool = block_exceeding_requests
        logger.info('RateLimitMiddleware initialized', rules_count=len(self.rules), use_redis=use_redis, enable_headers=enable_headers, block_exceeding_requests=block_exceeding_requests)
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        metrics_service = None
        start_time = time.time()
        is_limited = False
        try:
            if HAS_METRICS:
                try:
                    metrics_service = get_dependency('metrics_service')
                except Exception as e:
                    logger.debug(f'Could not get metrics service: {str(e)}')
            path: str = request.url.path
            if any((path.startswith(excluded) for rule in self.rules for excluded in rule.exclude_paths)):
                return await call_next(request)
            applicable_rules: List[RateLimitRule] = [rule for rule in self.rules if rule.path_pattern is None or path.startswith(rule.path_pattern)]
            if not applicable_rules:
                applicable_rules = [self.rules[0]]
            is_limited = False
            headers: Dict[str, str] = {}
            client_host = getattr(request.client, 'host', 'unknown')
            for rule in applicable_rules:
                key: str = self.rate_limiter.get_key_for_request(request, rule)
                limited, count, limit = await self.rate_limiter.is_rate_limited(key, rule)
                if limited:
                    is_limited = True
                    logger.warning('Rate limit exceeded', client_host=client_host, path=path, key=key, count=count, limit=limit)
                if self.enable_headers:
                    headers['X-RateLimit-Limit'] = str(limit)
                    headers['X-RateLimit-Remaining'] = str(max(0, limit - count))
                    headers['X-RateLimit-Reset'] = str(rule.window_seconds)
            if is_limited and self.block_exceeding_requests:
                headers['Retry-After'] = str(applicable_rules[0].window_seconds)
                if metrics_service and HAS_METRICS:
                    try:
                        metrics_service.increment_counter('rate_limit_exceeded_total', 1, {'path': path, 'client_host': client_host})
                    except Exception as metrics_err:
                        logger.warning(f'Failed to record rate limit exceeded metric: {str(metrics_err)}', exc_info=metrics_err)
                raise RateLimitExceededException(message='Rate limit exceeded', details={'ip': client_host, 'path': path}, headers=headers, reset_seconds=applicable_rules[0].window_seconds)
            response: Response = await call_next(request)
            if self.enable_headers:
                for header, value in headers.items():
                    response.headers[header] = value
            return response
        finally:
            if metrics_service and HAS_METRICS:
                duration = time.time() - start_time
                try:
                    metrics_service.observe_histogram('rate_limiting_middleware_duration_seconds', duration, {'limited': str(is_limited)})
                    metrics_service.increment_counter('rate_limiting_requests_total', 1, {'limited': str(is_limited)})
                except Exception as metrics_err:
                    logger.warning(f'Failed to record rate limiting metrics: {str(metrics_err)}', exc_info=metrics_err)