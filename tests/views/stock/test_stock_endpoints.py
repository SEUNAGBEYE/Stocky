"""Module for stock endpoints"""

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


class TestStockEndpoint:
    """
    Test class for stock endpoints
    """

    def test_upload_stocks_with_valid_file_succeeds(
        self, init_db, client, mock_user, auth_header_form_data,
        stock_file
        ):
        """
        Should upload stocks with 201 response

        """

        data = dict(
            file=(stock_file, 'stock.csv')
        )
        response = client.post(
            f'{API_V1_BASE_URL}/stocks',
            data=data,
            headers=auth_header_form_data
        )

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 201
        assert response_json['status'] == 'Success'
        assert len(response_json['data']) > 0
    
    def test_upload_stocks_with_invalid_file_fails(
        self, init_db, client, auth_header_form_data, stock_file
        ):
        """
        Should fail, and return both errors and a response code of 400
        """

        data = dict(
            file=(stock_file, 'stock.pdf')
        )
        response = client.post(
            f'{API_V1_BASE_URL}/stocks',
            data=data,
            headers=auth_header_form_data
        )

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == error_dict['invalid_file_type']

    def test_upload_stocks_with_no_file_fails(
        self, init_db, client, auth_header_form_data,
        ):
        """
        Should fail, and return both errors and a response code of 400
        """

        data = dict()
        response = client.post(
            f'{API_V1_BASE_URL}/stocks',
            data=data,
            headers=auth_header_form_data
        )

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == error_dict['no_file']

    def test_get_stocks_succeeds(
        self, init_db, client, auth_header
        ):
        """
        Should return a list of paginated stocks with a status code of 200
        """
        response = client.get(
            f'{API_V1_BASE_URL}/stocks',
            headers=auth_header
        )

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'Success'
        assert 'meta' in response_json
        assert len(response_json) > 0

    def test_get_stocks_with_valid_search_queries_succeeds(
        self, init_db, client, auth_header
        ):
        """
        Should return a list of paginated stocks with a status code of 200
        """
        response = client.get(
            f'{API_V1_BASE_URL}/stocks?key=startCreatedAt&value=2011-10-10',
            headers=auth_header
        )

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'Success'
        assert 'meta' in response_json

    def test_get_stocks_with_invalid_search_queries_fails(
        self, init_db, client, auth_header
        ):
        """
        Should return a list of paginated stocks with a status code of 200
        """
        response = client.get(
            f'{API_V1_BASE_URL}/stocks?filter=true&createdAt=10',
            headers=auth_header
        )

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == error_dict['invalid_query']