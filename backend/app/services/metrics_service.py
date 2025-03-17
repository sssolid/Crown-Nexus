# app/services/metrics_service.py
from __future__ import annotations

import asyncio
import inspect
import time
import uuid
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum
from functools import wraps
from typing import Any, Callable, Dict, Generator, List, Optional, Set, Tuple, TypeVar, Union, cast

from fastapi import Depends, Request, Response
from fastapi.routing import APIRoute
from prometheus_client import (
    REGISTRY,
    Counter,
    Gauge,
    Histogram,
    Summary,
    start_http_server,
    push_to_gateway
)

from app.core.config import settings
from app.core.logging import get_logger
from app.services.interfaces import ServiceInterface

logger = get_logger("app.services.metrics_service")
F = TypeVar("F", bound=Callable[..., Any])


class MetricType(str, Enum):
    """Enum for different types of metrics."""

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


@dataclass
class MetricsConfig:
    """Configuration for the metrics service."""

    namespace: str = "crown_nexus"
    subsystem: str = "api"
    default_labels: Dict[str, str] = field(default_factory=dict)
    default_buckets: List[float] = field(default_factory=lambda: [
        0.001, 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0
    ])
    enable_prometheus: bool = True
    enable_endpoint: bool = True
    endpoint_port: int = 9090
    push_gateway: Optional[str] = None
    push_interval: int = 60  # seconds
    enable_default_metrics: bool = True
    enable_process_metrics: bool = True
    enable_platform_metrics: bool = True


class MetricTag:
    """Common metric tag names for consistent labeling."""

    # Standard tags
    SERVICE = "service"
    ENVIRONMENT = "environment"
    VERSION = "version"
    INSTANCE = "instance"

    # API tags
    ENDPOINT = "endpoint"
    METHOD = "method"
    PATH = "path"
    STATUS_CODE = "status_code"

    # Database tags
    OPERATION = "operation"
    ENTITY = "entity"
    QUERY_TYPE = "query_type"

    # Service tags
    COMPONENT = "component"
    ACTION = "action"

    # Error tags
    ERROR_TYPE = "error_type"
    ERROR_CODE = "error_code"

    # Resource tags
    RESOURCE_TYPE = "resource_type"
    RESOURCE_ID = "resource_id"

    # User tags
    USER_ID = "user_id"
    USER_ROLE = "user_role"

    # Cache tags
    CACHE_HIT = "cache_hit"
    CACHE_BACKEND = "cache_backend"


class MetricName:
    """Common metric names for consistent measurement."""

    # HTTP metrics
    HTTP_REQUESTS_TOTAL = "http_requests_total"
    HTTP_REQUEST_DURATION_SECONDS = "http_request_duration_seconds"
    HTTP_REQUEST_SIZE_BYTES = "http_request_size_bytes"
    HTTP_RESPONSE_SIZE_BYTES = "http_response_size_bytes"
    HTTP_ERRORS_TOTAL = "http_errors_total"
    HTTP_IN_PROGRESS = "http_requests_in_progress"

    # Database metrics
    DB_QUERIES_TOTAL = "db_queries_total"
    DB_QUERY_DURATION_SECONDS = "db_query_duration_seconds"
    DB_CONNECTIONS_TOTAL = "db_connections_total"
    DB_CONNECTIONS_IN_USE = "db_connections_in_use"
    DB_TRANSACTION_DURATION_SECONDS = "db_transaction_duration_seconds"
    DB_ERRORS_TOTAL = "db_errors_total"

    # Service metrics
    SERVICE_CALLS_TOTAL = "service_calls_total"
    SERVICE_CALL_DURATION_SECONDS = "service_call_duration_seconds"
    SERVICE_ERRORS_TOTAL = "service_errors_total"

    # Cache metrics
    CACHE_HIT_TOTAL = "cache_hit_total"
    CACHE_MISS_TOTAL = "cache_miss_total"
    CACHE_OPERATIONS_TOTAL = "cache_operations_total"
    CACHE_OPERATION_DURATION_SECONDS = "cache_operation_duration_seconds"

    # Business metrics
    USER_LOGINS_TOTAL = "user_logins_total"
    ORDERS_TOTAL = "orders_total"
    PRODUCTS_CREATED_TOTAL = "products_created_total"

    # System metrics
    SYSTEM_MEMORY_BYTES = "system_memory_bytes"
    SYSTEM_CPU_USAGE = "system_cpu_usage"
    SYSTEM_DISK_USAGE_BYTES = "system_disk_usage_bytes"

    # Process metrics
    PROCESS_RESIDENT_MEMORY_BYTES = "process_resident_memory_bytes"
    PROCESS_VIRTUAL_MEMORY_BYTES = "process_virtual_memory_bytes"
    PROCESS_CPU_SECONDS_TOTAL = "process_cpu_seconds_total"
    PROCESS_OPEN_FDS = "process_open_fds"


