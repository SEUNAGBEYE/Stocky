""" Module for generic string length validators. """

from marshmallow import ValidationError

from ..messages.error_messages import serialization_errors 

def string_length_validator(length):
    """ Returns a function that checks data over a given length
    Args:
        length (Integer): Length a string must not exceed
    Returns:
        Function which validates length of the data
    """

    def length_validator(data):
        """ Checks if data does not exceed a given length
            Args:
                data (String): data to be validated
            Raises:
                validation error if data exceeds a given length
        """

        if len(data) > length:
            raise ValidationError(serialization_errors['must_be_less_than'].format(length))

    return length_validator


def empty_string_validator(string):
    """Checks if string is not empty
    
    Args:
        string (str): the string to be validated
    """
    if len(string.strip()) < 1:
        raise ValidationError(serialization_errors['cannot_be_empty'])
