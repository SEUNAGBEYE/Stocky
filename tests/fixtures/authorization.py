"""Module with authorization fixtures """

# Third Party Modules
import pytest


# Utilities
from api.utilities.helpers.generate_token import generate_token
from api.utilities.constants import MIMETYPE, MIMETYPE_TEXT, MIMETYPE_FORM_DATA


@pytest.fixture(scope='module')
def auth_header(generate_token=generate_token):
    return {
        'Authorization': generate_token(),
        'Content-Type': MIMETYPE,
        'Accept': MIMETYPE
    }


@pytest.fixture(scope='module')
def auth_header_text(generate_token=generate_token):
    return {
        'Authorization': generate_token(),
        'Content-Type': MIMETYPE_TEXT,
        'Accept': MIMETYPE_TEXT
    }


@pytest.fixture(scope='module')
def auth_header_form_data(generate_token=generate_token):
    return {
        'Authorization': generate_token(),
        'Content-Type': MIMETYPE_FORM_DATA,
        'Accept': MIMETYPE_FORM_DATA
    }

