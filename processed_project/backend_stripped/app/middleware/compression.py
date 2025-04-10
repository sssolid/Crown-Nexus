from __future__ import annotations
from app.utils.circuit_breaker_utils import safe_observe_histogram
'\nCompression middleware for the application.\n\nThis middleware compresses response bodies to reduce network bandwidth and\nimprove client performance.\n'
import time
from typing import Callable, Optional, Any, Dict
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.datastructures import MutableHeaders
import gzip
from app.logging import get_logger
from app.core.dependency_manager import get_service
logger = get_logger('app.middleware.compression')
class CompressionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: Any, minimum_size: int=500, compression_level: int=6, exclude_paths: Optional[list[str]]=None) -> None:
        super().__init__(app)
        self.minimum_size = minimum_size
        self.compression_level = compression_level
        self.exclude_paths = exclude_paths or ['/docs', '/redoc', '/openapi.json']
        logger.info('CompressionMiddleware initialized')
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        accepts_gzip = 'gzip' in request.headers.get('Accept-Encoding', '').lower()
        path = request.url.path
        if not accepts_gzip or any((path.startswith(exc) for exc in self.exclude_paths)):
            return await call_next(request)
        start_time = time.monotonic()
        response = await call_next(request)
        duration = time.monotonic() - start_time
        if 'Content-Encoding' in response.headers:
            return response
        if not hasattr(response, 'body') or response.body is None:
            return response
        response_body = response.body
        if len(response_body) < self.minimum_size:
            return response
        try:
            compressed_body = gzip.compress(response_body, compresslevel=self.compression_level)
            headers = MutableHeaders(dict(response.headers))
            headers['Content-Encoding'] = 'gzip'
            headers['Content-Length'] = str(len(compressed_body))
            try:
                metrics_service = get_service('metrics_service')
                original_size = len(response_body)
                compressed_size = len(compressed_body)
                compression_ratio = (1 - compressed_size / original_size) * 100
                safe_observe_histogram('response_compression_ratio_percent', compression_ratio, {'path': path.split('/')[1] if len(path.split('/')) > 1 else 'root'})
                safe_observe_histogram('response_size_bytes', original_size, {'compressed': 'false', 'path': path.split('/')[1] if len(path.split('/')) > 1 else 'root'})
                safe_observe_histogram('response_size_bytes', compressed_size, {'compressed': 'true', 'path': path.split('/')[1] if len(path.split('/')) > 1 else 'root'})
                logger.debug('Compressed response', original_size=original_size, compressed_size=compressed_size, compression_ratio=f'{compression_ratio:.2f}%', path=path, duration=duration)
            except Exception as e:
                logger.debug(f'Failed to track compression metrics: {str(e)}')
            return Response(content=compressed_body, status_code=response.status_code, headers=dict(headers), media_type=response.media_type)
        except Exception as e:
            logger.warning(f'Compression failed: {str(e)}', exc_info=True)
            return response