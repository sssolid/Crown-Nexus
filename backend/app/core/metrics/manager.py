# /app/core/metrics/manager.py
"""Core metrics functionality.

This module provides the main metrics functionality for collecting, tracking,
and exposing application metrics for monitoring and performance analysis.
"""
from __future__ import annotations

import asyncio
import uuid
from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, cast

from app.core.config import settings
from app.core.logging import get_logger
from app.core.metrics.base import (
    MetricName,
    MetricTag,
    MetricType,
    MetricsConfig,
)
from app.core.metrics.collectors import (
    CounterCollector,
    GaugeCollector,
    HistogramCollector,
    SummaryCollector,
)
from app.core.metrics.decorators import async_timed, timed
from app.core.metrics.prometheus import PrometheusManager
from app.core.metrics.trackers import (
    CacheTracker,
    DatabaseTracker,
    HttpTracker,
    ServiceTracker,
)

logger = get_logger(__name__)

# Global configuration
_config: MetricsConfig = MetricsConfig()

# Store metric collectors
_counters: Dict[str, CounterCollector] = {}
_gauges: Dict[str, GaugeCollector] = {}
_histograms: Dict[str, HistogramCollector] = {}
_summaries: Dict[str, SummaryCollector] = {}

# Generate a unique instance ID
_instance_id = str(uuid.uuid4())[:8]

# Tracking for in-progress operations
_in_progress: Dict[str, Dict[Tuple, int]] = defaultdict(dict)

# Prometheus integration
_prometheus: Optional[PrometheusManager] = None

# Specialized trackers
_http_tracker: Optional[HttpTracker] = None
_db_tracker: Optional[DatabaseTracker] = None
_service_tracker: Optional[ServiceTracker] = None
_cache_tracker: Optional[CacheTracker] = None

# Initialization flag
_initialized = False


def _init_trackers() -> None:
    """Initialize specialized metric trackers."""
    global _http_tracker, _db_tracker, _service_tracker, _cache_tracker

    # Create trackers with references to metric methods
    _http_tracker = HttpTracker(increment_counter, observe_histogram, increment_counter)

    _db_tracker = DatabaseTracker(
        increment_counter, observe_histogram, increment_counter
    )

    _service_tracker = ServiceTracker(
        increment_counter, observe_histogram, increment_counter
    )

    _cache_tracker = CacheTracker(increment_counter, observe_histogram)


def _initialize_default_metrics() -> None:
    """Initialize default application metrics."""
    # HTTP metrics
    create_counter(
        MetricName.HTTP_REQUESTS_TOTAL,
        "Total number of HTTP requests",
        [MetricTag.METHOD, MetricTag.ENDPOINT, MetricTag.STATUS_CODE],
    )

    create_histogram(
        MetricName.HTTP_REQUEST_DURATION_SECONDS,
        "HTTP request duration in seconds",
        [MetricTag.METHOD, MetricTag.ENDPOINT],
    )

    create_gauge(
        MetricName.HTTP_IN_PROGRESS,
        "Number of HTTP requests in progress",
        [MetricTag.METHOD, MetricTag.ENDPOINT],
    )

    create_counter(
        MetricName.HTTP_ERRORS_TOTAL,
        "Total number of HTTP errors",
        [MetricTag.METHOD, MetricTag.ENDPOINT, MetricTag.ERROR_CODE],
    )

    # Database metrics
    create_counter(
        MetricName.DB_QUERIES_TOTAL,
        "Total number of database queries",
        [MetricTag.OPERATION, MetricTag.ENTITY],
    )

    create_histogram(
        MetricName.DB_QUERY_DURATION_SECONDS,
        "Database query duration in seconds",
        [MetricTag.OPERATION, MetricTag.ENTITY],
    )

    create_counter(
        MetricName.DB_ERRORS_TOTAL,
        "Total number of database errors",
        [MetricTag.OPERATION, MetricTag.ENTITY, MetricTag.ERROR_TYPE],
    )

    # Service metrics
    create_counter(
        MetricName.SERVICE_CALLS_TOTAL,
        "Total number of service calls",
        [MetricTag.COMPONENT, MetricTag.ACTION],
    )

    create_histogram(
        MetricName.SERVICE_CALL_DURATION_SECONDS,
        "Service call duration in seconds",
        [MetricTag.COMPONENT, MetricTag.ACTION],
    )

    create_counter(
        MetricName.SERVICE_ERRORS_TOTAL,
        "Total number of service errors",
        [MetricTag.COMPONENT, MetricTag.ACTION, MetricTag.ERROR_TYPE],
    )

    # Cache metrics
    create_counter(
        MetricName.CACHE_HIT_TOTAL,
        "Total number of cache hits",
        [MetricTag.CACHE_BACKEND, MetricTag.COMPONENT],
    )

    create_counter(
        MetricName.CACHE_MISS_TOTAL,
        "Total number of cache misses",
        [MetricTag.CACHE_BACKEND, MetricTag.COMPONENT],
    )

    create_histogram(
        MetricName.CACHE_OPERATION_DURATION_SECONDS,
        "Cache operation duration in seconds",
        [MetricTag.CACHE_BACKEND, MetricTag.OPERATION],
    )

    # System metrics if process metrics enabled
    if _config.enable_process_metrics:
        create_gauge(
            MetricName.PROCESS_RESIDENT_MEMORY_BYTES,
            "Resident memory size in bytes",
            [],
        )

        create_gauge(
            MetricName.PROCESS_VIRTUAL_MEMORY_BYTES,
            "Virtual memory size in bytes",
            [],
        )

        create_counter(
            MetricName.PROCESS_CPU_SECONDS_TOTAL,
            "Total user and system CPU time spent in seconds",
            [],
        )

        create_gauge(MetricName.PROCESS_OPEN_FDS, "Number of open file descriptors", [])


