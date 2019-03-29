
"""Celery Tasks"""
import threading
from datetime import datetime

from main import celery_app
from manage import app
from api.models import Stock, User
from ..services.email_factories.email_builder import build_email_sender

app.app_context().push()

@celery_app.task(name='send_stock_notification')
def send_stock_notification():
    """Checks if the age of the last stock in the db is old enough for notification.

    Example:
        Notifications are sent by 10 am and 10pm every day
    """

    latest_stock_age = Stock.query.order_by(
        Stock.created_at.desc()
    ).first().created_at
    
    due = datetime.now().day - latest_stock_age.day <= 1

    if due:
        mail_body = 'Hi, New stocks has been uploaded please login to see stock trends'
        email_sender = build_email_sender('flask_mail')
        notification_threads = []

        for user in User.query.all():
            notification_thread = threading.Thread(
                target=email_sender.send_mail_without_template,
                args=([user.email], 'New Stock Uploaded', mail_body)
            )
            notification_threads.append(notification_thread)
            notification_thread.start()
        
        # called join here to avoid blocking inside the upper loop
        [thread.join() for thread in notification_threads]
    
