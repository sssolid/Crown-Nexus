from __future__ import annotations
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