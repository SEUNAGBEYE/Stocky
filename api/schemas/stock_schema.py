""" Module with stock model schemas. """

# Third Party
from marshmallow import (fields, post_load, validates, ValidationError, validates_schema)

from ..utilities.validators.string_length_validators import string_length_validator
from ..utilities.enums import IsAdmin
from ..utilities.constants import ENUM_CHOICES
from ..utilities.messages.error_messages.serialization_errors import error_dict
from ..models import Stock

# Schemas
from .base_schema import BaseSchema

class StockSchema(BaseSchema):
    stock_name = fields.String(
        required=True,
        dump_to='stockName',
        validate=(string_length_validator(60))
    )
    closing_price = fields.Float(required=True, dump_to='closingPrice')
    opening_price = fields.Float(required=True, dump_to='openingPrice')
    highest_price = fields.Float(
        required=True,
        dump_to='highestPriceOfTheDay'
    )
    lowest_price = fields.Float(
        required=True,
        dump_to='lowestPriceOfTheDay'
    )
    number_of_shares = fields.Integer(
        required=True,
        dump_to='numberOfShares'
    )
    price_date = fields.DateTime(dump_to='priceDate')