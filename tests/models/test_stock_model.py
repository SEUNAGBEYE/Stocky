"""Module to test stock model"""

from api.models import Stock

class TestStockModel:
    """Test stock model"""

    def test_new_stock(self, init_db, new_stock):
        """Test for creating a new stock"""
        assert new_stock == new_stock.save()

    def test_get(self, new_stock):
        """Test for get method"""
        assert Stock.get(new_stock.id) == new_stock

    def test_update(self, new_stock):
        """Test for update method"""
        new_stock.update_(stock_name='Lorem')
        assert new_stock.stock_name == 'Lorem'

    def test_count(self, new_stock):
        """Test for count of stocks"""
        assert new_stock.count() == 1

    def test_query(self, new_stock):
        """Test for query method"""
        pass

    def test_delete(self, new_stock, request_ctx):
        """Test for delete method"""
        new_stock.delete()

    def test_stock_repr(self, new_stock):
        """Should return the stock first name and last name

        Args:
            new_stock (object): Fixture to create a new stock
        """
        assert repr(new_stock) == f'<Stock {new_stock.stock_name}>'
