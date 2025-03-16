from __future__ import annotations
import os
from celery import Celery
from celery.schedules import crontab
from app.core.config import settings
os.environ.setdefault('CELERY_CONFIG_MODULE', 'app.core.celeryconfig')
celery_app = Celery('crown_nexus')
celery_app.config_from_object('app.core.celeryconfig')
import app.tasks.currency_tasks
celery_app.conf.beat_schedule = {'update-exchange-rates': {'task': 'app.tasks.currency_tasks.update_exchange_rates', 'schedule': crontab(hour=1, minute=0), 'options': {'expires': 3600}}}
def get_celery_app() -> Celery:
    return celery_app