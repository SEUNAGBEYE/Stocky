""" Module with email validator. """
import re

from marshmallow import ValidationError
from ..messages.error_messages.serialization_errors import error_dict

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


def email_validator(data):
    """
    Checks if given string is at least 1 character and only contains characters.
    """

    data = data.lower()

    # Check if email pattern is matched
    if not EMAIL_REGEX.match(data):
        raise ValidationError(
            error_dict['email_syntax'])
