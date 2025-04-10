from __future__ import annotations
import uuid
from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional, Tuple
from app.logging import get_logger
from app.core.metrics.base import MetricName, MetricTag, MetricType, MetricsConfig
from app.core.metrics.collectors import CounterCollector, GaugeCollector, HistogramCollector, SummaryCollector
from app.core.metrics.decorators import async_timed, timed
from app.core.metrics.prometheus import PrometheusManager
from app.core.metrics.trackers import CacheTracker, DatabaseTracker, HttpTracker, ServiceTracker
logger = get_logger('app.core.metrics.manager')
_config: MetricsConfig = MetricsConfig()
_counters: Dict[str, CounterCollector] = {}
_gauges: Dict[str, GaugeCollector] = {}
_histograms: Dict[str, HistogramCollector] = {}
_summaries: Dict[str, SummaryCollector] = {}
_instance_id = str(uuid.uuid4())[:8]
_in_progress: Dict[str, Dict[Tuple, int]] = defaultdict(dict)
_prometheus: Optional[PrometheusManager] = None
_http_tracker: Optional[HttpTracker] = None
_db_tracker: Optional[DatabaseTracker] = None
_service_tracker: Optional[ServiceTracker] = None
_cache_tracker: Optional[CacheTracker] = None
_initialized = False
def _init_trackers() -> None:
    global _http_tracker, _db_tracker, _service_tracker, _cache_tracker
    _http_tracker = HttpTracker(increment_counter, observe_histogram, increment_counter)
    _db_tracker = DatabaseTracker(increment_counter, observe_histogram, increment_counter)
    _service_tracker = ServiceTracker(increment_counter, observe_histogram, increment_counter)
    _cache_tracker = CacheTracker(increment_counter, observe_histogram)
def _initialize_default_metrics() -> None:
    create_counter(MetricName.HTTP_REQUESTS_TOTAL.value, 'Total number of HTTP requests', [MetricTag.METHOD, MetricTag.ENDPOINT, MetricTag.STATUS_CODE])
    create_histogram(MetricName.HTTP_REQUEST_DURATION_SECONDS.value, 'HTTP request duration in seconds', [MetricTag.METHOD, MetricTag.ENDPOINT, MetricTag.STATUS_CODE])
    create_counter(MetricName.HTTP_REQUESTS_BY_AGENT_TOTAL.value, 'Total number of HTTP requests by agent type and endpoint', [MetricTag.AGENT_TYPE, MetricTag.ENDPOINT])
    create_gauge(MetricName.HTTP_IN_PROGRESS.value, 'Number of HTTP requests in progress', [MetricTag.METHOD, MetricTag.ENDPOINT])
    create_counter(MetricName.HTTP_ERRORS_TOTAL.value, 'Total number of HTTP errors', [MetricTag.METHOD, MetricTag.ENDPOINT, MetricTag.ERROR_CODE])
    create_counter(MetricName.DB_QUERIES_TOTAL.value, 'Total number of database queries', [MetricTag.OPERATION, MetricTag.ENTITY])
    create_histogram(MetricName.DB_QUERY_DURATION_SECONDS.value, 'Database query duration in seconds', [MetricTag.OPERATION, MetricTag.ENTITY])
    create_counter(MetricName.DB_ERRORS_TOTAL.value, 'Total number of database errors', [MetricTag.OPERATION, MetricTag.ENTITY, MetricTag.ERROR_TYPE])
    create_counter(MetricName.SERVICE_CALLS_TOTAL.value, 'Total number of service calls', [MetricTag.COMPONENT, MetricTag.ACTION])
    create_histogram(MetricName.SERVICE_CALL_DURATION_SECONDS.value, 'Service call duration in seconds', [MetricTag.COMPONENT, MetricTag.ACTION])
    create_counter(MetricName.SERVICE_ERRORS_TOTAL.value, 'Total number of service errors', [MetricTag.COMPONENT, MetricTag.ACTION, MetricTag.ERROR_TYPE])
    create_counter(MetricName.CACHE_HIT_TOTAL.value, 'Total number of cache hits', [MetricTag.CACHE_BACKEND, MetricTag.COMPONENT])
    create_counter(MetricName.CACHE_MISS_TOTAL.value, 'Total number of cache misses', [MetricTag.CACHE_BACKEND, MetricTag.COMPONENT])
    create_histogram(MetricName.CACHE_OPERATION_DURATION_SECONDS.value, 'Cache operation duration in seconds', [MetricTag.CACHE_BACKEND, MetricTag.OPERATION])
    create_histogram(MetricName.REQUEST_TRACE_DURATION_SECONDS.value, 'Duration of request traces in seconds', [MetricTag.PATH, MetricTag.METHOD, MetricTag.STATUS_CODE, MetricTag.ERROR_CODE])
    create_histogram(MetricName.RATE_LIMITING_CHECK_DURATION_SECONDS.value, 'Duration of rate limiting checks', [MetricTag.CACHE_BACKEND, MetricTag.ERROR_TYPE])
    create_histogram(MetricName.RATE_LIMITING_MIDDLEWARE_DURATION_SECONDS.value, 'Rate limiting middleware execution time', [MetricTag.LIMITED, MetricTag.PATH])
    create_counter(MetricName.RATE_LIMITING_REQUESTS_TOTAL.value, 'Total number of rate-limited requests', [MetricTag.LIMITED, MetricTag.PATH])
    create_histogram(MetricName.HTTP_RESPONSE_SIZE_BYTES.value, 'Size of HTTP responses in bytes', [MetricTag.PATH, MetricTag.METHOD])
    create_counter(MetricName.HTTP_STATUS_CODES_TOTAL.value, 'HTTP status code count', [MetricTag.METHOD, MetricTag.ENDPOINT, MetricTag.STATUS_CODE])
    create_histogram(MetricName.REQUEST_SECURITY_CHECK_DURATION_SECONDS.value, 'Duration of security checks on requests', [MetricTag.SUSPICIOUS, MetricTag.PATH])
    create_histogram(MetricName.SECURITY_HEADERS_DURATION_SECONDS.value, 'Duration to set security headers', [MetricTag.PATH])
    create_histogram(MetricName.RESPONSE_FORMATTING_DURATION_SECONDS.value, 'Time taken to format HTTP responses', [MetricTag.RESPONSE_FORMATTED, MetricTag.PATH])
    if _config.enable_process_metrics:
        create_gauge(MetricName.PROCESS_RESIDENT_MEMORY_BYTES.value, 'Resident memory size in bytes', [])
        create_gauge(MetricName.PROCESS_VIRTUAL_MEMORY_BYTES.value, 'Virtual memory size in bytes', [])
        create_counter(MetricName.PROCESS_CPU_SECONDS_TOTAL.value, 'Total user and system CPU time spent in seconds', [])
        create_gauge(MetricName.PROCESS_OPEN_FDS.value, 'Number of open file descriptors', [])
