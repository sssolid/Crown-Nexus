# backend/app/middleware/__init__.py
from __future__ import annotations

"""
Middleware package for the application.

This package contains all middleware components used by the application to process
HTTP requests and responses. Middleware are executed in the order they are added
to the application.

Available middleware:
- RequestContextMiddleware: Sets up request context and attaches request ID
- RequestLoggingMiddleware: Logs request/response details
- TracingMiddleware: Implements distributed tracing
- MetricsMiddleware: Collects request metrics
- TimeoutMiddleware: Enforces request timeout limits
- CompressionMiddleware: Compresses response data
- SecurityHeadersMiddleware: Adds security headers to responses
- SecureRequestMiddleware: Blocks suspicious requests
- RateLimitMiddleware: Controls request rate limiting
- CacheControlMiddleware: Adds cache control headers
- ResponseFormatterMiddleware: Standardizes API response format
- ErrorHandlerMiddleware: Handles exceptions during request processing

Middleware best practices:
1. Order matters - Consider request flow when ordering middleware
2. Performance impact - Keep middleware lightweight
3. Error handling - Handle errors appropriately in each middleware
4. Metrics - Track performance metrics where possible
5. Idempotency - Ensure middleware can be executed multiple times safely
"""

from app.middleware.request_context import RequestContextMiddleware
from app.middleware.tracing import TracingMiddleware
from app.middleware.metrics import MetricsMiddleware
from app.middleware.timeout import TimeoutMiddleware
from app.middleware.compression import CompressionMiddleware
from app.middleware.security import SecurityHeadersMiddleware, SecureRequestMiddleware
from app.middleware.rate_limiting import RateLimitMiddleware
from app.middleware.cache_control import CacheControlMiddleware
from app.middleware.response_formatter import ResponseFormatterMiddleware
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.middleware.cors import EnhancedCORSMiddleware

__all__ = [
    "RequestContextMiddleware",
    "TracingMiddleware",
    "MetricsMiddleware",
    "TimeoutMiddleware",
    "CompressionMiddleware",
    "SecurityHeadersMiddleware",
    "SecureRequestMiddleware",
    "RateLimitMiddleware",
    "CacheControlMiddleware",
    "ResponseFormatterMiddleware",
    "ErrorHandlerMiddleware",
    "EnhancedCORSMiddleware",
]
