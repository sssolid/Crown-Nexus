# backend/app/services/metrics/decorators.py
"""Metric decorators for measuring function performance.

This module provides decorators for easily instrumenting functions and methods
with metrics, tracking execution time and call counts.
"""
from __future__ import annotations

import asyncio
import functools
import time
from contextlib import contextmanager
from typing import Any, Callable, Dict, Generator, Optional, TypeVar, cast

from app.core.logging import get_logger
from app.services.metrics.base import F

logger = get_logger(__name__)


@contextmanager
def timer(
    metric_type: str,
    name: str,
    observe_func: Callable[[str, float, Optional[Dict[str, str]]], None],
    labels: Optional[Dict[str, str]] = None,
    track_in_progress: bool = False,
    track_in_progress_func: Optional[Callable[[str, Dict[str, str], int], None]] = None,
    in_progress_metric: Optional[str] = None,
) -> Generator[None, None, None]:
    """
    Context manager for timing operations.

    Args:
        metric_type: Type of metric (histogram or summary)
        name: Metric name
        observe_func: Function to call for recording observations
        labels: Optional label values
        track_in_progress: Whether to track in-progress operations
        track_in_progress_func: Function to call for tracking in-progress operations
        in_progress_metric: Optional name of gauge metric for tracking in-progress operations
    """
    start_time = time.monotonic()

    # Track start of operation if requested
    if track_in_progress and track_in_progress_func and in_progress_metric and labels:
        track_in_progress_func(in_progress_metric, labels, 1)

    try:
        yield
    finally:
        duration = time.monotonic() - start_time

        # Record the duration
        observe_func(name, duration, labels)

        # Track end of operation if requested
        if track_in_progress and track_in_progress_func and in_progress_metric and labels:
            track_in_progress_func(in_progress_metric, labels, -1)


def timed(
    metric_type: str,
    name: str,
    observe_func: Callable[[str, float, Optional[Dict[str, str]]], None],
    labels_func: Optional[Callable[..., Dict[str, str]]] = None,
    track_in_progress: bool = False,
    track_in_progress_func: Optional[Callable[[str, Dict[str, str], int], None]] = None,
    in_progress_metric: Optional[str] = None,
) -> Callable[[F], F]:
    """
    Decorator for timing function execution.

    Args:
        metric_type: Type of metric (histogram or summary)
        name: Metric name
        observe_func: Function to call for recording observations
        labels_func: Optional function to generate label values from function args
        track_in_progress: Whether to track in-progress operations
        track_in_progress_func: Function to call for tracking in-progress operations
        in_progress_metric: Optional name of gauge metric for tracking in-progress operations

    Returns:
        Decorator function
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Generate labels if a function was provided
            labels = None
            if labels_func:
                labels = labels_func(*args, **kwargs)

            # Use the timing context manager
            with timer(
                metric_type,
                name,
                observe_func,
                labels,
                track_in_progress,
                track_in_progress_func,
                in_progress_metric
            ):
                return func(*args, **kwargs)

        return cast(F, wrapper)

    return decorator


def async_timed(
    metric_type: str,
    name: str,
    observe_func: Callable[[str, float, Optional[Dict[str, str]]], None],
    labels_func: Optional[Callable[..., Dict[str, str]]] = None,
    track_in_progress: bool = False,
    track_in_progress_func: Optional[Callable[[str, Dict[str, str], int], None]] = None,
    in_progress_metric: Optional[str] = None,
) -> Callable[[F], F]:
    """
    Decorator for timing async function execution.

    Args:
        metric_type: Type of metric (histogram or summary)
        name: Metric name
        observe_func: Function to call for recording observations
        labels_func: Optional function to generate label values from function args
        track_in_progress: Whether to track in-progress operations
        track_in_progress_func: Function to call for tracking in-progress operations
        in_progress_metric: Optional name of gauge metric for tracking in-progress operations

    Returns:
        Decorator function
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Generate labels if a function was provided
            labels = None
            if labels_func:
                labels = labels_func(*args, **kwargs)

            # Start timing
            start_time = time.monotonic()

            # Track start of operation if requested
            if track_in_progress and track_in_progress_func and in_progress_metric and labels:
                track_in_progress_func(in_progress_metric, labels, 1)

            try:
                # Execute the function
                return await func(*args, **kwargs)
            finally:
                # Record duration
                duration = time.monotonic() - start_time

                # Call the observe function
                observe_func(name, duration, labels)

                # Track end of operation if requested
                if track_in_progress and track_in_progress_func and in_progress_metric and labels:
                    track_in_progress_func(in_progress_metric, labels, -1)

        return cast(F, wrapper)

    return decorator
