from __future__ import annotations
from typing import Dict, List, Optional
from prometheus_client import Counter, Gauge, Histogram, Summary
from app.logging import get_logger
logger = get_logger('app.core.metrics.collectors')
class MetricCollector:
    def __init__(self, name: str, description: str, labelnames: Optional[List[str]]=None, namespace: Optional[str]=None, subsystem: Optional[str]=None):
        self.name = name
        self.description = description
        self.labelnames = labelnames or []
        self.namespace = namespace
        self.subsystem = subsystem
class CounterCollector(MetricCollector):
    def __init__(self, name: str, description: str, labelnames: Optional[List[str]]=None, namespace: Optional[str]=None, subsystem: Optional[str]=None):
        super().__init__(name, description, labelnames, namespace, subsystem)
        self.counter = Counter(name=name, documentation=description, labelnames=labelnames or [], namespace=namespace, subsystem=subsystem)
    def increment(self, amount: float=1.0, labels: Optional[Dict[str, str]]=None) -> None:
        try:
            if labels:
                self.counter.labels(**labels).inc(amount)
            else:
                self.counter.inc(amount)
        except Exception as e:
            logger.error(f'Error incrementing counter {self.name}: {str(e)}')
class GaugeCollector(MetricCollector):
    def __init__(self, name: str, description: str, labelnames: Optional[List[str]]=None, namespace: Optional[str]=None, subsystem: Optional[str]=None):
        super().__init__(name, description, labelnames, namespace, subsystem)
        self.gauge = Gauge(name=name, documentation=description, labelnames=labelnames or [], namespace=namespace, subsystem=subsystem)
    def set(self, value: float, labels: Optional[Dict[str, str]]=None) -> None:
        try:
            if labels:
                self.gauge.labels(**labels).set(value)
            else:
                self.gauge.set(value)
        except Exception as e:
            logger.error(f'Error setting gauge {self.name}: {str(e)}')
    def increment(self, amount: float=1.0, labels: Optional[Dict[str, str]]=None) -> None:
        try:
            if labels:
                self.gauge.labels(**labels).inc(amount)
            else:
                self.gauge.inc(amount)
        except Exception as e:
            logger.error(f'Error incrementing gauge {self.name}: {str(e)}')
    def decrement(self, amount: float=1.0, labels: Optional[Dict[str, str]]=None) -> None:
        try:
            if labels:
                self.gauge.labels(**labels).dec(amount)
            else:
                self.gauge.dec(amount)
        except Exception as e:
            logger.error(f'Error decrementing gauge {self.name}: {str(e)}')
class HistogramCollector(MetricCollector):
    def __init__(self, name: str, description: str, labelnames: Optional[List[str]]=None, buckets: Optional[List[float]]=None, namespace: Optional[str]=None, subsystem: Optional[str]=None):
        super().__init__(name, description, labelnames, namespace, subsystem)
        self.histogram = Histogram(name=name, documentation=description, labelnames=labelnames or [], buckets=buckets or Histogram.DEFAULT_BUCKETS, namespace=namespace, subsystem=subsystem)
    def observe(self, value: float, labels: Optional[Dict[str, str]]=None) -> None:
        try:
            if labels:
                self.histogram.labels(**labels).observe(value)
            else:
                self.histogram.observe(value)
        except Exception as e:
            logger.error(f'Error observing histogram {self.name}: {str(e)}')
class SummaryCollector(MetricCollector):
    def __init__(self, name: str, description: str, labelnames: Optional[List[str]]=None, namespace: Optional[str]=None, subsystem: Optional[str]=None):
        super().__init__(name, description, labelnames, namespace, subsystem)
        self.summary = Summary(name=name, documentation=description, labelnames=labelnames or [], namespace=namespace, subsystem=subsystem)
    def observe(self, value: float, labels: Optional[Dict[str, str]]=None) -> None:
        try:
            if labels:
                self.summary.labels(**labels).observe(value)
            else:
                self.summary.observe(value)
        except Exception as e:
            logger.error(f'Error observing summary {self.name}: {str(e)}')