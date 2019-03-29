"""Module for token generation"""

from os import getenv
from datetime import datetime
from base64 import b64encode, b64decode, encode
import jwt

from faker import Faker

from api.utilities.constants import CHARSET
from api.utilities.enums import IsAdmin
from api.models.user import User


fake = Faker()

def generate_token(exp=None):
    """
    Generates jwt tokens for testing purpose

    Args:
        exp: Token Expiration. This could be datetime object or an integer
    Returns:
        token: This is the bearer token in this format 'Bearer token'
    """

    secret_key = getenv('JWT_SECRET_KEY')
    user = {
        'first_name': fake.name(),
        'last_name': fake.name(),
        'email': fake.email(),
        'is_admin': IsAdmin.yes,
        'password': fake.password()
    }

    payload = {'id': str(User.find_or_create(user, email=user['email']).id)}
    payload.__setitem__('exp', exp) if exp is not None else ''
    token = jwt.encode(payload, secret_key, algorithm='HS256').decode(CHARSET)
    return 'Bearer {0}'.format(token)