class MetricsService:
    """Service for tracking and exposing application metrics.

    Provides methods for recording metrics and exposing them to
    monitoring systems like Prometheus.
    """

    def __init__(self, config: Optional[MetricsConfig] = None) -> None:
        """Initialize the metrics service.

        Args:
            config: Optional metrics configuration
        """
        self.logger = logger
        self.config = config or MetricsConfig()

        # Store metric objects
        self.counters: Dict[str, Counter] = {}
        self.gauges: Dict[str, Gauge] = {}
        self.histograms: Dict[str, Histogram] = {}
        self.summaries: Dict[str, Summary] = {}

        # Generate a unique instance ID
        self.instance_id = str(uuid.uuid4())[:8]

        # Tracking for in-progress requests and operations
        self.in_progress: Dict[str, Dict[Tuple, int]] = defaultdict(dict)

        # Flag to determine if the service has been initialized
        self.initialized = False

        logger.info("MetricsService created")

    async def initialize(self) -> None:
        """Initialize the metrics service."""
        self.logger.debug("Initializing metrics service")

        # Create default metrics if enabled
        if self.config.enable_default_metrics:
            self._initialize_default_metrics()

        # Start Prometheus HTTP server if enabled
        if self.config.enable_prometheus and self.config.enable_endpoint:
            try:
                start_http_server(self.config.endpoint_port)
                self.logger.info(f"Prometheus metrics endpoint started on port {self.config.endpoint_port}")
            except Exception as e:
                self.logger.error(f"Failed to start Prometheus HTTP server: {str(e)}")

        # Start metrics pushing if push gateway is configured
        if self.config.enable_prometheus and self.config.push_gateway:
            asyncio.create_task(self._start_push_loop())

        self.initialized = True

    async def shutdown(self) -> None:
        """Shutdown the metrics service."""
        self.logger.debug("Shutting down metrics service")

        # Final push to gateway if configured
        if self.config.enable_prometheus and self.config.push_gateway:
            try:
                push_to_gateway(
                    self.config.push_gateway,
                    job=self.config.namespace,
                    registry=REGISTRY
                )
                self.logger.info(f"Final metrics push to gateway: {self.config.push_gateway}")
            except Exception as e:
                self.logger.error(f"Failed to push metrics to gateway: {str(e)}")

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

        # System metrics
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

    async def _start_push_loop(self) -> None:
        """Start loop to periodically push metrics to gateway."""
        self.logger.info(f"Starting metrics push loop (interval: {self.config.push_interval}s)")

        while True:
            try:
                # Update process metrics before pushing
                if self.config.enable_process_metrics:
                    self._update_process_metrics()

                # Push metrics to gateway
                push_to_gateway(
                    self.config.push_gateway,
                    job=self.config.namespace,
                    registry=REGISTRY
                )
                self.logger.debug(f"Pushed metrics to gateway: {self.config.push_gateway}")
            except Exception as e:
                self.logger.error(f"Failed to push metrics to gateway: {str(e)}")

            # Wait for next push interval
            await asyncio.sleep(self.config.push_interval)

    def _update_process_metrics(self) -> None:
        """Update process metrics like memory usage and CPU time."""
        try:
            import os
            import psutil

            process = psutil.Process(os.getpid())

            # Update memory metrics
            memory_info = process.memory_info()
            self.set_gauge(
                MetricName.PROCESS_RESIDENT_MEMORY_BYTES,
                memory_info.rss
            )
            self.set_gauge(
                MetricName.PROCESS_VIRTUAL_MEMORY_BYTES,
                memory_info.vms
            )

            # Update CPU metrics
            cpu_times = process.cpu_times()
            self.set_gauge(
                MetricName.PROCESS_CPU_SECONDS_TOTAL,
                cpu_times.user + cpu_times.system
            )

            # Update file descriptors
            if hasattr(process, 'num_fds'):
                self.set_gauge(
                    MetricName.PROCESS_OPEN_FDS,
                    process.num_fds()
                )
        except ImportError:
            self.logger.warning("psutil not installed, skipping process metrics update")
        except Exception as e:
            self.logger.error(f"Error updating process metrics: {str(e)}")

    def create_counter(
        self,
        name: str,
        description: str,
        labelnames: Optional[List[str]] = None,
        namespace: Optional[str] = None,
        subsystem: Optional[str] = None,
    ) -> Counter:
        """Create a new counter metric.

        Args:
            name: Metric name
            description: Metric description
            labelnames: Optional list of label names
            namespace: Optional metric namespace
            subsystem: Optional metric subsystem

        Returns:
            Prometheus Counter object
        """
        namespace = namespace or self.config.namespace
        subsystem = subsystem or self.config.subsystem

        if name not in self.counters:
            self.counters[name] = Counter(
                name=name,
                documentation=description,
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
    ) -> Gauge:
        """Create a new gauge metric.

        Args:
            name: Metric name
            description: Metric description
            labelnames: Optional list of label names
            namespace: Optional metric namespace
            subsystem: Optional metric subsystem

        Returns:
            Prometheus Gauge object
        """
        namespace = namespace or self.config.namespace
        subsystem = subsystem or self.config.subsystem

        if name not in self.gauges:
            self.gauges[name] = Gauge(
                name=name,
                documentation=description,
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
    ) -> Histogram:
        """Create a new histogram metric.

        Args:
            name: Metric name
            description: Metric description
            labelnames: Optional list of label names
            buckets: Optional histogram buckets
            namespace: Optional metric namespace
            subsystem: Optional metric subsystem

        Returns:
            Prometheus Histogram object
        """
        namespace = namespace or self.config.namespace
        subsystem = subsystem or self.config.subsystem
        buckets = buckets or self.config.default_buckets

        if name not in self.histograms:
            self.histograms[name] = Histogram(
                name=name,
                documentation=description,
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
    ) -> Summary:
        """Create a new summary metric.

        Args:
            name: Metric name
            description: Metric description
            labelnames: Optional list of label names
            namespace: Optional metric namespace
            subsystem: Optional metric subsystem

        Returns:
            Prometheus Summary object
        """
        namespace = namespace or self.config.namespace
        subsystem = subsystem or self.config.subsystem

        if name not in self.summaries:
            self.summaries[name] = Summary(
                name=name,
                documentation=description,
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
        """Increment a counter metric.

        Args:
            name: Metric name
            amount: Amount to increment by
            labels: Optional label values
        """
        if name not in self.counters:
            self.logger.warning(f"Counter {name} not found, skipping increment")
            return

        counter = self.counters[name]

        try:
            if labels:
                counter.labels(**labels).inc(amount)
            else:
                counter.inc(amount)
        except Exception as e:
            self.logger.error(f"Error incrementing counter {name}: {str(e)}")

    def set_gauge(
        self,
        name: str,
        value: float,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """Set a gauge metric value.

        Args:
            name: Metric name
            value: Value to set
            labels: Optional label values
        """
        if name not in self.gauges:
            self.logger.warning(f"Gauge {name} not found, skipping set")
            return

        gauge = self.gauges[name]

        try:
            if labels:
                gauge.labels(**labels).set(value)
            else:
                gauge.set(value)
        except Exception as e:
            self.logger.error(f"Error setting gauge {name}: {str(e)}")

    def observe_histogram(
        self,
        name: str,
        value: float,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """Record an observation in a histogram metric.

        Args:
            name: Metric name
            value: Value to observe
            labels: Optional label values
        """
        if name not in self.histograms:
            self.logger.warning(f"Histogram {name} not found, skipping observation")
            return

        histogram = self.histograms[name]

        try:
            if labels:
                histogram.labels(**labels).observe(value)
            else:
                histogram.observe(value)
        except Exception as e:
            self.logger.error(f"Error observing histogram {name}: {str(e)}")

    def observe_summary(
        self,
        name: str,
        value: float,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """Record an observation in a summary metric.

        Args:
            name: Metric name
            value: Value to observe
            labels: Optional label values
        """
        if name not in self.summaries:
            self.logger.warning(f"Summary {name} not found, skipping observation")
            return

        summary = self.summaries[name]

        try:
            if labels:
                summary.labels(**labels).observe(value)
            else:
                summary.observe(value)
        except Exception as e:
            self.logger.error(f"Error observing summary {name}: {str(e)}")

    def track_in_progress(
        self,
        metric_name: str,
        labels: Dict[str, str],
        count: int = 1,
    ) -> None:
        """Track in-progress operations.

        Args:
            metric_name: Name of the gauge metric to update
            labels: Label values that uniquely identify the operation
            count: Number to adjust the gauge by (1 for start, -1 for end)
        """
        if metric_name not in self.gauges:
            self.logger.warning(f"Gauge {metric_name} not found, skipping in-progress tracking")
            return

        # Create a tuple of label values to use as a dictionary key
        labels_key = tuple(sorted(labels.items()))

        # Get the current count for these labels
        current = self.in_progress[metric_name].get(labels_key, 0)

        # Update the count
        new_count = current + count

        # Store the updated count
        self.in_progress[metric_name][labels_key] = new_count

        # Update the gauge
        self.set_gauge(metric_name, new_count, labels)

    @contextmanager
    def timer(
        self,
        metric_type: str,
        name: str,
        labels: Optional[Dict[str, str]] = None,
        track_in_progress: bool = False,
        in_progress_metric: Optional[str] = None,
    ) -> Generator[None, None, None]:
        """Context manager for timing operations.

        Args:
            metric_type: Type of metric (histogram or summary)
            name: Metric name
            labels: Optional label values
            track_in_progress: Whether to track in-progress operations
            in_progress_metric: Optional name of gauge metric for tracking in-progress operations
        """
        start_time = time.monotonic()

        # Track start of operation if requested
        if track_in_progress and in_progress_metric:
            self.track_in_progress(in_progress_metric, labels or {}, 1)

        try:
            yield
        finally:
            duration = time.monotonic() - start_time

            # Record the duration
            if metric_type == "histogram":
                self.observe_histogram(name, duration, labels)
            elif metric_type == "summary":
                self.observe_summary(name, duration, labels)

            # Track end of operation if requested
            if track_in_progress and in_progress_metric:
                self.track_in_progress(in_progress_metric, labels or {}, -1)

    def timed(
        self,
        metric_type: str,
        name: str,
        labels_func: Optional[Callable[..., Dict[str, str]]] = None,
        track_in_progress: bool = False,
        in_progress_metric: Optional[str] = None,
    ) -> Callable[[F], F]:
        """Decorator for timing function execution.

        Args:
            metric_type: Type of metric (histogram or summary)
            name: Metric name
            labels_func: Optional function to generate label values from function args
            track_in_progress: Whether to track in-progress operations
            in_progress_metric: Optional name of gauge metric for tracking in-progress operations

        Returns:
            Decorator function
        """
        def decorator(func: F) -> F:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                # Generate labels if a function was provided
                labels = None
                if labels_func:
                    labels = labels_func(*args, **kwargs)

                # Use the timing context manager
                with self.timer(
                    metric_type,
                    name,
                    labels,
                    track_in_progress,
                    in_progress_metric
                ):
                    return func(*args, **kwargs)

            return cast(F, wrapper)

        return decorator

    def async_timed(
        self,
        metric_type: str,
        name: str,
        labels_func: Optional[Callable[..., Dict[str, str]]] = None,
        track_in_progress: bool = False,
        in_progress_metric: Optional[str] = None,
    ) -> Callable[[F], F]:
        """Decorator for timing async function execution.

        Args:
            metric_type: Type of metric (histogram or summary)
            name: Metric name
            labels_func: Optional function to generate label values from function args
            track_in_progress: Whether to track in-progress operations
            in_progress_metric: Optional name of gauge metric for tracking in-progress operations

        Returns:
            Decorator function
        """
        def decorator(func: F) -> F:
            @wraps(func)
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                # Generate labels if a function was provided
                labels = None
                if labels_func:
                    labels = labels_func(*args, **kwargs)

                # Start timing
                start_time = time.monotonic()

                # Track start of operation if requested
                if track_in_progress and in_progress_metric:
                    self.track_in_progress(in_progress_metric, labels or {}, 1)

                try:
                    # Execute the function
                    return await func(*args, **kwargs)
                finally:
                    # Record duration
                    duration = time.monotonic() - start_time

                    if metric_type == "histogram":
                        self.observe_histogram(name, duration, labels)
                    elif metric_type == "summary":
                        self.observe_summary(name, duration, labels)

                    # Track end of operation if requested
                    if track_in_progress and in_progress_metric:
                        self.track_in_progress(in_progress_metric, labels or {}, -1)

            return cast(F, wrapper)

        return decorator

    def track_request(
        self,
        method: str,
        endpoint: str,
        status_code: int,
        duration: float,
        error_code: Optional[str] = None,
    ) -> None:
        """Track HTTP request metrics.

        Args:
            method: HTTP method
            endpoint: Request endpoint
            status_code: Response status code
            duration: Request duration in seconds
            error_code: Optional error code if request failed
        """
        # Track request count
        self.increment_counter(
            MetricName.HTTP_REQUESTS_TOTAL,
            1,
            {
                MetricTag.METHOD: method,
                MetricTag.ENDPOINT: endpoint,
                MetricTag.STATUS_CODE: str(status_code)
            }
        )

        # Track request duration
        self.observe_histogram(
            MetricName.HTTP_REQUEST_DURATION_SECONDS,
            duration,
            {
                MetricTag.METHOD: method,
                MetricTag.ENDPOINT: endpoint
            }
        )

        # Track errors if status code indicates an error
        if status_code >= 400:
            self.increment_counter(
                MetricName.HTTP_ERRORS_TOTAL,
                1,
                {
                    MetricTag.METHOD: method,
                    MetricTag.ENDPOINT: endpoint,
                    MetricTag.ERROR_CODE: error_code or f"http_{status_code}"
                }
            )

    def track_db_query(
        self,
        operation: str,
        entity: str,
        duration: float,
        error: Optional[str] = None,
    ) -> None:
        """Track database query metrics.

        Args:
            operation: Database operation (e.g., SELECT, INSERT)
            entity: Entity being queried
            duration: Query duration in seconds
            error: Optional error message if query failed
        """
        # Track query count
        self.increment_counter(
            MetricName.DB_QUERIES_TOTAL,
            1,
            {
                MetricTag.OPERATION: operation,
                MetricTag.ENTITY: entity
            }
        )

        # Track query duration
        self.observe_histogram(
            MetricName.DB_QUERY_DURATION_SECONDS,
            duration,
            {
                MetricTag.OPERATION: operation,
                MetricTag.ENTITY: entity
            }
        )

        # Track errors if an error occurred
        if error:
            self.increment_counter(
                MetricName.DB_ERRORS_TOTAL,
                1,
                {
                    MetricTag.OPERATION: operation,
                    MetricTag.ENTITY: entity,
                    MetricTag.ERROR_TYPE: error
                }
            )

    def track_service_call(
        self,
        component: str,
        action: str,
        duration: float,
        error: Optional[str] = None,
    ) -> None:
        """Track service call metrics.

        Args:
            component: Service component name
            action: Action being performed
            duration: Call duration in seconds
            error: Optional error message if call failed
        """
        # Track call count
        self.increment_counter(
            MetricName.SERVICE_CALLS_TOTAL,
            1,
            {
                MetricTag.COMPONENT: component,
                MetricTag.ACTION: action
            }
        )

        # Track call duration
        self.observe_histogram(
            MetricName.SERVICE_CALL_DURATION_SECONDS,
            duration,
            {
                MetricTag.COMPONENT: component,
                MetricTag.ACTION: action
            }
        )

        # Track errors if an error occurred
        if error:
            self.increment_counter(
                MetricName.SERVICE_ERRORS_TOTAL,
                1,
                {
                    MetricTag.COMPONENT: component,
                    MetricTag.ACTION: action,
                    MetricTag.ERROR_TYPE: error
                }
            )

    def track_cache_operation(
        self,
        operation: str,
        backend: str,
        hit: bool,
        duration: float,
        component: str = "unknown",
    ) -> None:
        """Track cache operation metrics.

        Args:
            operation: Cache operation (get, set, delete)
            backend: Cache backend (memory, redis)
            hit: Whether the operation was a cache hit
            duration: Operation duration in seconds
            component: Component using the cache
        """
        # Track operation count
        self.increment_counter(
            MetricName.CACHE_OPERATIONS_TOTAL,
            1,
            {
                MetricTag.OPERATION: operation,
                MetricTag.CACHE_BACKEND: backend,
                MetricTag.COMPONENT: component
            }
        )

        # Track hits/misses
        if operation == "get":
            if hit:
                self.increment_counter(
                    MetricName.CACHE_HIT_TOTAL,
                    1,
                    {
                        MetricTag.CACHE_BACKEND: backend,
                        MetricTag.COMPONENT: component
                    }
                )
            else:
                self.increment_counter(
                    MetricName.CACHE_MISS_TOTAL,
                    1,
                    {
                        MetricTag.CACHE_BACKEND: backend,
                        MetricTag.COMPONENT: component
                    }
                )

        # Track operation duration
        self.observe_histogram(
            MetricName.CACHE_OPERATION_DURATION_SECONDS,
            duration,
            {
                MetricTag.CACHE_BACKEND: backend,
                MetricTag.OPERATION: operation
            }
        )

    def get_current_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Get the current values of all metrics.

        Returns:
            Dictionary of metric values by name
        """
        result = {}

        # This is not a standard way to get values from Prometheus client
        # but can be useful for debugging

        for name, counter in self.counters.items():
            result[name] = {
                "type": "counter",
                "values": dict(counter._metrics)
            }

        for name, gauge in self.gauges.items():
            result[name] = {
                "type": "gauge",
                "values": dict(gauge._metrics)
            }

        for name, histogram in self.histograms.items():
            result[name] = {
                "type": "histogram",
                "values": dict(histogram._metrics)
            }

        for name, summary in self.summaries.items():
            result[name] = {
                "type": "summary",
                "values": dict(summary._metrics)
            }

        return result
