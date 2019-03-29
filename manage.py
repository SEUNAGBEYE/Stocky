"""Module with application entry point."""

# System imports
from os import getenv

# Third party Imports
import click
from flask import jsonify
from redis.exceptions import ConnectionError
from flask_mail import Mail
from sqlalchemy import text
from flask_bcrypt import Bcrypt

# Local Imports
from api.utilities.constants import SEED_OPTIONS
from api.utilities.celery_state import celery_task_state
from main import create_app
from config import config
from seeders import seed_db
from main import celery_app
from api.models.config import db

# get flask config name from env or default to production config
config_name = getenv('FLASK_ENV', default='production')

# create application object
app = create_app(config[config_name])
mail = Mail(app)
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    """Process / routes and returns 'Welcome to the Stock API' as json."""
    return jsonify(dict(message='Welcome to the Stock API api'))


@app.route('/health')
def health_check():
    """Checks the health of application and returns 'Health App Server' as json."""
    return jsonify(dict(message='Healthy App Server')), 200


@app.cli.command(context_settings=dict(token_normalize_func=str.lower))
@click.argument('resource_name', required=False)
@click.option(
    '--resource_name',
    help='The Resource name you want to seed.',
    type=click.Choice(SEED_OPTIONS))
def seed(resource_name):
    """
    Seeds the database with sample data

    Args:
        resource_name (string): The resource name you want to seed
    Return:
        func: call the function if successful or the click help option if unsuccesful
    """
    seed_db(resource_name)


@app.cli.command(context_settings=dict(token_normalize_func=str.lower))
@click.argument('table_name', required=False)
@click.option('--table_name', help='Table name to drop.')
def truncate(table_name=None):
    """
    Truncates the all tables
    """

    tables = db.engine.execute(
        text("""SELECT table_name
  FROM information_schema.tables
 WHERE table_schema='public'
   AND table_type='BASE TABLE'""")).fetchall()

    tables = ', '.join(
        [table[0] for table in tables if table[0] not in ('alembic_version')])

    if table_name:
        tables = table_name
    db.engine.execute(text(f'TRUNCATE {tables} CASCADE'))


@app.route('/celery/health')
def celery_stats():
    """Checks tasks queued by celery.

    if celery is up the response should have `sample_scheduler` task
    """

    msg = None

    ins = celery_app.control.inspect()

    try:
        tasks = ins.registered_tasks()
        msg = {"tasks": tasks, "status": "Celery up"}
    except ConnectionError:
        msg = {"status": "Redis server down"}
    except Exception:
        msg = {"status": "Celery down"}

    return jsonify(dict(data=msg, message='Success')), 200


@app.route('/celery-beat/health')
def celery_beat_stats():
    """Checks tasks scheduled by celery-beat."""

    import shelve

    down_tasks = {}
    ok_tasks = {}

    file_data = shelve.open(
        'celerybeat-schedule'
    )  # Name of the file used by PersistentScheduler to store the last run times of periodic tasks.

    entries = file_data.get('entries')

    if not entries:
        return jsonify(dict(error="celery-beat service not available")), 503

    for task_name, task in entries.items():

        try:
            celery_task_state(
                task, task_name, ok_tasks, down_tasks, is_cron_task=False)

        except AttributeError:

            celery_task_state(task, task_name, ok_tasks, down_tasks)

    if down_tasks:
        return jsonify(dict(message={
            'Down tasks': down_tasks,
        })), 503

    return jsonify(dict(message={'Okay tasks': ok_tasks})), 200


if __name__ == '__main__':
    app.run()
