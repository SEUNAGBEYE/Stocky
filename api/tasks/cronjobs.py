"""Configuring Celery Beat used for running periodic tasks"""

# Third Party
from celery.schedules import crontab

from main import celery_app

celery_app.conf.beat_schedule = {
    'run-notify-user-every-day-by-12am': {
        'task': 'send_stock_notification',
        'schedule': crontab(hour='*', minute=1),
        'args': ()
    },
}
