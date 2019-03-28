"""Module with users fixtures """

# Third Party Modules
import pytest

from api.models import Stock

@pytest.fixture(scope='module')
def new_stock(app):
    params = {
            'stock_name': '7UP',
            'opening_price': 45.34,
            'closing_price': 45.88,
            'highest_price': 47.44,
            'lowest_price': 44.45,
            'number_of_shares': 100,
        }

    return Stock(**params)