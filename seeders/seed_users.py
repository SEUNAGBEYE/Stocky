"""Module for seeding users"""

from api.models import User
from .data import get_data


def seed_users():
    user_data = get_data('user')
    User.bulk_create(user_data)