async def initialize(config: Optional[MetricsConfig]=None) -> None:
    global _config, _prometheus, _initialized
    if _initialized:
        return
    logger.debug('Initializing metrics system')
    if config:
        _config = config
    _init_trackers()
    if _config.enable_default_metrics:
        _initialize_default_metrics()
    if _config.enable_prometheus:
        _prometheus = PrometheusManager(_config)
        await _prometheus.initialize()
    _initialized = True
    logger.info('Metrics system initialized')
async def shutdown() -> None:
    global _prometheus, _initialized
    logger.debug('Shutting down metrics system')
    if _prometheus and _config.enable_prometheus:
        await _prometheus.shutdown()
    _initialized = False
def create_counter(name: str, description: str, labelnames: Optional[List[str]]=None, namespace: Optional[str]=None, subsystem: Optional[str]=None) -> CounterCollector:
    name = str(name)
    namespace = namespace or _config.namespace
    subsystem = subsystem or _config.subsystem
    if name not in _counters:
        _counters[name] = CounterCollector(name=name, description=description, labelnames=labelnames or [], namespace=namespace, subsystem=subsystem)
    return _counters[name]
def create_gauge(name: str, description: str, labelnames: Optional[List[str]]=None, namespace: Optional[str]=None, subsystem: Optional[str]=None) -> GaugeCollector:
    name = str(name)
    namespace = namespace or _config.namespace
    subsystem = subsystem or _config.subsystem
    if name not in _gauges:
        _gauges[name] = GaugeCollector(name=name, description=description, labelnames=labelnames or [], namespace=namespace, subsystem=subsystem)
    return _gauges[name]
def create_histogram(name: str, description: str, labelnames: Optional[List[str]]=None, buckets: Optional[List[float]]=None, namespace: Optional[str]=None, subsystem: Optional[str]=None) -> HistogramCollector:
    name = str(name)
    namespace = namespace or _config.namespace
    subsystem = subsystem or _config.subsystem
    buckets = buckets or _config.default_buckets
    if name not in _histograms:
        _histograms[name] = HistogramCollector(name=name, description=description, labelnames=labelnames or [], buckets=buckets, namespace=namespace, subsystem=subsystem)
    return _histograms[name]
