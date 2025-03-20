# /app/core/metrics/__init__.py
"""Metrics package for application monitoring and observability.

This package provides core functionality for collecting, tracking, and exposing
application metrics for monitoring and performance analysis.
"""
from __future__ import annotations

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
from app.core.metrics.decorators import timer
from app.core.metrics.manager import (
    initialize,
    shutdown,
    create_counter,
    create_gauge,
    create_histogram,
    create_summary,
    increment_counter,
    set_gauge,
    observe_histogram,
    observe_summary,
    track_in_progress,
    track_request,
    track_db_query,
    track_service_call,
    track_cache_operation,
    timed_function,
    async_timed_function,
    get_current_metrics,
)
from app.core.metrics.trackers import (
    HttpTracker,
    DatabaseTracker,
    ServiceTracker,
    CacheTracker,
)

__all__ = [
    # Base types and constants
    "MetricName",
    "MetricTag",
    "MetricType",
    "MetricsConfig",
    # Collectors
    "CounterCollector",
    "GaugeCollector",
    "HistogramCollector",
    "SummaryCollector",
    # Decorators
    "timer",
    "timed_function",
    "async_timed_function",
    # Core functions
    "initialize",
    "shutdown",
    "create_counter",
    "create_gauge",
    "create_histogram",
    "create_summary",
    "increment_counter",
    "set_gauge",
    "observe_histogram",
    "observe_summary",
    "track_in_progress",
    "track_request",
    "track_db_query",
    "track_service_call",
    "track_cache_operation",
    "get_current_metrics",
    # Trackers
    "HttpTracker",
    "DatabaseTracker",
    "ServiceTracker",
    "CacheTracker",
]
