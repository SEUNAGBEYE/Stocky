"""Module for user endpoints"""

from os import getenv
from flask import json

from api.utilities.constants import (
    CHARSET,
    MIMETYPE,
    MISSING_FIELD, 
    ENUM_CHOICES
)

from api.utilities.messages.error_messages.serialization_errors import error_dict
from api.models import User
API_V1_BASE_URL = getenv('API_BASE_URL')


class TestUserEndpoint:
    """
    Test class for user endpoints
    """

    def test_register_user_with_valid_data_succeeds(
        self, init_db, client, mock_user, auth_header
        ):
        """
        Should create a user with 201 response

        """
        data = mock_user()
        response = client.post(
            f'{API_V1_BASE_URL}/users/register',
            data=json.dumps(data),
            headers=auth_header
        )

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 201
        assert response_json['status'] == 'Success'
        assert 'id' in response_json['data']
        assert response_json['data']['email'] == data['email']
        assert response_json['data']['firstName'] == data['firstName']
        assert response_json['data']['lastName'] == data['lastName']
    
    def test_register_user_with_uncompelete_data_fails(
        self, init_db, client, auth_header
        ):
        """
        Should fail, and return both errors and a response code of 400
        """
        data = {}
        response = client.post(
            f'{API_V1_BASE_URL}/users/register',
            data=json.dumps(data),
            headers=auth_header
        )

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['email'][0] == MISSING_FIELD
        assert response_json['errors']['password'][0] == MISSING_FIELD
        assert response_json['errors']['firstName'][0] == MISSING_FIELD
        assert response_json['errors']['lastName'][0] == MISSING_FIELD
        assert response_json['errors']['isAdmin'][0] == f'{ENUM_CHOICES} yes, no'

    def test_register_user_with_invalid_email_fails(
        self, init_db, client, auth_header
        ):
        """
        Should fail, and return both errors and a response code of 400
        """
        data = {'email': 'lorem'}
        response = client.post(
            f'{API_V1_BASE_URL}/users/register',
            data=json.dumps(data),
            headers=auth_header
        )

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['email'][0] == error_dict['email_syntax']
        assert response_json['errors']['password'][0] == MISSING_FIELD
        assert response_json['errors']['firstName'][0] == MISSING_FIELD
        assert response_json['errors']['lastName'][0] == MISSING_FIELD
        assert response_json['errors']['isAdmin'][0] == f'{ENUM_CHOICES} yes, no'

    def test_register_user_with_existing_user_fails(
        self, init_db, client, auth_header, existing_user,
        ):
        """
        Should fail, and return both errors and a response code of 400
        """
        user = existing_user.save()

        data = {
            'firstName': user.first_name,
            'lastName': user.first_name,
            'password': 'lorem',
            'email': user.email,
            'isAdmin': 'no',
            }

        response = client.post(
            f'{API_V1_BASE_URL}/users/register',
            data=json.dumps(data),
            headers=auth_header
        )

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['email'][0] == error_dict['user_exists']

    def test_login_user_with_correct_credentials_succeeds(
        self, init_db, client, new_user, auth_header
        ):
        """
        Should login a user with 200 response

        """
        data = {'email': new_user.email, 'password': new_user.password}
        user = new_user.save()
        response = client.post(
            f'{API_V1_BASE_URL}/users/login',
            data=json.dumps(data),
            headers=auth_header
        )

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'Success'
        assert response_json['data']['email'] == user.email
        assert response_json['data']['token'] == user.token
    
    def test_login_user_with_empty_data_fails(
        self, init_db, client, auth_header
        ):
        """
        Should fail, and return both errors and a response code of 400
        """
        data = {}
        response = client.post(
            f'{API_V1_BASE_URL}/users/login',
            data=json.dumps(data),
            headers=auth_header
        )

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['email'][0] == MISSING_FIELD
        assert response_json['errors']['password'][0] == MISSING_FIELD

    def test_login_user_with_invalid_crendentials_fails(
        self, init_db, client, auth_header
        ):
        """
        Should fail, and return both errors and a response code of 400
        """
        data = {'email': 'lorem@ip.com', 'password': 'ispsum'}
        response = client.post(
            f'{API_V1_BASE_URL}/users/login',
            data=json.dumps(data),
            headers=auth_header
        )

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['error'] == error_dict['invalid_email_or_pass']