"""Module with users fixtures """

from io import BytesIO

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

@pytest.fixture(scope='function')
def stock_file(app):
    params = {
            'stock_name': '7UP',
            'opening_price': 45.34,
            'closing_price': 45.88,
            'highest_price': 47.44,
            'lowest_price': 44.45,
            'number_of_shares': 100,
        }
    
    content = b"""stock_name,opening_price,closing_price,highest_price,lowest_price,number_of_shares
7up,3.45,100,60,20,100
Cocacola,6.45,102,40,30,120
Apple,300000,500000,450000,350000,10
Facebook,6000,100,605,205,102
Stanbic IBTC,35000,100,50,20,10
"""
    return BytesIO(content)