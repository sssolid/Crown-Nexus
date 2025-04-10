from __future__ import annotations
'\nRate limiting middleware for FastAPI applications.\n\nThis middleware applies rate limiting to incoming requests based on configurable\nrules and strategies. It supports both Redis-backed and in-memory rate limiting.\n'
import time
from typing import Any, Callable, Dict, List, Optional, Tuple
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.core.exceptions import RateLimitException
from app.logging import get_logger
from app.core.rate_limiting.limiter import RateLimiter
from app.core.rate_limiting.models import RateLimitRule, RateLimitStrategy
from app.core.rate_limiting.exceptions import RateLimitExceededException
from app.core.dependency_manager import get_service
from app.core.metrics import MetricName
from app.utils.circuit_breaker_utils import safe_is_rate_limited, safe_increment_counter, safe_observe_histogram
logger = get_logger('app.middleware.rate_limiting')
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: Any, rules: Optional[List[RateLimitRule]]=None, use_redis: bool=True, enable_headers: bool=True, block_exceeding_requests: bool=True, fallback_to_memory: bool=True, limit_by_path: bool=False) -> None:
        super().__init__(app)
        self.rules: List[RateLimitRule] = rules or [RateLimitRule(requests_per_window=settings.RATE_LIMIT_REQUESTS_PER_MINUTE * settings.RATE_LIMIT_BURST_MULTIPLIER, window_seconds=60)]
        self.use_redis: bool = use_redis
        self.enable_headers: bool = enable_headers
        self.block_exceeding_requests: bool = block_exceeding_requests
        self.fallback_to_memory: bool = fallback_to_memory
        self.limit_by_path: bool = limit_by_path
        try:
            self.rate_limiter: RateLimiter = RateLimiter(use_redis=use_redis)
            self.using_fallback: bool = False
        except Exception as e:
            if fallback_to_memory:
                logger.warning('Failed to initialize Redis rate limiter, falling back to memory', error=str(e))
                self.rate_limiter = RateLimiter(use_redis=False)
                self.using_fallback = True
            else:
                logger.error('Failed to initialize rate limiter and fallback disabled', error=str(e))
                raise
        logger.info('RateLimitMiddleware initialized', rules_count=len(self.rules), use_redis=use_redis, using_fallback=getattr(self, 'using_fallback', False), enable_headers=enable_headers, block_exceeding_requests=block_exceeding_requests, limit_by_path=limit_by_path)
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        metrics_service = None
        try:
            metrics_service = get_service('metrics_service')
        except Exception as e:
            logger.debug(f'Could not get metrics service: {str(e)}')
        start_time = time.time()
        is_limited = False
        path: str = request.url.path
        client_host = getattr(request.client, 'host', 'unknown') if request.client else 'unknown'
        rate_limit_error = False
        try:
            excluded_path = False
            for rule in self.rules:
                if hasattr(rule, 'exclude_paths') and any((path.startswith(excluded) for excluded in rule.exclude_paths)):
                    excluded_path = True
                    break
            if excluded_path:
                if metrics_service:
                    try:
                        safe_increment_counter('rate_limit_skipped_total', 1, {'endpoint': path, 'reason': 'excluded_path'})
                    except Exception as e:
                        logger.debug(f'Failed to record rate limit metrics: {str(e)}')
                return await call_next(request)
            applicable_rules, rule_match_reason = self._get_applicable_rules(request)
            if not applicable_rules:
                if metrics_service:
                    try:
                        safe_increment_counter('rate_limit_skipped_total', 1, {'endpoint': path, 'reason': 'no_applicable_rules'})
                    except Exception as e:
                        logger.debug(f'Failed to record rate limit metrics: {str(e)}')
                return await call_next(request)
            headers: Dict[str, str] = {}
            limited_rule = None
            for rule in applicable_rules:
                try:
                    key: str = self.rate_limiter.get_key_for_request(request, rule)
                    try:
                        limited, count, limit = await safe_is_rate_limited(self.rate_limiter, key, rule)
                    except Exception as e:
                        logger.warning(f'Rate limit check failed: {str(e)}')
                        limited, count, limit = (False, 0, rule.requests_per_window)
                        rate_limit_error = True
                        continue
                    if limited:
                        is_limited = True
                        limited_rule = rule
                        logger.warning('Rate limit exceeded', client_host=client_host, path=path, key=key, count=count, limit=limit, rule_type=rule.strategy.value)
                        if metrics_service:
                            try:
                                safe_increment_counter('rate_limit_exceeded_total', 1, {'endpoint': path, 'client_host': client_host[:15], 'strategy': rule.strategy.value, 'match_reason': rule_match_reason})
                            except Exception as e:
                                logger.debug(f'Failed to record rate limit metrics: {str(e)}')
                        break
                    if self.enable_headers:
                        remaining = max(0, limit - count)
                        if 'X-RateLimit-Remaining' not in headers or int(headers['X-RateLimit-Remaining']) > remaining:
                            headers['X-RateLimit-Limit'] = str(limit)
                            headers['X-RateLimit-Remaining'] = str(remaining)
                            headers['X-RateLimit-Reset'] = str(rule.window_seconds)
                except Exception as e:
                    logger.error(f'Error processing rate limit rule: {str(e)}', exc_info=True)
                    continue
            if is_limited and self.block_exceeding_requests:
                retry_after = '60'
                if limited_rule is not None:
                    retry_after = str(limited_rule.window_seconds)
                    headers['Retry-After'] = retry_after
                else:
                    logger.error('Rate limit triggered but no limited_rule found')
                    headers['Retry-After'] = retry_after
                return JSONResponse(content={'success': False, 'message': 'Rate limit exceeded', 'error': {'code': 'RATE_LIMIT_EXCEEDED', 'details': {'retry_after': retry_after, 'path': path}}, 'timestamp': time.time()}, status_code=429, headers=headers)
            try:
                response = await call_next(request)
                if self.enable_headers and headers:
                    for header, value in headers.items():
                        response.headers[header] = value
                return response
            except Exception as e:
                logger.error(f'Error in rate limit middleware call_next: {str(e)}', exc_info=True)
                raise
        except Exception as e:
            logger.error(f'Unexpected error in rate limit middleware: {str(e)}', exc_info=True)
            raise
        finally:
            if metrics_service:
                duration = time.time() - start_time
                try:
                    safe_observe_histogram(MetricName.RATE_LIMITING_MIDDLEWARE_DURATION_SECONDS.value, duration, {'limited': str(is_limited), 'path': path})
                    safe_increment_counter(MetricName.RATE_LIMITING_REQUESTS_TOTAL.value, 1, {'limited': str(is_limited), 'path': path})
                except Exception as e:
                    logger.debug(f'Failed to record rate limiting metrics: {str(e)}')
    def _get_applicable_rules(self, request: Request) -> Tuple[List[RateLimitRule], str]:
        path: str = request.url.path
        path_rules = [rule for rule in self.rules if rule.path_pattern is not None and path.startswith(rule.path_pattern)]
        if path_rules:
            return (path_rules, 'path_pattern')
        default_rules = [rule for rule in self.rules if rule.path_pattern is None]
        if default_rules:
            return (default_rules, 'default')
        if self.rules:
            return ([self.rules[0]], 'fallback')
        return ([], 'no_rules')