"""Module to test user model"""

from api.models import User

class TestUserModel:
    """Test user model"""

    def test_new_user(self, init_db, new_user):
        """Test for creating a new user"""
        assert new_user == new_user.save()

    def test_get(self, new_user):
        """Test for get method"""
        assert User.get(new_user.id) == new_user

    def test_update(self, new_user):
        """Test for update method"""
        new_user.update_(first_name='Lorem')
        assert new_user.first_name == 'Lorem'

    def test_count(self, new_user):
        """Test for count of users"""
        assert new_user.count() == 1

    def test_query(self, new_user):
        """Test for query method"""
        pass

    def test_delete(self, new_user):
        """Test for delete method"""
        new_user.delete()

    def test_user_repr(self, new_user):
        """Should return the user first name and last name

        Args:
            new_user (object): Fixture to create a new user
        """
        assert repr(new_user) == f'<User {new_user.first_name} {new_user.last_name}>'
