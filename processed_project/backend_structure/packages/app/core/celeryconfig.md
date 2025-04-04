# Module: app.core.celeryconfig

**Path:** `app/core/celeryconfig.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from kombu import Exchange, Queue
from app.core.config import settings
```

## Global Variables
```python
broker_url = broker_url = settings.CELERY_BROKER_URL
result_backend = result_backend = settings.CELERY_RESULT_BACKEND
task_serializer = 'json'
accept_content = accept_content = ["json"]
result_serializer = 'json'
enable_utc = True
timezone = 'UTC'
task_acks_late = True
task_reject_on_worker_lost = True
task_time_limit = 1800
task_soft_time_limit = 1500
worker_prefetch_multiplier = 1
worker_concurrency = 4
worker_max_tasks_per_child = 100
task_default_queue = 'default'
task_queues = task_queues = (
    Queue("default", Exchange("default"), routing_key="default"),
    Queue("currency", Exchange("currency"), routing_key="currency"),
)
task_routes = task_routes = {
    "app.tasks.currency_tasks.*": {"queue": "currency"},
}
beat_schedule_filename = 'celerybeat-schedule'
```
