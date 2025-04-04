from __future__ import annotations
import functools
import time
from contextlib import contextmanager
from typing import Any, Callable, Dict, Generator, Optional, cast
from app.logging import get_logger
from app.core.metrics.base import F
logger = get_logger('app.core.metrics.decorators')
@contextmanager
def timer(metric_type: str, name: str, observe_func: Callable[[str, float, Optional[Dict[str, str]]], None], labels: Optional[Dict[str, str]]=None, track_in_progress: bool=False, track_in_progress_func: Optional[Callable[[str, Dict[str, str], int], None]]=None, in_progress_metric: Optional[str]=None) -> Generator[None, None, None]:
    start_time = time.monotonic()
    if track_in_progress and track_in_progress_func and in_progress_metric and labels:
        track_in_progress_func(in_progress_metric, labels, 1)
    try:
        yield
    finally:
        duration = time.monotonic() - start_time
        observe_func(name, duration, labels)
        if track_in_progress and track_in_progress_func and in_progress_metric and labels:
            track_in_progress_func(in_progress_metric, labels, -1)
def timed(metric_type: str, name: str, observe_func: Callable[[str, float, Optional[Dict[str, str]]], None], labels_func: Optional[Callable[..., Dict[str, str]]]=None, track_in_progress: bool=False, track_in_progress_func: Optional[Callable[[str, Dict[str, str], int], None]]=None, in_progress_metric: Optional[str]=None) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            labels = None
            if labels_func:
                labels = labels_func(*args, **kwargs)
            with timer(metric_type, name, observe_func, labels, track_in_progress, track_in_progress_func, in_progress_metric):
                return func(*args, **kwargs)
        return cast(F, wrapper)
    return decorator
def async_timed(metric_type: str, name: str, observe_func: Callable[[str, float, Optional[Dict[str, str]]], None], labels_func: Optional[Callable[..., Dict[str, str]]]=None, track_in_progress: bool=False, track_in_progress_func: Optional[Callable[[str, Dict[str, str], int], None]]=None, in_progress_metric: Optional[str]=None) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            labels = None
            if labels_func:
                labels = labels_func(*args, **kwargs)
            start_time = time.monotonic()
            if track_in_progress and track_in_progress_func and in_progress_metric and labels:
                track_in_progress_func(in_progress_metric, labels, 1)
            try:
                return await func(*args, **kwargs)
            finally:
                duration = time.monotonic() - start_time
                observe_func(name, duration, labels)
                if track_in_progress and track_in_progress_func and in_progress_metric and labels:
                    track_in_progress_func(in_progress_metric, labels, -1)
        return cast(F, wrapper)
    return decorator