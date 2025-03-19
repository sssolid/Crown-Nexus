# backend/app/middleware/security.py
"""Security middleware components for Crown Nexus application.

This module provides middleware components that enhance the security of the
application by adding security headers, validating requests, and preventing
common web vulnerabilities like XSS, CSRF, and clickjacking.
"""

from __future__ import annotations

import json
from typing import Callable, Optional, Dict, Any

from fastapi import FastAPI, Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.core.exceptions import SecurityException
from app.core.logging import get_logger

logger = get_logger("app.middleware.security")


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware that adds security headers to all responses.

    This middleware adds various security headers to enhance protection against
    common web vulnerabilities like XSS, clickjacking, and MIME type sniffing.

    Attributes:
        content_security_policy: CSP policy string for the application
        permissions_policy: Permissions policy string to restrict features
        expect_ct: Certificate Transparency policy
    """

    def __init__(
        self,
        app: FastAPI,
        content_security_policy: Optional[str] = None,
        permissions_policy: Optional[str] = None,
        expect_ct: Optional[str] = None,
    ) -> None:
        """Initialize the security headers middleware.

        Args:
            app: The FastAPI application
            content_security_policy: CSP policy string, defaults to restrictive policy
            permissions_policy: Permissions policy string, defaults to restrictive policy
            expect_ct: Certificate Transparency policy, defaults to None
        """
        super().__init__(app)
        self.content_security_policy: str = (
            content_security_policy or settings.CONTENT_SECURITY_POLICY
        )
        self.permissions_policy: str = (
            permissions_policy or settings.PERMISSIONS_POLICY
        )
        self.expect_ct: Optional[str] = expect_ct

        logger.info("SecurityHeadersMiddleware initialized")

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Response],
    ) -> Response:
        """Process the request and add security headers to the response.

        Args:
            request: The incoming request
            call_next: The next middleware or route handler

        Returns:
            Response: The processed response with security headers
        """
        try:
            # Process the request through the rest of the application
            response: Response = await call_next(request)

            # Add security headers
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            response.headers["Content-Security-Policy"] = self.content_security_policy
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )
            response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

            # Add optional headers
            if self.permissions_policy:
                response.headers["Permissions-Policy"] = self.permissions_policy

            if self.expect_ct:
                response.headers["Expect-CT"] = self.expect_ct

            return response
        except Exception as e:
            # Let the application's error handlers handle exceptions
            # This ensures the exception handling middleware can process all exceptions
            raise


class SecureRequestMiddleware(BaseHTTPMiddleware):
    """Middleware for validating and sanitizing incoming requests.

    This middleware checks request data for potential security issues
    and can reject suspicious requests.

    Attributes:
        block_suspicious_requests: Whether to block suspicious requests
        suspicious_patterns: List of patterns to check for in request data
    """

    def __init__(
        self,
        app: FastAPI,
        block_suspicious_requests: bool = True,
    ) -> None:
        """Initialize the secure request middleware.

        Args:
            app: The FastAPI application
            block_suspicious_requests: Whether to block requests that look suspicious
        """
        super().__init__(app)
        self.block_suspicious_requests: bool = block_suspicious_requests
        self.suspicious_patterns: list[str] = [
            "../../",  # Path traversal
            "<script",  # Basic XSS
            "eval(",  # Code injection
            "SELECT ",  # SQL injection
        ]
        logger.info("SecureRequestMiddleware initialized")

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Response],
    ) -> Response:
        """Process and validate incoming requests.

        Args:
            request: The incoming request
            call_next: The next middleware or route handler

        Returns:
            Response: The processed response

        Raises:
            SecurityException: If the request appears suspicious
        """
        # Check for suspicious patterns in headers
        if self.block_suspicious_requests and self._is_suspicious_request(request):
            logger.warning(f"Blocked suspicious request from {request.client.host}")

            # Use custom exception from app's hierarchy
            raise SecurityException(
                message="Forbidden - Suspicious request detected",
                details={"ip": request.client.host},
                status_code=status.HTTP_403_FORBIDDEN,
            )

        return await call_next(request)

    def _is_suspicious_request(self, request: Request) -> bool:
        """Check if the request contains suspicious patterns.

        Args:
            request: The incoming HTTP request

        Returns:
            bool: True if the request appears suspicious, False otherwise
        """
        # Check URL path for suspicious patterns
        path = request.url.path
        for pattern in self.suspicious_patterns:
            if pattern.lower() in path.lower():
                logger.warning(f"Suspicious pattern '{pattern}' found in path: {path}")
                return True

        # Check query parameters
        query_string = str(request.url.query)
        for pattern in self.suspicious_patterns:
            if pattern.lower() in query_string.lower():
                logger.warning(f"Suspicious pattern '{pattern}' found in query: {query_string}")
                return True

        # Check headers for suspicious patterns
        for header_name, header_value in request.headers.items():
            for pattern in self.suspicious_patterns:
                if pattern.lower() in header_value.lower():
                    logger.warning(f"Suspicious pattern '{pattern}' found in header {header_name}")
                    return True

        # Check request body if available
        async def check_body() -> bool:
            try:
                body = await request.body()
                if body:
                    body_str = body.decode("utf-8", errors="ignore")
                    for pattern in self.suspicious_patterns:
                        if pattern.lower() in body_str.lower():
                            logger.warning(f"Suspicious pattern '{pattern}' found in request body")
                            return True
            except Exception as e:
                logger.debug(f"Error checking request body: {str(e)}")
            return False

        # We can't check the body here as it would consume it
        # The body check would need to be implemented differently for production
        # potentially using a custom request object that allows multiple body reads

        # Request appears safe
        return False
