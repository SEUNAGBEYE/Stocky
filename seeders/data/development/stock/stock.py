"""Development/Testing environment user deed data"""


def stock_data():
    """Returns the stock's data to be seeded

    Returns:
        (list): stock data to be seeded into the db.
    """

    return [
        {
            'stock_name': '7UP',
            'opening_price': 45.34,
            'closing_price': 45.88,
            'highest_price': 47.44,
            'lowest_price': 44.45,
            'number_of_shares': 100,
        }
    ]
