"""Configuring Celery Beat used for running periodic tasks"""

# Third Party
from celery.schedules import crontab

from main import celery_app

celery_app.conf.beat_schedule = {
    'run-notify-user-every-day-by-10am': {
        'task': 'send_stock_notification',
        'schedule': crontab(hour=10),  # You can replace this with timedelta(seconds=5) to test
        'args': ()
    },
    'run-notify-user-every-day-by-10pm': {
        'task': 'send_stock_notification',
        'schedule': crontab(hour=20),
        'args': ()
    },
}
