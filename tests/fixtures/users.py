"""Module with users fixtures """

# Third Party Modules
import pytest
from faker import Faker

from api.utilities.enums import IsAdmin
from api.models import User

fake = Faker()

@pytest.fixture(scope='module')
def new_user(app):
    params = {
        'first_name': fake.name(),
        'last_name': fake.name(),
        'email': fake.email(),
        'password': fake.password(),
        'is_admin': IsAdmin.no
    }
    return User(**params)

@pytest.fixture(scope='module')
def existing_user(app):
    params = {
        'first_name': fake.name(),
        'last_name': fake.name(),
        'email': fake.email(),
        'password': fake.password(),
        'is_admin': IsAdmin.no
    }
    return User(**params).save()