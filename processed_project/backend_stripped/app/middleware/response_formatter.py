from __future__ import annotations
import datetime
import json
from typing import Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.logging import get_logger
logger = get_logger('app.middleware.response_formatter')
class ResponseFormatterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        if not isinstance(response, JSONResponse):
            return response
        if request.url.path.startswith(('/docs', '/redoc', '/openapi.json')):
            return response
        try:
            body = response.body
            if not body:
                return response
            content = json.loads(body)
            if isinstance(content, dict) and 'success' in content:
                if 'timestamp' not in content:
                    content['timestamp'] = datetime.datetime.now(datetime.UTC).isoformat()
                return JSONResponse(content=content, status_code=response.status_code, headers=dict(response.headers))
            formatted_content = {'success': 200 <= response.status_code < 300, 'message': 'OK' if 200 <= response.status_code < 300 else 'Error', 'data': content, 'meta': {'request_id': getattr(request.state, 'request_id', None)}, 'timestamp': datetime.datetime.now(datetime.UTC).isoformat()}
            return JSONResponse(content=formatted_content, status_code=response.status_code, headers=dict(response.headers))
        except Exception as e:
            logger.error(f'Error formatting response: {str(e)}', exc_info=e, request_id=getattr(request.state, 'request_id', None))
            return response