# app/core/rate_limiting/models.py
from __future__ import annotations

"""
Rate limiting data models.

This module defines the data models for rate limiting, including strategies
and rule configurations for flexible rate limiting rules.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class RateLimitStrategy(str, Enum):
    """Strategy for determining the rate limit key."""

    IP = "ip"
    USER = "user"
    COMBINED = "combined"


@dataclass
class RateLimitRule:
    """Rule configuration for rate limiting.

    Attributes:
        requests_per_window: Maximum number of requests allowed in the window.
        window_seconds: Size of the window in seconds.
        strategy: Strategy for determining the rate limit key.
        burst_multiplier: Multiplier for burst allowance above the limit.
        path_pattern: Pattern to match request paths this rule applies to.
            If None, applies to all paths.
        exclude_paths: List of path prefixes to exclude from rate limiting.
    """

    requests_per_window: int
    window_seconds: int
    strategy: RateLimitStrategy = RateLimitStrategy.IP
    burst_multiplier: float = 1.5
    path_pattern: Optional[str] = None
    exclude_paths: List[str] = field(default_factory=list)
