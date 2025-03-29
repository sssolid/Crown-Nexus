# Module: app.core.metrics.base

**Path:** `app/core/metrics/base.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, TypeVar
```

## Global Variables
```python
F = F = TypeVar("F", bound=Callable[..., Any])
```

## Classes

| Class | Description |
| --- | --- |
| `MetricName` |  |
| `MetricTag` |  |
| `MetricType` |  |
| `MetricsConfig` |  |

### Class: `MetricName`

#### Attributes

| Name | Value |
| --- | --- |
| `HTTP_REQUESTS_TOTAL` | `'http_requests_total'` |
| `HTTP_REQUEST_DURATION_SECONDS` | `'http_request_duration_seconds'` |
| `HTTP_REQUEST_SIZE_BYTES` | `'http_request_size_bytes'` |
| `HTTP_RESPONSE_SIZE_BYTES` | `'http_response_size_bytes'` |
| `HTTP_ERRORS_TOTAL` | `'http_errors_total'` |
| `HTTP_IN_PROGRESS` | `'http_requests_in_progress'` |
| `DB_QUERIES_TOTAL` | `'db_queries_total'` |
| `DB_QUERY_DURATION_SECONDS` | `'db_query_duration_seconds'` |
| `DB_CONNECTIONS_TOTAL` | `'db_connections_total'` |
| `DB_CONNECTIONS_IN_USE` | `'db_connections_in_use'` |
| `DB_TRANSACTION_DURATION_SECONDS` | `'db_transaction_duration_seconds'` |
| `DB_ERRORS_TOTAL` | `'db_errors_total'` |
| `SERVICE_CALLS_TOTAL` | `'service_calls_total'` |
| `SERVICE_CALL_DURATION_SECONDS` | `'service_call_duration_seconds'` |
| `SERVICE_ERRORS_TOTAL` | `'service_errors_total'` |
| `CACHE_HIT_TOTAL` | `'cache_hit_total'` |
| `CACHE_MISS_TOTAL` | `'cache_miss_total'` |
| `CACHE_OPERATIONS_TOTAL` | `'cache_operations_total'` |
| `CACHE_OPERATION_DURATION_SECONDS` | `'cache_operation_duration_seconds'` |
| `USER_LOGINS_TOTAL` | `'user_logins_total'` |
| `ORDERS_TOTAL` | `'orders_total'` |
| `PRODUCTS_CREATED_TOTAL` | `'products_created_total'` |
| `SYSTEM_MEMORY_BYTES` | `'system_memory_bytes'` |
| `SYSTEM_CPU_USAGE` | `'system_cpu_usage'` |
| `SYSTEM_DISK_USAGE_BYTES` | `'system_disk_usage_bytes'` |
| `PROCESS_RESIDENT_MEMORY_BYTES` | `'process_resident_memory_bytes'` |
| `PROCESS_VIRTUAL_MEMORY_BYTES` | `'process_virtual_memory_bytes'` |
| `PROCESS_CPU_SECONDS_TOTAL` | `'process_cpu_seconds_total'` |
| `PROCESS_OPEN_FDS` | `'process_open_fds'` |

### Class: `MetricTag`

#### Attributes

| Name | Value |
| --- | --- |
| `SERVICE` | `'service'` |
| `ENVIRONMENT` | `'environment'` |
| `VERSION` | `'version'` |
| `INSTANCE` | `'instance'` |
| `ENDPOINT` | `'endpoint'` |
| `METHOD` | `'method'` |
| `PATH` | `'path'` |
| `STATUS_CODE` | `'status_code'` |
| `OPERATION` | `'operation'` |
| `ENTITY` | `'entity'` |
| `QUERY_TYPE` | `'query_type'` |
| `COMPONENT` | `'component'` |
| `ACTION` | `'action'` |
| `ERROR_TYPE` | `'error_type'` |
| `ERROR_CODE` | `'error_code'` |
| `RESOURCE_TYPE` | `'resource_type'` |
| `RESOURCE_ID` | `'resource_id'` |
| `USER_ID` | `'user_id'` |
| `USER_ROLE` | `'user_role'` |
| `CACHE_HIT` | `'cache_hit'` |
| `CACHE_BACKEND` | `'cache_backend'` |

### Class: `MetricType`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `COUNTER` | `'counter'` |
| `GAUGE` | `'gauge'` |
| `HISTOGRAM` | `'histogram'` |
| `SUMMARY` | `'summary'` |

### Class: `MetricsConfig`
**Decorators:**
- `@dataclass`
