# app/middleware/response_formatter.py
from __future__ import annotations

import json
from typing import Any, Callable, Dict, Optional, Union, cast

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.background import BackgroundTask
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse

from app.core.logging import get_logger
from app.schemas.responses import Response as StandardResponse

logger = get_logger("app.middleware.response_formatter")


class ResponseFormatterMiddleware(BaseHTTPMiddleware):
    """Middleware to format responses into a standard structure.
    
    This middleware intercepts responses and wraps them in the standard
    response envelope if they are not already formatted.
    """
    
    def __init__(
        self, 
        app: FastAPI,
        exclude_paths: Optional[list[str]] = None,
    ) -> None:
        """Initialize the middleware.
        
        Args:
            app: FastAPI application
            exclude_paths: Paths to exclude from formatting
        """
        super().__init__(app)
        self.exclude_paths = exclude_paths or [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/health",
        ]
    
    async def dispatch(
        self, 
        request: Request, 
        call_next: Callable[[Request], Response],
    ) -> Response:
        """Process the request and format the response.
        
        Args:
            request: FastAPI request
            call_next: Next middleware in the chain
            
        Returns:
            Response: Formatted HTTP response
        """
        # Skip formatting for excluded paths
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return await call_next(request)
        
        # Get request ID from context if available
        request_id = getattr(request.state, "request_id", None)
        
        # Process the request
        response = await call_next(request)
        
        # Skip certain types of responses
        if isinstance(response, StreamingResponse):
            return response
        
        # Skip already formatted responses
        if hasattr(response, "is_formatted") and response.is_formatted:
            return response
        
        # Skip redirect responses
        if 300 <= response.status_code < 400:
            return response
        
        # Format JSON responses
        if isinstance(response, JSONResponse):
            return self.format_json_response(response, request_id)
        
        # Handle other response types
        if hasattr(response, "body"):
            try:
                body = response.body.decode("utf-8")
                if body.startswith("{") or body.startswith("["):
                    # Attempt to parse as JSON
                    data = json.loads(body)
                    formatted_response = self.create_formatted_response(
                        data, 
                        response.status_code, 
                        request_id,
                    )
                    return formatted_response
            except (json.JSONDecodeError, UnicodeDecodeError):
                # Not a JSON response, return as-is
                pass
        
        # Return unmodified response for non-JSON responses
        return response
    
    def format_json_response(
        self, 
        response: JSONResponse, 
        request_id: Optional[str] = None,
    ) -> JSONResponse:
        """Format a JSON response into the standard envelope.
        
        Args:
            response: Original JSON response
            request_id: Request ID for tracking
            
        Returns:
            JSONResponse: Formatted JSON response
        """
        # Extract data from original response
        content = response.body.decode("utf-8")
        data = json.loads(content)
        
        # Check if already in standard format
        if isinstance(data, dict) and "status" in data and "data" in data:
            if "meta" in data and data["meta"] and request_id:
                # Add request ID to existing metadata
                if data["meta"].get("request_id") is None:
                    data["meta"]["request_id"] = request_id
                
            # Mark as already formatted and return
            formatted_response = JSONResponse(
                content=data,
                status_code=response.status_code,
                headers=response.headers,
                media_type=response.media_type,
                background=response.background,
            )
            setattr(formatted_response, "is_formatted", True)
            return formatted_response
        
        # Create formatted response
        return self.create_formatted_response(
            data, 
            response.status_code,
            request_id,
            response.background,
            dict(response.headers),
        )
    
    def create_formatted_response(
        self,
        data: Any,
        status_code: int,
        request_id: Optional[str] = None,
        background: Optional[BackgroundTask] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> JSONResponse:
        """Create a formatted response using the standard envelope.
        
        Args:
            data: Response data
            status_code: HTTP status code
            request_id: Request ID for tracking
            background: Background task
            headers: Response headers
            
        Returns:
            JSONResponse: Formatted JSON response
        """
        # Determine if success or error based on status code
        is_success = 200 <= status_code < 300
        
        # Create standard response
        if is_success:
            standard_response = StandardResponse.success(
                data=data,
                code=status_code,
                request_id=request_id,
            )
        else:
            message = "Request failed"
            if isinstance(data, dict) and "detail" in data:
                message = data["detail"]
            
            standard_response = StandardResponse.error(
                message=message,
                code=status_code,
                data=data,
                request_id=request_id,
            )
        
        # Create response
        formatted_response = JSONResponse(
            content=standard_response.dict(),
            status_code=status_code,
            background=background,
            headers=headers,
        )
        
        # Mark as formatted to avoid double formatting
        setattr(formatted_response, "is_formatted", True)
        
        return formatted_response