async def initialize(config: Optional[MetricsConfig] = None) -> None:
    """Initialize the metrics system.

    Args:
        config: Optional metrics configuration
    """
    global _config, _prometheus, _initialized

    if _initialized:
        return

    logger.debug("Initializing metrics system")

    # Set configuration
    if config:
        _config = config

    # Initialize trackers
    _init_trackers()

    # Create default metrics if enabled
    if _config.enable_default_metrics:
        _initialize_default_metrics()

    # Initialize Prometheus integration if enabled
    if _config.enable_prometheus:
        _prometheus = PrometheusManager(_config)
        await _prometheus.initialize()

    _initialized = True
    logger.info("Metrics system initialized")


async def shutdown() -> None:
    """Shutdown the metrics system."""
    global _prometheus, _initialized

    logger.debug("Shutting down metrics system")

    # Shutdown Prometheus integration
    if _prometheus and _config.enable_prometheus:
        await _prometheus.shutdown()

    _initialized = False


def create_counter(
    name: str,
    description: str,
    labelnames: Optional[List[str]] = None,
    namespace: Optional[str] = None,
    subsystem: Optional[str] = None,
) -> CounterCollector:
    """
    Create a new counter metric.

    Args:
        name: Metric name
        description: Metric description
        labelnames: Optional list of label names
        namespace: Optional metric namespace
        subsystem: Optional metric subsystem

    Returns:
        CounterCollector object
    """
    namespace = namespace or _config.namespace
    subsystem = subsystem or _config.subsystem

    if name not in _counters:
        _counters[name] = CounterCollector(
            name=name,
            description=description,
            labelnames=labelnames or [],
            namespace=namespace,
            subsystem=subsystem,
        )

    return _counters[name]


def create_gauge(
    name: str,
    description: str,
    labelnames: Optional[List[str]] = None,
    namespace: Optional[str] = None,
    subsystem: Optional[str] = None,
) -> GaugeCollector:
    """
    Create a new gauge metric.

    Args:
        name: Metric name
        description: Metric description
        labelnames: Optional list of label names
        namespace: Optional metric namespace
        subsystem: Optional metric subsystem

    Returns:
        GaugeCollector object
    """
    namespace = namespace or _config.namespace
    subsystem = subsystem or _config.subsystem

    if name not in _gauges:
        _gauges[name] = GaugeCollector(
            name=name,
            description=description,
            labelnames=labelnames or [],
            namespace=namespace,
            subsystem=subsystem,
        )

    return _gauges[name]


