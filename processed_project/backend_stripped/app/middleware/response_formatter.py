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
logger = get_logger('app.middleware.response_formatter')
class ResponseFormatterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, exclude_paths: Optional[list[str]]=None) -> None:
        super().__init__(app)
        self.exclude_paths = exclude_paths or ['/docs', '/redoc', '/openapi.json', '/health']
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        if any((request.url.path.startswith(path) for path in self.exclude_paths)):
            return await call_next(request)
        request_id = getattr(request.state, 'request_id', None)
        response = await call_next(request)
        if isinstance(response, StreamingResponse):
            return response
        if hasattr(response, 'is_formatted') and response.is_formatted:
            return response
        if 300 <= response.status_code < 400:
            return response
        if isinstance(response, JSONResponse):
            return self.format_json_response(response, request_id)
        if hasattr(response, 'body'):
            try:
                body = response.body.decode('utf-8')
                if body.startswith('{') or body.startswith('['):
                    data = json.loads(body)
                    formatted_response = self.create_formatted_response(data, response.status_code, request_id)
                    return formatted_response
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass
        return response
    def format_json_response(self, response: JSONResponse, request_id: Optional[str]=None) -> JSONResponse:
        content = response.body.decode('utf-8')
        data = json.loads(content)
        if isinstance(data, dict) and 'status' in data and ('data' in data):
            if 'meta' in data and data['meta'] and request_id:
                if data['meta'].get('request_id') is None:
                    data['meta']['request_id'] = request_id
            formatted_response = JSONResponse(content=data, status_code=response.status_code, headers=response.headers, media_type=response.media_type, background=response.background)
            setattr(formatted_response, 'is_formatted', True)
            return formatted_response
        return self.create_formatted_response(data, response.status_code, request_id, response.background, dict(response.headers))
    def create_formatted_response(self, data: Any, status_code: int, request_id: Optional[str]=None, background: Optional[BackgroundTask]=None, headers: Optional[Dict[str, str]]=None) -> JSONResponse:
        is_success = 200 <= status_code < 300
        if is_success:
            standard_response = StandardResponse.success(data=data, code=status_code, request_id=request_id)
        else:
            message = 'Request failed'
            if isinstance(data, dict) and 'detail' in data:
                message = data['detail']
            standard_response = StandardResponse.error(message=message, code=status_code, data=data, request_id=request_id)
        formatted_response = JSONResponse(content=standard_response.dict(), status_code=status_code, background=background, headers=headers)
        setattr(formatted_response, 'is_formatted', True)
        return formatted_response