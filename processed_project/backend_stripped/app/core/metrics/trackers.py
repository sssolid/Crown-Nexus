from __future__ import annotations
from typing import Optional
from app.logging import get_logger
from app.core.metrics.base import MetricName, MetricTag
logger = get_logger('app.core.metrics.trackers')
class HttpTracker:
    def __init__(self, increment_counter_func: callable, observe_histogram_func: callable, increment_error_func: callable):
        self.increment_counter = increment_counter_func
        self.observe_histogram = observe_histogram_func
        self.increment_error = increment_error_func
    def track_request(self, method: str, endpoint: str, status_code: int, duration: float, error_code: Optional[str]=None) -> None:
        self.increment_counter(MetricName.HTTP_REQUESTS_TOTAL, 1, {MetricTag.METHOD: method, MetricTag.ENDPOINT: endpoint, MetricTag.STATUS_CODE: str(status_code)})
        self.observe_histogram(MetricName.HTTP_REQUEST_DURATION_SECONDS, duration, {MetricTag.METHOD: method, MetricTag.ENDPOINT: endpoint})
        if status_code >= 400:
            self.increment_error(MetricName.HTTP_ERRORS_TOTAL, 1, {MetricTag.METHOD: method, MetricTag.ENDPOINT: endpoint, MetricTag.ERROR_CODE: error_code or f'http_{status_code}'})
class DatabaseTracker:
    def __init__(self, increment_counter_func: callable, observe_histogram_func: callable, increment_error_func: callable):
        self.increment_counter = increment_counter_func
        self.observe_histogram = observe_histogram_func
        self.increment_error = increment_error_func
    def track_query(self, operation: str, entity: str, duration: float, error: Optional[str]=None) -> None:
        self.increment_counter(MetricName.DB_QUERIES_TOTAL, 1, {MetricTag.OPERATION: operation, MetricTag.ENTITY: entity})
        self.observe_histogram(MetricName.DB_QUERY_DURATION_SECONDS, duration, {MetricTag.OPERATION: operation, MetricTag.ENTITY: entity})
        if error:
            self.increment_error(MetricName.DB_ERRORS_TOTAL, 1, {MetricTag.OPERATION: operation, MetricTag.ENTITY: entity, MetricTag.ERROR_TYPE: error})
class ServiceTracker:
    def __init__(self, increment_counter_func: callable, observe_histogram_func: callable, increment_error_func: callable):
        self.increment_counter = increment_counter_func
        self.observe_histogram = observe_histogram_func
        self.increment_error = increment_error_func
    def track_call(self, component: str, action: str, duration: float, error: Optional[str]=None) -> None:
        self.increment_counter(MetricName.SERVICE_CALLS_TOTAL, 1, {MetricTag.COMPONENT: component, MetricTag.ACTION: action})
        self.observe_histogram(MetricName.SERVICE_CALL_DURATION_SECONDS, duration, {MetricTag.COMPONENT: component, MetricTag.ACTION: action})
        if error:
            self.increment_error(MetricName.SERVICE_ERRORS_TOTAL, 1, {MetricTag.COMPONENT: component, MetricTag.ACTION: action, MetricTag.ERROR_TYPE: error})
class CacheTracker:
    def __init__(self, increment_counter_func: callable, observe_histogram_func: callable):
        self.increment_counter = increment_counter_func
        self.observe_histogram = observe_histogram_func
    def track_operation(self, operation: str, backend: str, hit: bool, duration: float, component: str='unknown') -> None:
        self.increment_counter(MetricName.CACHE_OPERATIONS_TOTAL, 1, {MetricTag.OPERATION: operation, MetricTag.CACHE_BACKEND: backend, MetricTag.COMPONENT: component})
        if operation == 'get':
            if hit:
                self.increment_counter(MetricName.CACHE_HIT_TOTAL, 1, {MetricTag.CACHE_BACKEND: backend, MetricTag.COMPONENT: component})
            else:
                self.increment_counter(MetricName.CACHE_MISS_TOTAL, 1, {MetricTag.CACHE_BACKEND: backend, MetricTag.COMPONENT: component})
        self.observe_histogram(MetricName.CACHE_OPERATION_DURATION_SECONDS, duration, {MetricTag.CACHE_BACKEND: backend, MetricTag.OPERATION: operation})