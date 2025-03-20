# /app/core/rate_limiting/models.py
"""Rate limiting models and types.

This module defines the data models and types used for rate limiting configuration.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class RateLimitStrategy(str, Enum):
    """Strategies for rate limiting.

    Defines the different strategies that can be used for rate limiting:
    - IP: Based on client IP address
    - USER: Based on authenticated user ID
    - COMBINED: Based on both IP address and user ID
    """

    IP = "ip"
    USER = "user"
    COMBINED = "combined"


@dataclass
class RateLimitRule:
    """Rule for rate limiting configuration.

    Attributes:
        requests_per_window: Number of allowed requests in the time window
        window_seconds: Time window in seconds
        strategy: Rate limiting strategy (IP, user, or combined)
        burst_multiplier: Multiplier for burst capacity (temporary overage)
        path_pattern: Optional regex pattern to match request paths
        exclude_paths: Optional list of path prefixes to exclude from rate limiting
    """

    requests_per_window: int
    window_seconds: int
    strategy: RateLimitStrategy = RateLimitStrategy.IP
    burst_multiplier: float = 1.5
    path_pattern: Optional[str] = None
    exclude_paths: List[str] = field(default_factory=list)
