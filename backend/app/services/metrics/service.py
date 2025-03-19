# backend/app/services/metrics/service.py
"""Main metrics service implementation.

This module provides the primary MetricsService that coordinates and manages
metric collection, storage, and reporting.
"""
from __future__ import annotations

import asyncio
import uuid
from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, cast

from app.core.config import settings
from app.core.logging import get_logger
from app.services.interfaces import ServiceInterface
from app.services.metrics.base import (
    MetricName,
    MetricTag,
    MetricType,
    MetricsConfig,
)
from app.services.metrics.collectors import (
    CounterCollector,
    GaugeCollector,
    HistogramCollector,
    SummaryCollector,
)
from app.services.metrics.decorators import async_timed, timed
from app.services.metrics.prometheus import PrometheusManager
from app.services.metrics.trackers import (
    CacheTracker,
    DatabaseTracker,
    HttpTracker,
    ServiceTracker,
)

logger = get_logger(__name__)


class MetricsService(ServiceInterface):
    """Service for tracking and exposing application metrics."""

    def __init__(self, config: Optional[MetricsConfig] = None):
        """
        Initialize the metrics service.

        Args:
            config: Optional metrics configuration
        """
        self.config = config or MetricsConfig()

        # Store metric collectors
        self.counters: Dict[str, CounterCollector] = {}
        self.gauges: Dict[str, GaugeCollector] = {}
        self.histograms: Dict[str, HistogramCollector] = {}
        self.summaries: Dict[str, SummaryCollector] = {}

        # Generate a unique instance ID
        self.instance_id = str(uuid.uuid4())[:8]

        # Tracking for in-progress operations
        self.in_progress: Dict[str, Dict[Tuple, int]] = defaultdict(dict)

        # Initialize Prometheus integration
        self.prometheus = PrometheusManager(self.config)

        # Initialize specialized trackers
        self._init_trackers()

        # Flag to determine if the service has been initialized
        self.initialized = False

        logger.info("MetricsService created")

    def _init_trackers(self) -> None:
        """Initialize specialized metric trackers."""
        # Create trackers with references to metric methods
        self.http_tracker = HttpTracker(
            self.increment_counter,
            self.observe_histogram,
            self.increment_counter
        )

        self.db_tracker = DatabaseTracker(
            self.increment_counter,
            self.observe_histogram,
            self.increment_counter
        )

        self.service_tracker = ServiceTracker(
            self.increment_counter,
            self.observe_histogram,
            self.increment_counter
        )

        self.cache_tracker = CacheTracker(
            self.increment_counter,
            self.observe_histogram
        )

    async def initialize(self) -> None:
        """Initialize the metrics service."""
        if self.initialized:
            return

        logger.debug("Initializing metrics service")

        # Create default metrics if enabled
        if self.config.enable_default_metrics:
            self._initialize_default_metrics()

        # Initialize Prometheus integration if enabled
        if self.config.enable_prometheus:
            await self.prometheus.initialize()

        self.initialized = True
        logger.info("Metrics service initialized")

    async def shutdown(self) -> None:
        """Shutdown the metrics service."""
        logger.debug("Shutting down metrics service")

        # Shutdown Prometheus integration
        if self.config.enable_prometheus:
            await self.prometheus.shutdown()

    def _initialize_default_metrics(self) -> None:
        """Initialize default application metrics."""
        # HTTP metrics
        self.create_counter(
            MetricName.HTTP_REQUESTS_TOTAL,
            "Total number of HTTP requests",
            [MetricTag.METHOD, MetricTag.ENDPOINT, MetricTag.STATUS_CODE]
        )

        self.create_histogram(
            MetricName.HTTP_REQUEST_DURATION_SECONDS,
            "HTTP request duration in seconds",
            [MetricTag.METHOD, MetricTag.ENDPOINT]
        )

        self.create_gauge(
            MetricName.HTTP_IN_PROGRESS,
            "Number of HTTP requests in progress",
            [MetricTag.METHOD, MetricTag.ENDPOINT]
        )

        self.create_counter(
            MetricName.HTTP_ERRORS_TOTAL,
            "Total number of HTTP errors",
            [MetricTag.METHOD, MetricTag.ENDPOINT, MetricTag.ERROR_CODE]
        )

        # Database metrics
        self.create_counter(
            MetricName.DB_QUERIES_TOTAL,
            "Total number of database queries",
            [MetricTag.OPERATION, MetricTag.ENTITY]
        )

        self.create_histogram(
            MetricName.DB_QUERY_DURATION_SECONDS,
            "Database query duration in seconds",
            [MetricTag.OPERATION, MetricTag.ENTITY]
        )

        self.create_counter(
            MetricName.DB_ERRORS_TOTAL,
            "Total number of database errors",
            [MetricTag.OPERATION, MetricTag.ENTITY, MetricTag.ERROR_TYPE]
        )

        # Service metrics
        self.create_counter(
            MetricName.SERVICE_CALLS_TOTAL,
            "Total number of service calls",
            [MetricTag.COMPONENT, MetricTag.ACTION]
        )

        self.create_histogram(
            MetricName.SERVICE_CALL_DURATION_SECONDS,
            "Service call duration in seconds",
            [MetricTag.COMPONENT, MetricTag.ACTION]
        )

        self.create_counter(
            MetricName.SERVICE_ERRORS_TOTAL,
            "Total number of service errors",
            [MetricTag.COMPONENT, MetricTag.ACTION, MetricTag.ERROR_TYPE]
        )

        # Cache metrics
        self.create_counter(
            MetricName.CACHE_HIT_TOTAL,
            "Total number of cache hits",
            [MetricTag.CACHE_BACKEND, MetricTag.COMPONENT]
        )

        self.create_counter(
            MetricName.CACHE_MISS_TOTAL,
            "Total number of cache misses",
            [MetricTag.CACHE_BACKEND, MetricTag.COMPONENT]
        )

        self.create_histogram(
            MetricName.CACHE_OPERATION_DURATION_SECONDS,
            "Cache operation duration in seconds",
            [MetricTag.CACHE_BACKEND, MetricTag.OPERATION]
        )

        # System metrics if process metrics enabled
        if self.config.enable_process_metrics:
            self.create_gauge(
                MetricName.PROCESS_RESIDENT_MEMORY_BYTES,
                "Resident memory size in bytes",
                []
            )

            self.create_gauge(
                MetricName.PROCESS_VIRTUAL_MEMORY_BYTES,
                "Virtual memory size in bytes",
                []
            )

            self.create_counter(
                MetricName.PROCESS_CPU_SECONDS_TOTAL,
                "Total user and system CPU time spent in seconds",
                []
            )

            self.create_gauge(
                MetricName.PROCESS_OPEN_FDS,
                "Number of open file descriptors",
                []
            )

    def create_counter(
        self,
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
        namespace = namespace or self.config.namespace
        subsystem = subsystem or self.config.subsystem

        if name not in self.counters:
            self.counters[name] = CounterCollector(
                name=name,
                description=description,
                labelnames=labelnames or [],
                namespace=namespace,
                subsystem=subsystem
            )

        return self.counters[name]

    def create_gauge(
        self,
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
        namespace = namespace or self.config.namespace
        subsystem = subsystem or self.config.subsystem

        if name not in self.gauges:
            self.gauges[name] = GaugeCollector(
                name=name,
                description=description,
                labelnames=labelnames or [],
                namespace=namespace,
                subsystem=subsystem
            )

        return self.gauges[name]

    def create_histogram(
        self,
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
        namespace = namespace or self.config.namespace
        subsystem = subsystem or self.config.subsystem
        buckets = buckets or self.config.default_buckets

        if name not in self.histograms:
            self.histograms[name] = HistogramCollector(
                name=name,
                description=description,
                labelnames=labelnames or [],
                buckets=buckets,
                namespace=namespace,
                subsystem=subsystem
            )

        return self.histograms[name]

    def create_summary(
        self,
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
        namespace = namespace or self.config.namespace
        subsystem = subsystem or self.config.subsystem

        if name not in self.summaries:
            self.summaries[name] = SummaryCollector(
                name=name,
                description=description,
                labelnames=labelnames or [],
                namespace=namespace,
                subsystem=subsystem
            )

        return self.summaries[name]

    def increment_counter(
        self,
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
        if name not in self.counters:
            logger.warning(f"Counter {name} not found, skipping increment")
            return

        self.counters[name].increment(amount, labels)

    def set_gauge(
        self,
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
        if name not in self.gauges:
            logger.warning(f"Gauge {name} not found, skipping set")
            return

        self.gauges[name].set(value, labels)

    def observe_histogram(
        self,
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
        if name not in self.histograms:
            logger.warning(f"Histogram {name} not found, skipping observation")
            return

        self.histograms[name].observe(value, labels)

    def observe_summary(
        self,
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
        if name not in self.summaries:
            logger.warning(f"Summary {name} not found, skipping observation")
            return

        self.summaries[name].observe(value, labels)

    def track_in_progress(
        self,
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
        if metric_name not in self.gauges:
            logger.warning(f"Gauge {metric_name} not found, skipping in-progress tracking")
            return

        # Create a tuple of label values to use as a dictionary key
        labels_key = tuple(sorted(labels.items()))

        # Get the current count for these labels
        current = self.in_progress[metric_name].get(labels_key, 0)

        # Update the count
        new_count = max(0, current + count)  # Ensure never negative

        # Store the updated count
        self.in_progress[metric_name][labels_key] = new_count

        # Update the gauge
        self.set_gauge(metric_name, new_count, labels)

    # Convenience methods for trackers
    def track_request(
        self,
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
        self.http_tracker.track_request(method, endpoint, status_code, duration, error_code)

    def track_db_query(
        self,
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
        self.db_tracker.track_query(operation, entity, duration, error)

    def track_service_call(
        self,
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
        self.service_tracker.track_call(component, action, duration, error)

    def track_cache_operation(
        self,
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
        self.cache_tracker.track_operation(operation, backend, hit, duration, component)

    # Decorator factories
    def timed(
        self,
        name: str,
        metric_type: MetricType = MetricType.HISTOGRAM,
        labels_func: Optional[Callable[..., Dict[str, str]]] = None,
        track_in_progress: bool = False,
        in_progress_metric: Optional[str] = None,
    ) -> Callable:
        """
        Create a decorator for timing function execution.

        Args:
            name: Metric name
            metric_type: Type of metric (histogram or summary)
            labels_func: Optional function to generate label values from function args
            track_in_progress: Whether to track in-progress operations
            in_progress_metric: Optional name of gauge metric for tracking in-progress operations

        Returns:
            Decorator function
        """
        observe_func = None
        if metric_type == MetricType.HISTOGRAM:
            observe_func = self.observe_histogram
        elif metric_type == MetricType.SUMMARY:
            observe_func = self.observe_summary
        else:
            raise ValueError(f"Invalid metric type for timing: {metric_type}")

        return timed(
            str(metric_type),
            name,
            observe_func,
            labels_func,
            track_in_progress,
            self.track_in_progress if track_in_progress else None,
            in_progress_metric
        )

    def async_timed(
        self,
        name: str,
        metric_type: MetricType = MetricType.HISTOGRAM,
        labels_func: Optional[Callable[..., Dict[str, str]]] = None,
        track_in_progress: bool = False,
        in_progress_metric: Optional[str] = None,
    ) -> Callable:
        """
        Create a decorator for timing async function execution.

        Args:
            name: Metric name
            metric_type: Type of metric (histogram or summary)
            labels_func: Optional function to generate label values from function args
            track_in_progress: Whether to track in-progress operations
            in_progress_metric: Optional name of gauge metric for tracking in-progress operations

        Returns:
            Decorator function
        """
        observe_func = None
        if metric_type == MetricType.HISTOGRAM:
            observe_func = self.observe_histogram
        elif metric_type == MetricType.SUMMARY:
            observe_func = self.observe_summary
        else:
            raise ValueError(f"Invalid metric type for timing: {metric_type}")

        return async_timed(
            str(metric_type),
            name,
            observe_func,
            labels_func,
            track_in_progress,
            self.track_in_progress if track_in_progress else None,
            in_progress_metric
        )

    def get_current_metrics(self) -> Dict[str, Dict[str, Any]]:
        """
        Get the current values of all metrics.

        Returns:
            Dictionary of metric values by name
        """
        result = {}

        # Get counter values
        for name, counter in self.counters.items():
            result[name] = {
                "type": "counter",
                "description": counter.description,
                # We don't have direct access to values in this refactoring
                # In real implementation, we'd expose a get_values method on collectors
                "values": {}
            }

        # Get gauge values
        for name, gauge in self.gauges.items():
            result[name] = {
                "type": "gauge",
                "description": gauge.description,
                "values": {}
            }

        # Get histogram values
        for name, histogram in self.histograms.items():
            result[name] = {
                "type": "histogram",
                "description": histogram.description,
                "values": {}
            }

        # Get summary values
        for name, summary in self.summaries.items():
            result[name] = {
                "type": "summary",
                "description": summary.description,
                "values": {}
            }

        return result
