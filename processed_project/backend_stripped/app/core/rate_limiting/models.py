from __future__ import annotations
'\nRate limiting data models.\n\nThis module defines the data models for rate limiting, including strategies\nand rule configurations for flexible rate limiting rules.\n'
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
class RateLimitStrategy(str, Enum):
    IP = 'ip'
    USER = 'user'
    COMBINED = 'combined'
@dataclass
class RateLimitRule:
    requests_per_window: int
    window_seconds: int
    strategy: RateLimitStrategy = RateLimitStrategy.IP
    burst_multiplier: float = 1.5
    path_pattern: Optional[str] = None
    exclude_paths: List[str] = field(default_factory=list)