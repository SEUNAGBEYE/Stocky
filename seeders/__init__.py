"""Module for seeding sample data into the database """

# Standard library
from collections import OrderedDict
from os import getenv

from .seed_users import seed_users
from .seed_stocks import seed_stocks

def seed_db(resource_name=None):
    """Checks the argument provided and matches it to the respective seeder

    Args:
        resource_name (str): Name of resource

    Return:
        func: calls a function with the resource name as arguments
    """

    resource_order_mapping = OrderedDict({
        'users': seed_users,
        'stocks': seed_stocks
    })

    if resource_name:
        return resource_order_mapping.get(resource_name)()

    if getenv('FLASK_ENV') in ('development', 'testing'):
        from subprocess import call
        call(["flask", "truncate"])

    for _, resource in resource_order_mapping.items():
        resource()
