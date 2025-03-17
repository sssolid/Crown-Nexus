# /backend/app/services/metrics_service.py
from __future__ import annotations

import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable, Dict, Generator, List, Optional, TypeVar, cast

from prometheus_client import Counter, Gauge, Histogram, Summary

from app.core.logging import get_logger
from app.services.interfaces import ServiceInterface

# Type variables
F = TypeVar("F", bound=Callable[..., Any])

logger = get_logger("app.services.metrics_service")

@dataclass
class MetricsConfig:
    """Configuration for metrics."""
    
    namespace: str = "crown_nexus"
    subsystem: str = "api"
    
    # Default labels for all metrics
    default_labels: Dict[str, str] = field(default_factory=dict)
    
    # Default buckets for histograms (in seconds)
    default_buckets: List[float] = field(
        default_factory=lambda: [
            0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0
        ]
    )

class MetricsService:
    """Service for collecting and exporting metrics.
    
    This service provides standardized metrics collection across the application,
    with support for counters, gauges, histograms, and summaries.
    """
    
    def __init__(self, config: Optional[MetricsConfig] = None) -> None:
        """Initialize the metrics service.
        
        Args:
            config: Metrics configuration
        """
        self.logger = logger
        self.config = config or MetricsConfig()
        
        # Metrics registries
        self.counters: Dict[str, Counter] = {}
        self.gauges: Dict[str, Gauge] = {}
        self.histograms: Dict[str, Histogram] = {}
        self.summaries: Dict[str, Summary] = {}
        
        # Initialize default metrics
        self._initialize_default_metrics()
        
    async def initialize(self) -> None:
        """Initialize service resources."""
        self.logger.debug("Initializing metrics service")
        
    async def shutdown(self) -> None:
        """Release service resources."""
        self.logger.debug("Shutting down metrics service")
        
    def _initialize_default_metrics(self) -> None:
        """Initialize default metrics for the application."""
        # HTTP request metrics
        self.create_counter(
            "http_requests_total",
            "Total number of HTTP requests",
            ["method", "endpoint", "status"]
        )
        
        self.create_histogram(
            "http_request_duration_seconds",
            "HTTP request duration in seconds",
            ["method", "endpoint"]
        )
        
        # Database metrics
        self.create_counter(
            "db_queries_total",
            "Total number of database queries",
            ["operation", "entity"]
        )
        
        self.create_histogram(
            "db_query_duration_seconds",
            "Database query duration in seconds",
            ["operation", "entity"]
        )
        
        # Service metrics
        self.create_counter(
            "service_calls_total",
            "Total number of service calls",
            ["service", "method"]
        )
        
        self.create_histogram(
            "service_call_duration_seconds",
            "Service call duration in seconds",
            ["service", "method"]
        )
        
        # Error metrics
        self.create_counter(
            "errors_total",
            "Total number of errors",
            ["service", "error_type"]
        )
        
    def create_counter(
        self, 
        name: str, 
        description: str, 
        labelnames: Optional[List[str]] = None,
        namespace: Optional[str] = None,
        subsystem: Optional[str] = None,
    ) -> Counter:
        """Create a counter metric.
        
        Args:
            name: Metric name
            description: Metric description
            labelnames: Label names
            namespace: Metric namespace
            subsystem: Metric subsystem
            
        Returns:
            Counter: Created counter
        """
        namespace = namespace or self.config.namespace
        subsystem = subsystem or self.config.subsystem
        
        # Create counter if it doesn't exist
        if name not in self.counters:
            self.counters[name] = Counter(
                name=name,
                documentation=description,
                labelnames=labelnames or [],
                namespace=namespace,
                subsystem=subsystem,
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
        """Create a gauge metric.
        
        Args:
            name: Metric name
            description: Metric description
            labelnames: Label names
            namespace: Metric namespace
            subsystem: Metric subsystem
            
        Returns:
            Gauge: Created gauge
        """
        namespace = namespace or self.config.namespace
        subsystem = subsystem or self.config.subsystem
        
        # Create gauge if it doesn't exist
        if name not in self.gauges:
            self.gauges[name] = Gauge(
                name=name,
                documentation=description,
                labelnames=labelnames or [],
                namespace=namespace,
                subsystem=subsystem,
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
        """Create a histogram metric.
        
        Args:
            name: Metric name
            description: Metric description
            labelnames: Label names
            buckets: Histogram buckets
            namespace: Metric namespace
            subsystem: Metric subsystem
            
        Returns:
            Histogram: Created histogram
        """
        namespace = namespace or self.config.namespace
        subsystem = subsystem or self.config.subsystem
        buckets = buckets or self.config.default_buckets
        
        # Create histogram if it doesn't exist
        if name not in self.histograms:
            self.histograms[name] = Histogram(
                name=name,
                documentation=description,
                labelnames=labelnames or [],
                buckets=buckets,
                namespace=namespace,
                subsystem=subsystem,
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
        """Create a summary metric.
        
        Args:
            name: Metric name
            description: Metric description
            labelnames: Label names
            namespace: Metric namespace
            subsystem: Metric subsystem
            
        Returns:
            Summary: Created summary
        """
        namespace = namespace or self.config.namespace
        subsystem = subsystem or self.config.subsystem
        
        # Create summary if it doesn't exist
        if name not in self.summaries:
            self.summaries[name] = Summary(
                name=name,
                documentation=description,
                labelnames=labelnames or [],
                namespace=namespace,
                subsystem=subsystem,
            )
            
        return self.summaries[name]
        
    def increment_counter(
        self, 
        name: str, 
        amount: float = 1.0, 
        labels: Optional[Dict[str, str]] = None
    ) -> None:
        """Increment a counter metric.
        
        Args:
            name: Metric name
            amount: Amount to increment by
            labels: Metric labels
        """
        if name not in self.counters:
            self.logger.warning(f"Counter {name} not found, skipping increment")
            return
            
        counter = self.counters[name]
        if labels:
            counter.labels(**labels).inc(amount)
        else:
            counter.inc(amount)
            
    def set_gauge(
        self, 
        name: str, 
        value: float, 
        labels: Optional[Dict[str, str]] = None
    ) -> None:
        """Set a gauge metric value.
        
        Args:
            name: Metric name
            value: Gauge value
            labels: Metric labels
        """
        if name not in self.gauges:
            self.logger.warning(f"Gauge {name} not found, skipping set")
            return
            
        gauge = self.gauges[name]
        if labels:
            gauge.labels(**labels).set(value)
        else:
            gauge.set(value)
            
    def observe_histogram(
        self, 
        name: str, 
        value: float, 
        labels: Optional[Dict[str, str]] = None
    ) -> None:
        """Observe a histogram metric value.
        
        Args:
            name: Metric name
            value: Observation value
            labels: Metric labels
        """
        if name not in self.histograms:
            self.logger.warning(f"Histogram {name} not found, skipping observation")
            return
            
        histogram = self.histograms[name]
        if labels:
            histogram.labels(**labels).observe(value)
        else:
            histogram.observe(value)
            
    def observe_summary(
        self, 
        name: str, 
        value: float, 
        labels: Optional[Dict[str, str]] = None
    ) -> None:
        """Observe a summary metric value.
        
        Args:
            name: Metric name
            value: Observation value
            labels: Metric labels
        """
        if name not in self.summaries:
            self.logger.warning(f"Summary {name} not found, skipping observation")
            return
            
        summary = self.summaries[name]
        if labels:
            summary.labels(**labels).observe(value)
        else:
            summary.observe(value)
            
    @contextmanager
    def timer(
        self, 
        metric_type: str, 
        name: str, 
        labels: Optional[Dict[str, str]] = None
    ) -> Generator[None, None, None]:
        """Context manager for timing operations.
        
        Args:
            metric_type: Type of metric (histogram or summary)
            name: Metric name
            labels: Metric labels
            
        Yields:
            None
        """
        start_time = time.time()
        try:
            yield
        finally:
            duration = time.time() - start_time
            
            if metric_type == "histogram":
                self.observe_histogram(name, duration, labels)
            elif metric_type == "summary":
                self.observe_summary(name, duration, labels)
            else:
                self.logger.warning(f"Unknown metric type: {metric_type}")
                
    def timing_decorator(
        self, 
        metric_type: str, 
        name: str, 
        labels_func: Optional[Callable[..., Dict[str, str]]] = None
    ) -> Callable[[F], F]:
        """Decorator for timing function execution.
        
        Args:
            metric_type: Type of metric (histogram or summary)
            name: Metric name
            labels_func: Function to extract labels from function arguments
            
        Returns:
            Callable: Decorated function
        """
        def decorator(func: F) -> F:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                # Get labels if provided
                labels = None
                if labels_func:
                    labels = labels_func(*args, **kwargs)
                    
                # Time function execution
                with self.timer(metric_type, name, labels):
                    return func(*args, **kwargs)
                    
            return cast(F, wrapper)
        return decorator
        
    async def timing_decorator_async(
        self, 
        metric_type: str, 
        name: str, 
        labels_func: Optional[Callable[..., Dict[str, str]]] = None
    ) -> Callable[[F], F]:
        """Decorator for timing async function execution.
        
        Args:
            metric_type: Type of metric (histogram or summary)
            name: Metric name
            labels_func: Function to extract labels from function arguments
            
        Returns:
            Callable: Decorated async function
        """
        def decorator(func: F) -> F:
            @wraps(func)
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                # Get labels if provided
                labels = None
                if labels_func:
                    labels = labels_func(*args, **kwargs)
                    
                # Time function execution
                start_time = time.time()
                try:
                    return await func(*args, **kwargs)
                finally:
                    duration = time.time() - start_time
                    
                    if metric_type == "histogram":
                        self.observe_histogram(name, duration, labels)
                    elif metric_type == "summary":
                        self.observe_summary(name, duration, labels)
                    else:
                        self.logger.warning(f"Unknown metric type: {metric_type}")
                    
            return cast(F, wrapper)
        return decorator
