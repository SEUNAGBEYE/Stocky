"""Module for pagination helpers"""

# Standard
from math import ceil

# Third Party Libraries
from flask import request

# Messages
from .messages.error_messages import serialization_errors

# Middlewares
from ..middlewares.base_validator import ValidationError

def validate_pagination_args(arg_value, arg_name):
    """
    Validates if the query strings are valid.

    Arguments:
        arg_value (string): Query string value
        arg_name (string): Query string name

    Raises:
        ValidationError: Use to raise exception if any error occur

    Returns:
        (int) -- Returns True or False
    """

    if arg_name == 'limit' and arg_value == 'None':
        return 10  # Defaults limit to 10 if not provided
    if arg_name == 'page' and arg_value == 'None':
        return 1  # Defaults page to 1 if not provided

    # Checks if the arg is >= 1
    if arg_value.isdigit() and int(arg_value) > 0:
        return int(arg_value)
    else:
        raise ValidationError({
            'message':
            serialization_errors['invalid_query_strings'].format(
                arg_name, arg_value)
        })


def generate_metadata(records_count):
    """Generates the pagination metadata object

    Args:
        records_count (int): The total record count

    Returns:
        tuple: A tuple with the limit, offset and pagination meta dict
    """

    root_url = request.url_root.strip('/')
    base_url = f'{root_url}{request.path}'
    current_page_url = request.url

    limit = validate_pagination_args(
        request.args.get('limit', 'None'), 'limit'
    )
    current_page_count = validate_pagination_args(
        request.args.get('page', 'None'), 'page'
    )

    first_page = f'{base_url}?page=1&limit={limit}'
    pages_count = ceil(records_count / limit)

    # when there are no records the default page_count should still be 1
    if pages_count == 0:
        pages_count = 1

    meta_message = None
    if current_page_count > pages_count:
        # If current_page_count > pages_count set current_page_count to pages_count
        current_page_count = pages_count
        first_page = f'{base_url}?page=1&limit={limit}'
        current_page_url = f'{base_url}?page={pages_count}&limit={limit}'
        meta_message = serialization_errors['last_page_returned']

    offset = (current_page_count - 1) * limit

    # pagination meta object
    pagination_object = {
        "firstPage": first_page,
        "currentPage": current_page_url,
        "nextPage": "",
        "previousPage": "",
        "page": current_page_count,
        "pagesCount": pages_count,
        "totalCount": records_count
    }

    previous_page_count = current_page_count - 1
    next_page_count = current_page_count + 1

    next_page_url = f'{base_url}?page={next_page_count}&limit={limit}'
    previous_page_url = f'{base_url}?page={previous_page_count}&limit={limit}'  # noqa

    if current_page_count > 1:
        # if current_page_count > 1 there should be a previous page url
        pagination_object['previousPage'] = previous_page_url

    if pages_count >= next_page_count:
        # if pages_count >= next_page_count there should be a next page url
        pagination_object['nextPage'] = next_page_url

    if meta_message:
        pagination_object['message'] = meta_message

    return limit, offset, pagination_object


def pagination_helper(model, schema, query):
    """Paginates records of a model.

    Usage:
        To use this function, the positional arguments (args) must be supplied in the right order e.g

        Example1: pagination_helper(model, schema)

        The the keyword arguments (kwargs) are optional i.e. any or none of the kwargs could be supplied e.g


    Args:
        model (class): Model to be paginated
        schema (class): Schema to be used for serialization

    Returns:
        tuple: Returns a tuple containing the paginated data and the
            paginated meta object or returns a tuple of None depending on
            whether the limit and page object is provided
    """

    records_count = query.count()
    limit, offset, pagination_object = generate_metadata(records_count)
    records = query.offset(offset).limit(limit)
    data = schema(many=True).dump(records).data

    return data, pagination_object
