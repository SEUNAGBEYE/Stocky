"""Configure celery worker instance """
from os import getenv

from config import config
from main import celery_app, create_app

# get flask config name from env or default to production config
config_name = getenv('FLASK_ENV', default='production')

app = create_app(config[config_name])
app.app_context().push()
