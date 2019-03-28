"""Development/Testing environment user deed data """

from faker import Faker

from api.utilities.enums import IsAdmin

faker = Faker()

def user_data():
    """Gets user data to be seeded.

    Returns:
        (list): user data to be seeded into the db.
    """

    return [
        {
            'first_name': faker.name(),
            'last_name': faker.name(),
            'email': 'admin@stocky.com',
            'is_admin': IsAdmin.yes,
            'password': faker.password(),
        },
        {
            'first_name': faker.name(),
            'last_name': faker.name(),
            'email': 'test-user@stocky.com',
            'is_admin': IsAdmin.no,
            'password': faker.password()
        }
    ]
