# backend/app/core/celery_app.py
"""
Celery configuration.

This module sets up the Celery application for background tasks:
- Task queue configuration
- Scheduled tasks
- Worker settings
"""

from __future__ import annotations

import os
from celery import Celery
from celery.schedules import crontab

# Set environment variables for Celery
os.environ.setdefault("CELERY_CONFIG_MODULE", "app.core.celeryconfig")

# Create Celery app
celery_app = Celery("crown_nexus")
celery_app.config_from_object("app.core.celeryconfig")

# Import tasks to ensure they're registered
import app.tasks.currency_tasks

# Define periodic tasks
celery_app.conf.beat_schedule = {
    "update-exchange-rates": {
        "task": "app.tasks.currency_tasks.update_exchange_rates",
        "schedule": crontab(hour=1, minute=0),  # Run at 1:00 AM every day
        "options": {"expires": 3600},  # Task expires after 1 hour
    },
}

# Make celery app available at module level
def get_celery_app() -> Celery:
    """Get the Celery application instance."""
    return celery_app