def create_histogram(
    name: str,
    description: str,
    labelnames: Optional[List[str]] = None,
    buckets: Optional[List[float]] = None,
    namespace: Optional[str] = None,
    subsystem: Optional[str] = None,
) -> HistogramCollector:
    """
    Create a new histogram metric.

    Args:
        name: Metric name
        description: Metric description
        labelnames: Optional list of label names
        buckets: Optional histogram buckets
        namespace: Optional metric namespace
        subsystem: Optional metric subsystem

    Returns:
        HistogramCollector object
    """
    namespace = namespace or _config.namespace
    subsystem = subsystem or _config.subsystem
    buckets = buckets or _config.default_buckets

    if name not in _histograms:
        _histograms[name] = HistogramCollector(
            name=name,
            description=description,
            labelnames=labelnames or [],
            buckets=buckets,
            namespace=namespace,
            subsystem=subsystem,
        )

    return _histograms[name]


def create_summary(
    name: str,
    description: str,
    labelnames: Optional[List[str]] = None,
    namespace: Optional[str] = None,
    subsystem: Optional[str] = None,
) -> SummaryCollector:
    """
    Create a new summary metric.

    Args:
        name: Metric name
        description: Metric description
        labelnames: Optional list of label names
        namespace: Optional metric namespace
        subsystem: Optional metric subsystem

    Returns:
        SummaryCollector object
    """
    namespace = namespace or _config.namespace
    subsystem = subsystem or _config.subsystem

    if name not in _summaries:
        _summaries[name] = SummaryCollector(
            name=name,
            description=description,
            labelnames=labelnames or [],
            namespace=namespace,
            subsystem=subsystem,
        )

    return _summaries[name]


def increment_counter(
    name: str,
    amount: float = 1.0,
    labels: Optional[Dict[str, str]] = None,
) -> None:
    """
    Increment a counter metric.

    Args:
        name: Metric name
        amount: Amount to increment by
        labels: Optional label values
    """
    if name not in _counters:
        logger.warning(f"Counter {name} not found, skipping increment")
        return

    _counters[name].increment(amount, labels)


def set_gauge(
    name: str,
    value: float,
    labels: Optional[Dict[str, str]] = None,
) -> None:
    """
    Set a gauge metric value.

    Args:
        name: Metric name
        value: Value to set
        labels: Optional label values
    """
    if name not in _gauges:
        logger.warning(f"Gauge {name} not found, skipping set")
        return

    _gauges[name].set(value, labels)


def observe_histogram(
    name: str,
    value: float,
    labels: Optional[Dict[str, str]] = None,
) -> None:
    """
    Record an observation in a histogram metric.

    Args:
        name: Metric name
        value: Value to observe
        labels: Optional label values
    """
    if name not in _histograms:
        logger.warning(f"Histogram {name} not found, skipping observation")
        return

    _histograms[name].observe(value, labels)


def observe_summary(
    name: str,
    value: float,
    labels: Optional[Dict[str, str]] = None,
) -> None:
    """
    Record an observation in a summary metric.

    Args:
        name: Metric name
        value: Value to observe
        labels: Optional label values
    """
    if name not in _summaries:
        logger.warning(f"Summary {name} not found, skipping observation")
        return

    _summaries[name].observe(value, labels)


def track_in_progress(
    metric_name: str,
    labels: Dict[str, str],
    count: int = 1,
) -> None:
    """
    Track in-progress operations using gauges.

    Args:
        metric_name: Name of the gauge metric to update
        labels: Label values that uniquely identify the operation
        count: Number to adjust the gauge by (1 for start, -1 for end)
    """
    if metric_name not in _gauges:
        logger.warning(f"Gauge {metric_name} not found, skipping in-progress tracking")
        return

    # Create a tuple of label values to use as a dictionary key
    labels_key = tuple(sorted(labels.items()))

    # Get the current count for these labels
    current = _in_progress[metric_name].get(labels_key, 0)

    # Update the count
    new_count = max(0, current + count)  # Ensure never negative

    # Store the updated count
    _in_progress[metric_name][labels_key] = new_count

    # Update the gauge
    set_gauge(metric_name, new_count, labels)


# Convenience methods for trackers
def track_request(
    method: str,
    endpoint: str,
    status_code: int,
    duration: float,
    error_code: Optional[str] = None,
) -> None:
    """
    Track HTTP request metrics.

    Args:
        method: HTTP method
        endpoint: Request endpoint
        status_code: Response status code
        duration: Request duration in seconds
        error_code: Optional error code if request failed
    """
    if _http_tracker:
        _http_tracker.track_request(method, endpoint, status_code, duration, error_code)


