# backend/app/core/celeryconfig.py
"""
Celery configuration settings.

This module contains all Celery configuration settings including:
- Broker and result backend
- Task serialization
- Worker settings
- Task routing
"""

from __future__ import annotations

from kombu import Exchange, Queue

from app.core.config import settings

# Broker settings
broker_url = settings.CELERY_BROKER_URL
result_backend = settings.CELERY_RESULT_BACKEND

# Task serialization
task_serializer = "json"
accept_content = ["json"]
result_serializer = "json"

# Time zone and enabling UTC
enable_utc = True
timezone = "UTC"

# Task settings
task_acks_late = True
task_reject_on_worker_lost = True
task_time_limit = 1800  # 30 minutes
task_soft_time_limit = 1500  # 25 minutes

# Worker settings
worker_prefetch_multiplier = 1
worker_concurrency = 4
worker_max_tasks_per_child = 100

# Queue configuration
task_default_queue = "default"
task_queues = (
    Queue("default", Exchange("default"), routing_key="default"),
    Queue("currency", Exchange("currency"), routing_key="currency"),
)

# Task routing
task_routes = {
    "app.tasks.currency_tasks.*": {"queue": "currency"},
}

# Beat settings (scheduler)
beat_schedule_filename = "celerybeat-schedule"