def create_summary(name: str, description: str, labelnames: Optional[List[str]]=None, namespace: Optional[str]=None, subsystem: Optional[str]=None) -> SummaryCollector:
    namespace = namespace or _config.namespace
    subsystem = subsystem or _config.subsystem
    if name not in _summaries:
        _summaries[name] = SummaryCollector(name=name, description=description, labelnames=labelnames or [], namespace=namespace, subsystem=subsystem)
    return _summaries[name]
def increment_counter(name: str, amount: float=1.0, labels: Optional[Dict[str, str]]=None) -> None:
    name = str(name)
    if name not in _counters:
        logger.warning(f'Counter {name} not found, skipping increment')
        return
    _counters[name].increment(amount, labels)
def set_gauge(name: str, value: float, labels: Optional[Dict[str, str]]=None) -> None:
    if name not in _gauges:
        logger.warning(f'Gauge {name} not found, skipping set')
        return
    _gauges[name].set(value, labels)
def observe_histogram(name: str, value: float, labels: Optional[Dict[str, str]]=None) -> None:
    name = str(name)
    if name not in _histograms:
        logger.warning(f'Histogram {name} not found, skipping observation')
        return
    _histograms[name].observe(value, labels)
def observe_summary(name: str, value: float, labels: Optional[Dict[str, str]]=None) -> None:
    name = str(name)
    if name not in _summaries:
        logger.warning(f'Summary {name} not found, skipping observation')
        return
    _summaries[name].observe(value, labels)
def track_in_progress(metric_name: str, labels: Dict[str, str], count: int=1) -> None:
    metric_name = str(metric_name)
    if metric_name not in _gauges:
        logger.warning(f'Gauge {metric_name} not found, skipping in-progress tracking')
        return
    labels_key = tuple(sorted(labels.items()))
    current = _in_progress[metric_name].get(labels_key, 0)
    new_count = max(0, current + count)
    _in_progress[metric_name][labels_key] = new_count
    set_gauge(metric_name, new_count, labels)
def track_request(method: str, endpoint: str, status_code: int, duration: float, error_code: Optional[str]=None) -> None:
    if _http_tracker:
        _http_tracker.track_request(method, endpoint, status_code, duration, error_code)
def track_db_query(operation: str, entity: str, duration: float, error: Optional[str]=None) -> None:
    if _db_tracker:
        _db_tracker.track_query(operation, entity, duration, error)
def track_service_call(component: str, action: str, duration: float, error: Optional[str]=None) -> None:
    if _service_tracker:
        _service_tracker.track_call(component, action, duration, error)
def track_cache_operation(operation: str, backend: str, hit: bool, duration: float, component: str='unknown') -> None:
    if _cache_tracker:
        _cache_tracker.track_operation(operation, backend, hit, duration, component)
def timed_function(name: str, metric_type: MetricType=MetricType.HISTOGRAM, labels_func: Optional[Callable[..., Dict[str, str]]]=None, track_in_progress_flag: bool=False, in_progress_metric: Optional[str]=None) -> Callable:
    observe_func = None
    if metric_type == MetricType.HISTOGRAM:
        observe_func = observe_histogram
    elif metric_type == MetricType.SUMMARY:
        observe_func = observe_summary
    else:
        raise ValueError(f'Invalid metric type for timing: {metric_type}')
    return timed(str(metric_type), name, observe_func, labels_func, track_in_progress_flag, track_in_progress if track_in_progress_flag else None, in_progress_metric)
def async_timed_function(name: str, metric_type: MetricType=MetricType.HISTOGRAM, labels_func: Optional[Callable[..., Dict[str, str]]]=None, track_in_progress_flag: bool=False, in_progress_metric: Optional[str]=None) -> Callable:
    observe_func = None
    if metric_type == MetricType.HISTOGRAM:
        observe_func = observe_histogram
    elif metric_type == MetricType.SUMMARY:
        observe_func = observe_summary
    else:
        raise ValueError(f'Invalid metric type for timing: {metric_type}')
    return async_timed(str(metric_type), name, observe_func, labels_func, track_in_progress_flag, track_in_progress if track_in_progress_flag else None, in_progress_metric)
def get_current_metrics() -> Dict[str, Dict[str, Any]]:
    result = {}
    for name, counter in _counters.items():
        result[name] = {'type': 'counter', 'description': counter.description, 'values': {}}
    for name, gauge in _gauges.items():
        result[name] = {'type': 'gauge', 'description': gauge.description, 'values': {}}
    for name, histogram in _histograms.items():
        result[name] = {'type': 'histogram', 'description': histogram.description, 'values': {}}
    for name, summary in _summaries.items():
        result[name] = {'type': 'summary', 'description': summary.description, 'values': {}}
    return result