# backend/app/services/metrics/__init__.py
"""Metrics service package for application monitoring and observability.

This package provides services for collecting, tracking, and exposing
application metrics for monitoring and performance analysis.
"""
from __future__ import annotations

from app.services.metrics.service import MetricsService

# Factory function for dependency injection
def get_metrics_service():
    """Factory function to get MetricsService"""
    return MetricsService()

__all__ = ["get_metrics_service", "MetricsService"]
