"""Module for seeding users"""

from api.models import Stock
from .data import get_data


def seed_stocks():
    stock_data = get_data('stock')
    Stock.bulk_create(stock_data)