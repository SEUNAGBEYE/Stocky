"""Development/Testing environment user deed data """

from api.utilities.enums import IsAdmin

def user_data():
    """Gets user data to be seeded.

    Returns:
        (list): user data to be seeded into the db.
    """

    return [
        {
            'first_name': 'Admin',
            'last_name': 'User',
            'email': 'admin@stocky.com',
            'is_admin': IsAdmin.yes
        },
        {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test-user@stocky.com',
            'is_admin': IsAdmin.no
        }
    ]
