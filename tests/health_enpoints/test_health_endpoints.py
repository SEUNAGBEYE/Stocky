from os import getenv

import pytest
import json

from api.utilities.constants import CHARSET

api_v1_base_url = getenv('API_BASE_URL_V1')

def test_index_endpoint(client):

    response = client.get('/')
    # response_json = json.loads(response.data.decode(CHARSET))