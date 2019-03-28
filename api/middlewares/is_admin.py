"""Module for admin validation"""

# Standard library
from functools import wraps

#Third party
from flask import request

#Utilities
from api.utilities.enums import IsAdmin


def is_admin(func):
    """Authentication decorator. Validates token from the client

    Args:
        func (function): Function to be decorated

    Returns:
        function: Decorated function

    Raises:
        ValidationError: Validation error
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        from .base_validator import ValidationError
        user = request.user
        if user.is_admin == IsAdmin.yes:
            return func(*args, **kwargs)
        raise ValidationError(
            {'message': 'You are not authorized to access this page'},
            403
        )

    return decorated_function
