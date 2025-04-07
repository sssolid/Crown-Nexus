# /app/core/metrics/base.py
"""Base types and interfaces for the metrics system.

This module defines common types, enums, and interfaces used throughout
the metrics components.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


class MetricType(str, Enum):
    """Enum for different types of metrics."""

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


class MetricTag:
    """Common metric tag names for consistent labeling."""

    # Standard tags
    SERVICE = "service"
    ENVIRONMENT = "environment"
    VERSION = "version"
    INSTANCE = "instance"

    # API tags
    ENDPOINT = "endpoint"
    METHOD = "method"
    PATH = "path"
    STATUS_CODE = "status_code"

    # Database tags
    OPERATION = "operation"
    ENTITY = "entity"
    QUERY_TYPE = "query_type"

    # Service tags
    COMPONENT = "component"
    ACTION = "action"

    # Error tags
    ERROR_TYPE = "error_type"
    ERROR_CODE = "error_code"

    # Resource tags
    RESOURCE_TYPE = "resource_type"
    RESOURCE_ID = "resource_id"

    # User tags
    USER_ID = "user_id"
    USER_ROLE = "user_role"

    # Cache tags
    CACHE_HIT = "cache_hit"
    CACHE_BACKEND = "cache_backend"

    # Suspicious tags
    SUSPICIOUS = "suspicious"

    # Rate Limiter tags
    LIMITED = "limited"

    # Response Formatting tags
    RESPONSE_FORMATTED = "response_formatted"

    # HTTP Request tags
    AGENT_TYPE = "agent_type"


class MetricName(str, Enum):
    """Common metric names for consistent measurement."""

    # HTTP metrics
    HTTP_REQUESTS_TOTAL = "http_requests_total"
    HTTP_REQUEST_DURATION_SECONDS = "http_request_duration_seconds"
    HTTP_REQUEST_SIZE_BYTES = "http_request_size_bytes"
    HTTP_REQUEST_ERRORS_TOTAL = "http_request_errors_total"
    HTTP_REQUESTS_BY_AGENT_TOTAL = "http_requests_by_agent_total"
    HTTP_RESPONSE_SIZE_BYTES = "http_response_size_bytes"
    HTTP_ERRORS_TOTAL = "http_errors_total"
    HTTP_IN_PROGRESS = "http_requests_in_progress"

    # Database metrics
    DB_QUERIES_TOTAL = "db_queries_total"
    DB_QUERY_DURATION_SECONDS = "db_query_duration_seconds"
    DB_CONNECTIONS_TOTAL = "db_connections_total"
    DB_CONNECTIONS_IN_USE = "db_connections_in_use"
    DB_TRANSACTION_DURATION_SECONDS = "db_transaction_duration_seconds"
    DB_ERRORS_TOTAL = "db_errors_total"

    # Service metrics
    SERVICE_CALLS_TOTAL = "service_calls_total"
    SERVICE_CALL_DURATION_SECONDS = "service_call_duration_seconds"
    SERVICE_ERRORS_TOTAL = "service_errors_total"

    # Cache metrics
    CACHE_HIT_TOTAL = "cache_hit_total"
    CACHE_MISS_TOTAL = "cache_miss_total"
    CACHE_OPERATIONS_TOTAL = "cache_operations_total"
    CACHE_OPERATION_DURATION_SECONDS = "cache_operation_duration_seconds"

    # Business metrics
    USER_LOGINS_TOTAL = "user_logins_total"
    ORDERS_TOTAL = "orders_total"
    PRODUCTS_CREATED_TOTAL = "products_created_total"

    # System metrics
    SYSTEM_MEMORY_BYTES = "system_memory_bytes"
    SYSTEM_CPU_USAGE = "system_cpu_usage"
    SYSTEM_DISK_USAGE_BYTES = "system_disk_usage_bytes"

    # Process metrics
    PROCESS_RESIDENT_MEMORY_BYTES = "process_resident_memory_bytes"
    PROCESS_VIRTUAL_MEMORY_BYTES = "process_virtual_memory_bytes"
    PROCESS_CPU_SECONDS_TOTAL = "process_cpu_seconds_total"
    PROCESS_OPEN_FDS = "process_open_fds"

    # Custom/Advanced Metrics
    REQUEST_TRACE_DURATION_SECONDS = "request_trace_duration_seconds"
    RATE_LIMITING_CHECK_DURATION_SECONDS = "rate_limiting_check_duration_seconds"
    RATE_LIMITING_MIDDLEWARE_DURATION_SECONDS = (
        "rate_limiting_middleware_duration_seconds"
    )
    RATE_LIMITING_REQUESTS_TOTAL = "rate_limiting_requests_total"
    HTTP_STATUS_CODES_TOTAL = "http_status_codes_total"
    REQUEST_SECURITY_CHECK_DURATION_SECONDS = "request_security_check_duration_seconds"
    SECURITY_HEADERS_DURATION_SECONDS = "security_headers_duration_seconds"
    RESPONSE_FORMATTING_DURATION_SECONDS = "response_formatting_duration_seconds"


@dataclass
class MetricsConfig:
    """Configuration for the metrics system."""

    namespace: str = "crown_nexus"
    subsystem: str = "api"
    default_labels: Dict[str, str] = field(default_factory=dict)
    default_buckets: List[float] = field(
        default_factory=lambda: [
            0.001,
            0.005,
            0.01,
            0.025,
            0.05,
            0.075,
            0.1,
            0.25,
            0.5,
            0.75,
            1.0,
            2.5,
            5.0,
            7.5,
            10.0,
        ]
    )
    enable_prometheus: bool = True
    enable_endpoint: bool = True
    endpoint_port: int = 9090
    push_gateway: Optional[str] = None
    push_interval: int = 60  # seconds
    enable_default_metrics: bool = True
    enable_process_metrics: bool = True
    enable_platform_metrics: bool = True
