# backend/app/middleware/security.py
from __future__ import annotations

from app.core.metrics import MetricName

"""
Security middleware for the application.

This module provides middleware for adding security headers and
blocking suspicious requests.
"""

import re
import time
from typing import Callable, Dict, List, Optional, Any, Pattern

from fastapi import FastAPI, Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.core.exceptions import SecurityException, ErrorCode
from app.logging.context import get_logger
from app.core.dependency_manager import get_service

logger = get_logger("app.middleware.security")


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware for adding security headers to responses.

    This middleware adds headers such as Content-Security-Policy,
    X-Frame-Options, and other security-related headers to responses.
    """

    def __init__(
        self,
        app: FastAPI,
        content_security_policy: Optional[str] = None,
        permissions_policy: Optional[str] = None,
        expect_ct: Optional[str] = None,
        hsts_max_age: int = 31536000,  # 1 year
        include_subdomains: bool = True,
        preload: bool = False,
        exclude_paths: Optional[List[str]] = None,
    ) -> None:
        """
        Initialize the middleware.

        Args:
            app: The FastAPI application
            content_security_policy: Optional CSP header value
            permissions_policy: Optional permissions policy header value
            expect_ct: Optional Expect-CT header value
            hsts_max_age: Max age for HSTS in seconds
            include_subdomains: Include subdomains in HSTS
            preload: Include preload directive in HSTS
            exclude_paths: List of paths to exclude from headers
        """
        super().__init__(app)
        self.content_security_policy: str = (
            content_security_policy or settings.CONTENT_SECURITY_POLICY
        )
        self.permissions_policy: str = permissions_policy or settings.PERMISSIONS_POLICY
        self.expect_ct: Optional[str] = expect_ct
        self.exclude_paths = exclude_paths or []

        # Build HSTS header
        hsts_value = f"max-age={hsts_max_age}"
        if include_subdomains:
            hsts_value += "; includeSubDomains"
        if preload:
            hsts_value += "; preload"
        self.hsts_value = hsts_value

        logger.info(
            "SecurityHeadersMiddleware initialized",
            hsts_max_age=hsts_max_age,
            include_subdomains=include_subdomains,
            preload=preload,
        )

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Response]
    ) -> Response:
        """
        Process the request, adding security headers to the response.

        Args:
            request: The incoming request
            call_next: The next middleware in the chain

        Returns:
            The response with added security headers
        """
        # Get metrics service if available
        metrics_service: Optional[Any] = None
        try:
            metrics_service = get_service("metrics_service")
        except Exception:
            pass  # Continue without metrics service

        # Get the path
        path = request.url.path

        # Check if path should be excluded
        if any(path.startswith(exc) for exc in self.exclude_paths):
            return await call_next(request)

        start_time = time.time()
        try:
            response: Response = await call_next(request)

            # Add security headers
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            response.headers["Content-Security-Policy"] = self.content_security_policy
            response.headers["Strict-Transport-Security"] = self.hsts_value
            response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

            # Add feature policy if available
            if self.permissions_policy:
                response.headers["Permissions-Policy"] = self.permissions_policy

            if self.expect_ct:
                response.headers["Expect-CT"] = self.expect_ct

            # Add security timestamp
            response.headers["X-Security-Headers-Added"] = str(int(time.time()))

            return response
        except Exception as e:
            logger.exception(
                f"Error in SecurityHeadersMiddleware: {str(e)}", exc_info=e
            )
            raise
        finally:
            # Track metrics if available
            if metrics_service:
                try:
                    duration = time.time() - start_time
                    metrics_service.observe_histogram(
                        MetricName.SECURITY_HEADERS_DURATION_SECONDS.value,
                        duration,
                        {"path": path},
                    )
                except Exception as e:
                    logger.debug(f"Failed to track security headers metrics: {e}")


class SecureRequestMiddleware(BaseHTTPMiddleware):
    """
    Middleware for blocking suspicious requests.

    This middleware checks incoming requests for suspicious patterns
    and blocks them if detected.
    """

    def __init__(
        self,
        app: FastAPI,
        block_suspicious_requests: bool = True,
        suspicious_patterns: Optional[List[str]] = None,
        suspicious_regex_patterns: Optional[List[str]] = None,
        exclude_paths: Optional[List[str]] = None,
    ) -> None:
        """
        Initialize the middleware.

        Args:
            app: The FastAPI application
            block_suspicious_requests: Whether to block suspicious requests
            suspicious_patterns: List of suspicious string patterns
            suspicious_regex_patterns: List of suspicious regex patterns
            exclude_paths: List of paths to exclude from security checks
        """
        super().__init__(app)
        self.block_suspicious_requests: bool = block_suspicious_requests
        self.suspicious_patterns: List[str] = suspicious_patterns or [
            "../../",
            "<script",
            "eval(",
            "document.cookie",
            "onload=",
            "javascript:",
            "onerror=",
            "SELECT ",
            "UNION ",
            "DROP ",
            "OR 1=1",
            "alert(",
        ]

        # Compile regex patterns for better performance
        regex_patterns = suspicious_regex_patterns or [
            r"(?i)(union[\s\(\+]+select)",
            r"(?i)(select.+from)",
            r'(?i)(/\*!|\*/(?!\*))',
            r"(?i)(script.*>)",
            r"(?i)(alert\s*\(.*\))",
        ]
        self.regex_patterns: List[Pattern[str]] = [
            re.compile(pattern) for pattern in regex_patterns
        ]

        self.exclude_paths = exclude_paths or [
            "/",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/static/",
            "/media/"
        ]

        logger.info(
            "SecureRequestMiddleware initialized",
            block_suspicious=block_suspicious_requests,
            patterns_count=len(self.suspicious_patterns),
            regex_count=len(self.regex_patterns),
        )

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Response]
    ) -> Response:
        """
        Process the request, checking for suspicious patterns.

        Args:
            request: The incoming request
            call_next: The next middleware in the chain

        Returns:
            The response if the request is not suspicious

        Raises:
            SecurityException: If the request is suspicious and blocking is enabled
        """
        # Get metrics service if available
        metrics_service: Optional[Any] = None
        try:
            metrics_service = get_service("metrics_service")
        except Exception:
            pass  # Continue without metrics service

        # Get the path
        path = request.url.path

        # Skip excluded paths
        if any(path.startswith(exc) for exc in self.exclude_paths):
            return await call_next(request)

        start_time = time.time()
        suspicious = False
        suspicious_pattern = None

        try:
            if self.block_suspicious_requests:
                suspicious, suspicious_pattern = await self._is_suspicious_request(request)

                if suspicious:
                    client_ip = getattr(request.client, "host", "unknown") if request.client else "unknown"
                    logger.warning(
                        f"Blocked suspicious request",
                        ip=client_ip,
                        path=path,
                        method=request.method,
                        pattern=suspicious_pattern,
                    )

                    # Track blocked request if metrics available
                    if metrics_service:
                        try:
                            metrics_service.increment_counter(
                                "blocked_suspicious_requests_total",
                                1,
                                {
                                    "endpoint": path,
                                    "method": request.method,
                                    "pattern_type": "regex" if isinstance(suspicious_pattern, re.Pattern) else "string",
                                },
                            )
                        except Exception as e:
                            logger.debug(f"Failed to track security metrics: {e}")

                    raise SecurityException(
                        message="Forbidden - Suspicious request detected",
                        details={"ip": client_ip, "path": path},
                        status_code=status.HTTP_403_FORBIDDEN
                    )

            return await call_next(request)
        finally:
            # Track metrics if available
            if metrics_service:
                try:
                    duration = time.time() - start_time
                    metrics_service.observe_histogram(
                        MetricName.REQUEST_SECURITY_CHECK_DURATION_SECONDS.value,
                        duration,
                        {"suspicious": str(suspicious), "path": path},
                    )
                except Exception as e:
                    logger.debug(f"Failed to track security check metrics: {e}")

    async def _is_suspicious_request(self, request: Request) -> tuple[bool, Optional[Any]]:
        """
        Check if a request contains suspicious patterns.

        Args:
            request: The request to check

        Returns:
            Tuple of (is_suspicious, matched_pattern)
        """
        # Check path
        path = request.url.path
        for pattern in self.suspicious_patterns:
            if pattern.lower() in path.lower():
                logger.warning(
                    f"Suspicious pattern detected in path", pattern=pattern, path=path
                )
                return True, pattern

        # Check query string
        query_string = str(request.url.query)
        for pattern in self.suspicious_patterns:
            if pattern.lower() in query_string.lower():
                logger.warning(
                    f"Suspicious pattern detected in query",
                    pattern=pattern,
                    query=query_string,
                )
                return True, pattern

        # Check regex patterns against both path and query
        combined = f"{path}?{query_string}"
        for regex in self.regex_patterns:
            if regex.search(combined):
                logger.warning(
                    f"Suspicious regex pattern detected",
                    pattern=regex.pattern,
                    path=path,
                    query=query_string,
                )
                return True, regex

        # Check headers
        for header_name, header_value in request.headers.items():
            for pattern in self.suspicious_patterns:
                if pattern.lower() in header_value.lower():
                    logger.warning(
                        f"Suspicious pattern detected in header",
                        pattern=pattern,
                        header_name=header_name,
                    )
                    return True, pattern

            # Check regex patterns in headers
            for regex in self.regex_patterns:
                if regex.search(header_value):
                    logger.warning(
                        f"Suspicious regex pattern detected in header",
                        pattern=regex.pattern,
                        header_name=header_name,
                    )
                    return True, regex

        # We can't check the body without consuming it, which would break other middleware
        # This would require more complex handling to read and restore the body

        return False, None
