from __future__ import annotations

"""
Metrics service implementation.

This module provides a service wrapper around the metrics system,
making it available through the dependency manager.
"""

from typing import Any, Callable, Dict, List, Optional, TypeVar, Union

from app.logging import get_logger
from app.core.metrics.base import MetricName, MetricTag, MetricType, MetricsConfig
from app.core.metrics.collectors import (
    CounterCollector,
    GaugeCollector,
    HistogramCollector,
    SummaryCollector,
)
from app.core.metrics.exceptions import MetricsConfigurationException
from app.core.metrics.manager import (
    increment_counter,
    set_gauge,
    observe_histogram,
    observe_summary,
    create_counter,
    create_gauge,
    create_histogram,
    create_summary,
    track_request,
    track_db_query,
    track_service_call,
    track_cache_operation,
    track_in_progress,
    timed_function,
    async_timed_function,
    initialize as initialize_manager,
    shutdown as shutdown_manager,
    get_current_metrics,
)

logger = get_logger("app.core.metrics.service")

F = TypeVar("F", bound=Callable[..., Any])


class MetricsService:
    """Service wrapper for the metrics system."""

    def __init__(self) -> None:
        """Initialize the metrics service."""
        self._initialized = False
        self._config: Optional[MetricsConfig] = None

    async def initialize(self, config: Optional[MetricsConfig] = None) -> None:
        """
        Initialize the metrics service.

        Args:
            config: Optional metrics configuration
        """
        if self._initialized:
            logger.debug("Metrics service already initialized, skipping")
            return

        logger.info("Initializing metrics service")
        self._config = config
        await initialize_manager(config)
        self._initialized = True
        logger.info("Metrics service initialized")

    async def shutdown(self) -> None:
        """Shutdown the metrics service."""
        if not self._initialized:
            return

        logger.info("Shutting down metrics service")
        await shutdown_manager()
        self._initialized = False
        logger.info("Metrics service shut down")

    def create_counter(
        self,
        name: str,
        description: str,
        labelnames: Optional[List[str]] = None,
        namespace: Optional[str] = None,
        subsystem: Optional[str] = None,
    ) -> CounterCollector:
        """
        Create a counter metric.

        Args:
            name: Metric name
            description: Metric description
            labelnames: Optional list of label names
            namespace: Optional namespace
            subsystem: Optional subsystem

        Returns:
            A counter collector instance
        """
        return create_counter(name, description, labelnames, namespace, subsystem)

    def create_gauge(
        self,
        name: str,
        description: str,
        labelnames: Optional[List[str]] = None,
        namespace: Optional[str] = None,
        subsystem: Optional[str] = None,
    ) -> GaugeCollector:
        """
        Create a gauge metric.

        Args:
            name: Metric name
            description: Metric description
            labelnames: Optional list of label names
            namespace: Optional namespace
            subsystem: Optional subsystem

        Returns:
            A gauge collector instance
        """
        return create_gauge(name, description, labelnames, namespace, subsystem)

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
        Create a histogram metric.

        Args:
            name: Metric name
            description: Metric description
            labelnames: Optional list of label names
            buckets: Optional bucket definitions
            namespace: Optional namespace
            subsystem: Optional subsystem

        Returns:
            A histogram collector instance
        """
        return create_histogram(
            name, description, labelnames, buckets, namespace, subsystem
        )

    def create_summary(
        self,
        name: str,
        description: str,
        labelnames: Optional[List[str]] = None,
        namespace: Optional[str] = None,
        subsystem: Optional[str] = None,
    ) -> SummaryCollector:
        """
        Create a summary metric.

        Args:
            name: Metric name
            description: Metric description
            labelnames: Optional list of label names
            namespace: Optional namespace
            subsystem: Optional subsystem

        Returns:
            A summary collector instance
        """
        return create_summary(name, description, labelnames, namespace, subsystem)

    def increment_counter(
        self, name: str, amount: float = 1.0, labels: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Increment a counter metric.

        Args:
            name: Metric name
            amount: Amount to increment by
            labels: Optional label values
        """
        increment_counter(name, amount, labels)

    def set_gauge(
        self, name: str, value: float, labels: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Set a gauge metric value.

        Args:
            name: Metric name
            value: Value to set
            labels: Optional label values
        """
        set_gauge(name, value, labels)

    def observe_histogram(
        self, name: str, value: float, labels: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Observe a value for a histogram metric.

        Args:
            name: Metric name
            value: Value to observe
            labels: Optional label values
        """
        observe_histogram(name, value, labels)

    def observe_summary(
        self, name: str, value: float, labels: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Observe a value for a summary metric.

        Args:
            name: Metric name
            value: Value to observe
            labels: Optional label values
        """
        observe_summary(name, value, labels)

    def track_in_progress(
        self, metric_name: str, labels: Dict[str, str], count: int = 1
    ) -> None:
        """
        Track in-progress operations.

        Args:
            metric_name: Metric name
            labels: Label values
            count: Count to adjust by
        """
        track_in_progress(metric_name, labels, count)

    def track_request(
        self,
        method: str,
        endpoint: str,
        status_code: int,
        duration: float,
        error_code: Optional[str] = None,
    ) -> None:
        """
        Track an HTTP request.

        Args:
            method: HTTP method
            endpoint: Request endpoint
            status_code: Response status code
            duration: Request duration in seconds
            error_code: Optional error code
        """
        track_request(method, endpoint, status_code, duration, error_code)

    def track_db_query(
        self, operation: str, entity: str, duration: float, error: Optional[str] = None
    ) -> None:
        """
        Track a database query.

        Args:
            operation: Database operation type
            entity: Entity being operated on
            duration: Query duration in seconds
            error: Optional error information
        """
        track_db_query(operation, entity, duration, error)

    def track_service_call(
        self, component: str, action: str, duration: float, error: Optional[str] = None
    ) -> None:
        """
        Track a service call.

        Args:
            component: Service component
            action: Action being performed
            duration: Call duration in seconds
            error: Optional error information
        """
        track_service_call(component, action, duration, error)

    def track_cache_operation(
        self,
        operation: str,
        backend: str,
        hit: bool,
        duration: float,
        component: str = "unknown",
    ) -> None:
        """
        Track a cache operation.

        Args:
            operation: Cache operation type
            backend: Cache backend type
            hit: Whether the operation was a cache hit
            duration: Operation duration in seconds
            component: Optional component name
        """
        track_cache_operation(operation, backend, hit, duration, component)

    def timed_function(
        self,
        name: str,
        metric_type: MetricType = MetricType.HISTOGRAM,
        labels_func: Optional[Callable[..., Dict[str, str]]] = None,
        track_in_progress_flag: bool = False,
        in_progress_metric: Optional[str] = None,
    ) -> Callable:
        """
        Create a decorator for timing a function.

        Args:
            name: Metric name
            metric_type: Type of metric
            labels_func: Optional function to generate labels
            track_in_progress_flag: Whether to track in-progress operations
            in_progress_metric: Optional metric name for in-progress tracking

        Returns:
            A decorator function
        """
        return timed_function(
            name, metric_type, labels_func, track_in_progress_flag, in_progress_metric
        )

    def async_timed_function(
        self,
        name: str,
        metric_type: MetricType = MetricType.HISTOGRAM,
        labels_func: Optional[Callable[..., Dict[str, str]]] = None,
        track_in_progress_flag: bool = False,
        in_progress_metric: Optional[str] = None,
    ) -> Callable:
        """
        Create a decorator for timing an async function.

        Args:
            name: Metric name
            metric_type: Type of metric
            labels_func: Optional function to generate labels
            track_in_progress_flag: Whether to track in-progress operations
            in_progress_metric: Optional metric name for in-progress tracking

        Returns:
            A decorator function
        """
        return async_timed_function(
            name, metric_type, labels_func, track_in_progress_flag, in_progress_metric
        )

    def get_current_metrics(self) -> Dict[str, Dict[str, Any]]:
        """
        Get the current metrics data.

        Returns:
            A dictionary of current metrics data
        """
        return get_current_metrics()


# Singleton instance
_metrics_service: Optional[MetricsService] = None


def get_metrics_service() -> MetricsService:
    """
    Get the metrics service singleton.

    Returns:
        The metrics service instance
    """
    global _metrics_service
    if _metrics_service is None:
        _metrics_service = MetricsService()
    return _metrics_service
