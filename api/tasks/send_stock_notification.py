
"""Celery Tasks"""
from main import celery_app

@celery_app.task(name='stock_notification')
def send_stock_notification():
    """Checks if the age of the last stock in the db is old enough for notification.

    Example:
        Notifications are sent by 10 am and 10pm every day
    """
    import threading
    from api.models import Stock, User
    from datetime import datetime

    latest_stock_age = Stock.query.order_by(
        Stock.created_at.desc()
    ).first().created_at
    
    if datetime.day() - latest_stock_age.day >= 1:

        notification_threads = []

        for user in User.query.all():
            notification_thread = threading.Thread(target=lambda x: x, args=('x'))
            notification_threads.append(notification_thread)
            notification_threads.start()
        
        # called join here to avoid blocking inside the upper loop
        [thread.join() for thread in notification_threads]
    
