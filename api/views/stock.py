"""Stock View Module"""

from datetime import datetime
from re import sub

from flask import request
from flask_restplus import Resource
import pyexcel as pe
from sqlalchemy import func


from main import api
from ..utilities.responses.success_response import success_response
from ..schemas.stock_schema import StockSchema
from ..middlewares.token_required import token_required
from ..middlewares.is_admin import is_admin
from ..models import Stock
from ..models.config import db
from ..utilities.paginator import pagination_helper
from ..middlewares.base_validator import ValidationError
from ..utilities.messages.error_messages.serialization_errors import error_dict


@api.route('/stocks')
class StockResource(Resource):


    @classmethod
    def to_snake_case(cls, string):
        """
        Converts a string in PascalCase or camelCase to snake_case one
        """
        return sub(r'(.)([A-Z])', r'\1_\2', string).lower()

    def process_query(self, column, op, value):
        """"Generates a filter query for a query params

        Args:
            column (sqlalchemmy.column): An instance of sqlalchemy column instance
            op (str): The operator for the query. ie =, <, >=, <=, ....
            value (str) The value to search for
        
        Returns:
            (query_object): Sqlalachemy query object
        """
        try:
            value = datetime.strptime(value, '%Y-%m-%d')
            column = func.DATE(column)
        except:
            pass
        
        # Maps the supported operators to their logical repr
        operators = {
            'lte': column <= value,
            '=': column == value if isinstance(value, datetime) else column.ilike(value),
            'gte': column >= value,
            'gt': column > value,
            'lt': column < value,
        }
        return operators.get(op)
    
    def process_queries(self, queries):
        """"Transforms the query params to what acceptable 
        self.process_query arguments

        Args:
            queries (list) A list of query objects
        """

        columns = Stock.__mapper__.columns # Gets all the column of the model

        for query_param, value in request.args.items():
            key_op = query_param.split('__') # Splits __ from the column name createdAt__lt ---> createdAt
            key, op = key_op if len(key_op) == 2 else (query_param, '=')
            column = columns.get(self.to_snake_case(key))
            if column is not None:
                queries.append(
                    self.process_query(column, op, value)
                )

    @token_required
    def get(self):

        queries = []
        
        if request.args.get('filter', '').lower() == 'true':
            self.process_queries(queries)

        if queries:
            query = Stock.query.filter(*queries) # spreads the queries to the filter func
        else:
            query = Stock.query
    
        try:
            # Pass the filter query to pagination helper for pagination
            stock_data, meta = pagination_helper(Stock, StockSchema, query)
        except:
            raise ValidationError({'message': error_dict['invalid_query']})
        return success_response(stock_data, 'Stock successfully fetched', meta=meta)
    
    def validate_file(self, file):
        """"Validates the file uploaded
        """
        empty_file_names = ['3e9', '527']
        if not file or file and file.filename in empty_file_names:
            raise ValidationError({'message': error_dict['no_file']})
        extension = file.filename.split(".")[-1]
        if not extension == 'csv':
            raise ValidationError({'message': error_dict['invalid_file_type']})
        return file, extension

    @token_required
    @is_admin
    def post(self):
        data, extension = self.validate_file(request.files.get('file'))
        content = data.read().decode('utf-8')
        pe.save_as(
            file_type=extension,
            file_content=content, name_columns_by_row=0,
            dest_session=db.session(), dest_table=Stock
        )

        stock_data = StockSchema(many=True).dump(Stock.query.all()).data
        return success_response(stock_data, 'Stocks successfully uploaded', 201)