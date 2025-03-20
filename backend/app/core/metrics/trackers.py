# /app/core/metrics/trackers.py
"""Specialized trackers for common metric collection scenarios.

This module provides high-level trackers for common use cases like HTTP requests,
database operations, service calls, and cache operations.
"""
from __future__ import annotations

from typing import Dict, Optional

from app.core.logging import get_logger
from app.core.metrics.base import MetricName, MetricTag

logger = get_logger(__name__)


class HttpTracker:
    """Tracker for HTTP request metrics."""

    def __init__(
        self,
        increment_counter_func: callable,
        observe_histogram_func: callable,
        increment_error_func: callable,
    ):
        """
        Initialize the HTTP tracker.

        Args:
            increment_counter_func: Function to increment a counter
            observe_histogram_func: Function to observe a histogram
            increment_error_func: Function to increment an error counter
        """
        self.increment_counter = increment_counter_func
        self.observe_histogram = observe_histogram_func
        self.increment_error = increment_error_func

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
        # Track request count
        self.increment_counter(
            MetricName.HTTP_REQUESTS_TOTAL,
            1,
            {
                MetricTag.METHOD: method,
                MetricTag.ENDPOINT: endpoint,
                MetricTag.STATUS_CODE: str(status_code),
            },
        )

        # Track request duration
        self.observe_histogram(
            MetricName.HTTP_REQUEST_DURATION_SECONDS,
            duration,
            {MetricTag.METHOD: method, MetricTag.ENDPOINT: endpoint},
        )

        # Track errors if status code indicates an error
        if status_code >= 400:
            self.increment_error(
                MetricName.HTTP_ERRORS_TOTAL,
                1,
                {
                    MetricTag.METHOD: method,
                    MetricTag.ENDPOINT: endpoint,
                    MetricTag.ERROR_CODE: error_code or f"http_{status_code}",
                },
            )


class DatabaseTracker:
    """Tracker for database operation metrics."""

    def __init__(
        self,
        increment_counter_func: callable,
        observe_histogram_func: callable,
        increment_error_func: callable,
    ):
        """
        Initialize the database tracker.

        Args:
            increment_counter_func: Function to increment a counter
            observe_histogram_func: Function to observe a histogram
            increment_error_func: Function to increment an error counter
        """
        self.increment_counter = increment_counter_func
        self.observe_histogram = observe_histogram_func
        self.increment_error = increment_error_func

    def track_query(
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
        # Track query count
        self.increment_counter(
            MetricName.DB_QUERIES_TOTAL,
            1,
            {MetricTag.OPERATION: operation, MetricTag.ENTITY: entity},
        )

        # Track query duration
        self.observe_histogram(
            MetricName.DB_QUERY_DURATION_SECONDS,
            duration,
            {MetricTag.OPERATION: operation, MetricTag.ENTITY: entity},
        )

        # Track errors if an error occurred
        if error:
            self.increment_error(
                MetricName.DB_ERRORS_TOTAL,
                1,
                {
                    MetricTag.OPERATION: operation,
                    MetricTag.ENTITY: entity,
                    MetricTag.ERROR_TYPE: error,
                },
            )


class ServiceTracker:
    """Tracker for service call metrics."""

    def __init__(
        self,
        increment_counter_func: callable,
        observe_histogram_func: callable,
        increment_error_func: callable,
    ):
        """
        Initialize the service tracker.

        Args:
            increment_counter_func: Function to increment a counter
            observe_histogram_func: Function to observe a histogram
            increment_error_func: Function to increment an error counter
        """
        self.increment_counter = increment_counter_func
        self.observe_histogram = observe_histogram_func
        self.increment_error = increment_error_func

    def track_call(
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
        # Track call count
        self.increment_counter(
            MetricName.SERVICE_CALLS_TOTAL,
            1,
            {MetricTag.COMPONENT: component, MetricTag.ACTION: action},
        )

        # Track call duration
        self.observe_histogram(
            MetricName.SERVICE_CALL_DURATION_SECONDS,
            duration,
            {MetricTag.COMPONENT: component, MetricTag.ACTION: action},
        )

        # Track errors if an error occurred
        if error:
            self.increment_error(
                MetricName.SERVICE_ERRORS_TOTAL,
                1,
                {
                    MetricTag.COMPONENT: component,
                    MetricTag.ACTION: action,
                    MetricTag.ERROR_TYPE: error,
                },
            )


class CacheTracker:
    """Tracker for cache operation metrics."""

    def __init__(
        self,
        increment_counter_func: callable,
        observe_histogram_func: callable,
    ):
        """
        Initialize the cache tracker.

        Args:
            increment_counter_func: Function to increment a counter
            observe_histogram_func: Function to observe a histogram
        """
        self.increment_counter = increment_counter_func
        self.observe_histogram = observe_histogram_func

    def track_operation(
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
        # Track operation count
        self.increment_counter(
            MetricName.CACHE_OPERATIONS_TOTAL,
            1,
            {
                MetricTag.OPERATION: operation,
                MetricTag.CACHE_BACKEND: backend,
                MetricTag.COMPONENT: component,
            },
        )

        # Track hits/misses
        if operation == "get":
            if hit:
                self.increment_counter(
                    MetricName.CACHE_HIT_TOTAL,
                    1,
                    {MetricTag.CACHE_BACKEND: backend, MetricTag.COMPONENT: component},
                )
            else:
                self.increment_counter(
                    MetricName.CACHE_MISS_TOTAL,
                    1,
                    {MetricTag.CACHE_BACKEND: backend, MetricTag.COMPONENT: component},
                )

        # Track operation duration
        self.observe_histogram(
            MetricName.CACHE_OPERATION_DURATION_SECONDS,
            duration,
            {MetricTag.CACHE_BACKEND: backend, MetricTag.OPERATION: operation},
        )
