"""Module for setting up fixtures for testing"""
# pylint: skip-file

# System libraries
import os

# Third-party libraries
import pytest

# Local imports
from main import create_app
from config import config


# Database
from api.models.config import db

config_name = 'testing'
os.environ['FLASK_ENV'] = config_name
V1_BASE_URL = os.getenv('API_BASE_URL_V1')

pytest_plugins = [
    'tests.fixtures.users', 'tests.fixtures.stocks',
    'tests.mocks.user', 'tests.fixtures.authorization',
    ]

@pytest.yield_fixture(scope='session')
def app():
    """
    Setup our flask test app, this only gets executed once.

    Returns:
        Flask app
    """

    _app = create_app(config[config_name])

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def client(app):
    """
    Setup an app client, this gets executed for each test function.


    Args:
        app: Pytest fixture

    Returns: 
        Flask app client
    """
    yield app.test_client()


@pytest.fixture(scope='module')
def init_db(app):
    db.create_all()
    yield db
    db.session.close()
    db.drop_all()
