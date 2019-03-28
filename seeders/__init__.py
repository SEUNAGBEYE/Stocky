"""Module for seeding sample data into the database """

# Standard library
from collections import OrderedDict
from os import getenv

# Third party
from sqlalchemy import text

# Database
# from api.models.config import db


def seed_db(resource_name=None):
    """Checks the argument provided and matches it to the respective seeder

    Args:
        resource_name (str): Name of resource

    Return:
        func: calls a function with the resource name as arguments
    """

    resource_order_mapping = OrderedDict()

    if resource_name:
        return resource_order_mapping.get(resource_name)()

    if getenv('FLASK_ENV') in ('development', 'testing'):
        from subprocess import call
        call(["flask", "truncate"])

    for _, resource in resource_order_mapping.items():
        resource()
