"""Module for response"""
from flask import jsonify

def success_response(data, message, status_code=200, **kwargs):
    """Returns response for successfull requests
    Args:
        data (dict): Response data
        message (message): Response message
        status_code (int): Response status code.
            Defaults to 200 when not provided

    Returns:
        (tuple): A tuple of the data and status code
    
    """
    return {
        'status': 'Success',
        'message': message,
        'data': data,
        **kwargs
    }, status_code