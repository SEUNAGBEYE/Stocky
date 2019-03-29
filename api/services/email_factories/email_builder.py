"""Email Builder Module"""

from .email_interface import EmailInterface
from .flask_mail import FlaskMail

EMAIL_SENDER_MAPPER = {
    'flask_mail': FlaskMail,
}


def build_email_sender(sender):
    """Builds the email sender class from concrete classes

    Args:
        sender (str): a string representing the concrete class
    """

    email_sender_class = EMAIL_SENDER_MAPPER.get(
        str(sender).lower())

    if not email_sender_class:
        raise NotImplementedError(
            f'You must implement the {sender} concrete class or choose one of the following {[concrete_class for concrete_class in EMAIL_SENDER_MAPPER]}'
        )

    try:
        if not isinstance(email_sender_class(), EmailInterface):
            raise Exception(
                f'{sender} concrete class must inherit from  EmailInterface'
            )
    except TypeError:
        raise Exception(
            f'{sender} object of type {type(email_sender_class)} is not callable'
        )

    return email_sender_class
