import pytest
from faker import Faker

from api.utilities.enums import IsAdmin

fake = Faker()

@pytest.fixture(scope='module')
def mock_user():

    def user(is_admin='no'):

        return {
            'firstName': fake.name(),
            'lastName': fake.name(),
            'email': fake.email(),
            'password': fake.password(),
            'isAdmin': is_admin
        }

    return user