def track_db_query(
    operation: str,
    entity: str,
    duration: float,
    error: Optional[str] = None,
) -> None:
    """
    Track database query metrics.

    Args:
        operation: Database operation (e.g., SELECT, INSERT)
        entity: Entity being queried
        duration: Query duration in seconds
        error: Optional error message if query failed
    """
    if _db_tracker:
        _db_tracker.track_query(operation, entity, duration, error)


def track_service_call(
    component: str,
    action: str,
    duration: float,
    error: Optional[str] = None,
) -> None:
    """
    Track service call metrics.

    Args:
        component: Service component name
        action: Action being performed
        duration: Call duration in seconds
        error: Optional error message if call failed
    """
    if _service_tracker:
        _service_tracker.track_call(component, action, duration, error)


def track_cache_operation(
    operation: str,
    backend: str,
    hit: bool,
    duration: float,
    component: str = "unknown",
) -> None:
    """
    Track cache operation metrics.

    Args:
        operation: Cache operation (get, set, delete)
        backend: Cache backend (memory, redis)
        hit: Whether the operation was a cache hit
        duration: Operation duration in seconds
        component: Component using the cache
    """
    if _cache_tracker:
        _cache_tracker.track_operation(operation, backend, hit, duration, component)


# Decorator factories
def timed_function(
    name: str,
    metric_type: MetricType = MetricType.HISTOGRAM,
    labels_func: Optional[Callable[..., Dict[str, str]]] = None,
    track_in_progress_flag: bool = False,
    in_progress_metric: Optional[str] = None,
) -> Callable:
    """
    Create a decorator for timing function execution.

    Args:
        name: Metric name
        metric_type: Type of metric (histogram or summary)
        labels_func: Optional function to generate label values from function args
        track_in_progress_flag: Whether to track in-progress operations
        in_progress_metric: Optional name of gauge metric for tracking in-progress operations

    Returns:
        Decorator function
    """
    observe_func = None
    if metric_type == MetricType.HISTOGRAM:
        observe_func = observe_histogram
    elif metric_type == MetricType.SUMMARY:
        observe_func = observe_summary
    else:
        raise ValueError(f"Invalid metric type for timing: {metric_type}")

    return timed(
        str(metric_type),
        name,
        observe_func,
        labels_func,
        track_in_progress_flag,
        track_in_progress if track_in_progress_flag else None,
        in_progress_metric,
    )


def async_timed_function(
    name: str,
    metric_type: MetricType = MetricType.HISTOGRAM,
    labels_func: Optional[Callable[..., Dict[str, str]]] = None,
    track_in_progress_flag: bool = False,
    in_progress_metric: Optional[str] = None,
) -> Callable:
    """
    Create a decorator for timing async function execution.

    Args:
        name: Metric name
        metric_type: Type of metric (histogram or summary)
        labels_func: Optional function to generate label values from function args
        track_in_progress_flag: Whether to track in-progress operations
        in_progress_metric: Optional name of gauge metric for tracking in-progress operations

    Returns:
        Decorator function
    """
    observe_func = None
    if metric_type == MetricType.HISTOGRAM:
        observe_func = observe_histogram
    elif metric_type == MetricType.SUMMARY:
        observe_func = observe_summary
    else:
        raise ValueError(f"Invalid metric type for timing: {metric_type}")

    return async_timed(
        str(metric_type),
        name,
        observe_func,
        labels_func,
        track_in_progress_flag,
        track_in_progress if track_in_progress_flag else None,
        in_progress_metric,
    )


def get_current_metrics() -> Dict[str, Dict[str, Any]]:
    """
    Get the current values of all metrics.

    Returns:
        Dictionary of metric values by name
    """
    result = {}

    # Get counter values
    for name, counter in _counters.items():
        result[name] = {
            "type": "counter",
            "description": counter.description,
            # We don't have direct access to values in this refactoring
            # In real implementation, we'd expose a get_values method on collectors
            "values": {},
        }

    # Get gauge values
    for name, gauge in _gauges.items():
        result[name] = {
            "type": "gauge",
            "description": gauge.description,
            "values": {},
        }

    # Get histogram values
    for name, histogram in _histograms.items():
        result[name] = {
            "type": "histogram",
            "description": histogram.description,
            "values": {},
        }

    # Get summary values
    for name, summary in _summaries.items():
        result[name] = {
            "type": "summary",
            "description": summary.description,
            "values": {},
        }

    return result
