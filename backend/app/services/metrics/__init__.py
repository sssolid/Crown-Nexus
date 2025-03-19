# backend/app/services/metrics/__init__.py
"""Metrics service package for application monitoring and observability.

This package provides services for collecting, tracking, and exposing
application metrics for monitoring and performance analysis.
"""
from __future__ import annotations

from app.core.dependency_manager import dependency_manager
from app.services.metrics.service import MetricsService

# Create a singleton instance
metrics_service = MetricsService()

# Register with dependency manager
dependency_manager.register_dependency("metrics_service", metrics_service)

__all__ = ["metrics_service", "MetricsService"]
