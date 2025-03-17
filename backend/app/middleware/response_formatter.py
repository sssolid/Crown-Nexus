# /backend/app/middleware/response_formatter.py
from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Callable, Dict, Optional, Union

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import get_logger

logger = get_logger("app.middleware.response_formatter")

class ResponseFormatterMiddleware(BaseHTTPMiddleware):
    """Middleware for formatting API responses.
    
    This middleware ensures all API responses follow a consistent format,
    with success flag, data, and metadata. It also adds timestamps and
    request IDs to responses.
    """
    
    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        """Process the request and format the response.
        
        Args:
            request: FastAPI request
            call_next: Next middleware or route handler
            
        Returns:
            Response: Formatted response
        """
        # Process request
        response = await call_next(request)
        
        # Only format JSON responses
        if not isinstance(response, JSONResponse):
            return response
            
        # Skip formatting for documentation endpoints
        if request.url.path.startswith(("/docs", "/redoc", "/openapi.json")):
            return response
            
        # Extract response content
        try:
            body = response.body
            if not body:
                return response
                
            # Parse JSON content
            content = json.loads(body)
            
            # Skip formatting if already formatted
            if isinstance(content, dict) and "success" in content:
                # Just add timestamp if not present
                if "timestamp" not in content:
                    content["timestamp"] = datetime.utcnow().isoformat()
                
                # Create new response with modified content
                return JSONResponse(
                    content=content,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                )
                
            # Format response
            formatted_content = {
                "success": 200 <= response.status_code < 300,
                "message": "OK" if 200 <= response.status_code < 300 else "Error",
                "data": content,
                "meta": {
                    "request_id": getattr(request.state, "request_id", None),
                },
                "timestamp": datetime.utcnow().isoformat(),
            }
            
            # Create new response with formatted content
            return JSONResponse(
                content=formatted_content,
                status_code=response.status_code,
                headers=dict(response.headers),
            )
        except Exception as e:
            # Log error and return original response
            logger.error(
                f"Error formatting response: {str(e)}",
                exc_info=e,
                request_id=getattr(request.state, "request_id", None),
            )
            return response