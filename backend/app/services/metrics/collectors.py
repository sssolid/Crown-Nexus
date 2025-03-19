# backend/app/services/metrics/collectors.py
"""Metric collectors for different metric types.

This module provides classes for collecting different types of metrics
(counters, gauges, histograms, summaries) with a consistent interface.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from prometheus_client import Counter, Gauge, Histogram, Summary

from app.core.logging import get_logger

logger = get_logger(__name__)


class MetricCollector:
    """Base class for metric collectors."""

    def __init__(
        self,
        name: str,
        description: str,
        labelnames: Optional[List[str]] = None,
        namespace: Optional[str] = None,
        subsystem: Optional[str] = None,
    ):
        """
        Initialize the metric collector.

        Args:
            name: Metric name
            description: Metric description
            labelnames: Optional list of label names
            namespace: Optional metric namespace
            subsystem: Optional metric subsystem
        """
        self.name = name
        self.description = description
        self.labelnames = labelnames or []
        self.namespace = namespace
        self.subsystem = subsystem


class CounterCollector(MetricCollector):
    """Collector for counter metrics."""

    def __init__(
        self,
        name: str,
        description: str,
        labelnames: Optional[List[str]] = None,
        namespace: Optional[str] = None,
        subsystem: Optional[str] = None,
    ):
        """
        Initialize the counter collector.

        Args:
            name: Metric name
            description: Metric description
            labelnames: Optional list of label names
            namespace: Optional metric namespace
            subsystem: Optional metric subsystem
        """
        super().__init__(name, description, labelnames, namespace, subsystem)
        self.counter = Counter(
            name=name,
            documentation=description,
            labelnames=labelnames or [],
            namespace=namespace,
            subsystem=subsystem
        )

    def increment(self, amount: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        """
        Increment the counter.

        Args:
            amount: Amount to increment by
            labels: Optional label values
        """
        try:
            if labels:
                self.counter.labels(**labels).inc(amount)
            else:
                self.counter.inc(amount)
        except Exception as e:
            logger.error(f"Error incrementing counter {self.name}: {str(e)}")


class GaugeCollector(MetricCollector):
    """Collector for gauge metrics."""

    def __init__(
        self,
        name: str,
        description: str,
        labelnames: Optional[List[str]] = None,
        namespace: Optional[str] = None,
        subsystem: Optional[str] = None,
    ):
        """
        Initialize the gauge collector.

        Args:
            name: Metric name
            description: Metric description
            labelnames: Optional list of label names
            namespace: Optional metric namespace
            subsystem: Optional metric subsystem
        """
        super().__init__(name, description, labelnames, namespace, subsystem)
        self.gauge = Gauge(
            name=name,
            documentation=description,
            labelnames=labelnames or [],
            namespace=namespace,
            subsystem=subsystem
        )

    def set(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """
        Set the gauge value.

        Args:
            value: Value to set
            labels: Optional label values
        """
        try:
            if labels:
                self.gauge.labels(**labels).set(value)
            else:
                self.gauge.set(value)
        except Exception as e:
            logger.error(f"Error setting gauge {self.name}: {str(e)}")

    def increment(self, amount: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        """
        Increment the gauge.

        Args:
            amount: Amount to increment by
            labels: Optional label values
        """
        try:
            if labels:
                self.gauge.labels(**labels).inc(amount)
            else:
                self.gauge.inc(amount)
        except Exception as e:
            logger.error(f"Error incrementing gauge {self.name}: {str(e)}")

    def decrement(self, amount: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        """
        Decrement the gauge.

        Args:
            amount: Amount to decrement by
            labels: Optional label values
        """
        try:
            if labels:
                self.gauge.labels(**labels).dec(amount)
            else:
                self.gauge.dec(amount)
        except Exception as e:
            logger.error(f"Error decrementing gauge {self.name}: {str(e)}")


class HistogramCollector(MetricCollector):
    """Collector for histogram metrics."""

    def __init__(
        self,
        name: str,
        description: str,
        labelnames: Optional[List[str]] = None,
        buckets: Optional[List[float]] = None,
        namespace: Optional[str] = None,
        subsystem: Optional[str] = None,
    ):
        """
        Initialize the histogram collector.

        Args:
            name: Metric name
            description: Metric description
            labelnames: Optional list of label names
            buckets: Optional histogram buckets
            namespace: Optional metric namespace
            subsystem: Optional metric subsystem
        """
        super().__init__(name, description, labelnames, namespace, subsystem)
        self.histogram = Histogram(
            name=name,
            documentation=description,
            labelnames=labelnames or [],
            buckets=buckets or Histogram.DEFAULT_BUCKETS,
            namespace=namespace,
            subsystem=subsystem
        )

    def observe(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """
        Record an observation.

        Args:
            value: Value to observe
            labels: Optional label values
        """
        try:
            if labels:
                self.histogram.labels(**labels).observe(value)
            else:
                self.histogram.observe(value)
        except Exception as e:
            logger.error(f"Error observing histogram {self.name}: {str(e)}")


class SummaryCollector(MetricCollector):
    """Collector for summary metrics."""

    def __init__(
        self,
        name: str,
        description: str,
        labelnames: Optional[List[str]] = None,
        namespace: Optional[str] = None,
        subsystem: Optional[str] = None,
    ):
        """
        Initialize the summary collector.

        Args:
            name: Metric name
            description: Metric description
            labelnames: Optional list of label names
            namespace: Optional metric namespace
            subsystem: Optional metric subsystem
        """
        super().__init__(name, description, labelnames, namespace, subsystem)
        self.summary = Summary(
            name=name,
            documentation=description,
            labelnames=labelnames or [],
            namespace=namespace,
            subsystem=subsystem
        )

    def observe(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """
        Record an observation.

        Args:
            value: Value to observe
            labels: Optional label values
        """
        try:
            if labels:
                self.summary.labels(**labels).observe(value)
            else:
                self.summary.observe(value)
        except Exception as e:
            logger.error(f"Error observing summary {self.name}: {str(e)}")
