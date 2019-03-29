from flask import request
from flask_restplus import Resource
import pyexcel as pe


from main import api
from ..utilities.responses.success_response import success_response
from ..schemas.stock_schema import StockSchema
from ..middlewares.token_required import token_required
from ..middlewares.is_admin import is_admin
from ..models import Stock
from ..models.config import db

from ..utilities.paginator import pagination_helper
from ..middlewares.base_validator import ValidationError


@api.route('/stocks')
class StockResource(Resource):
    
    @token_required
    def get(self):

        query_mapper = {
            'stockName': lambda value: Stock.stock_name.ilike(value),
            'startCreatedAt': lambda value: Stock.created_at >= value,
            'endCreatedAt': lambda value: Stock.created_at <= value,
        }

        search_column = request.args.get('key')
        query = query_mapper.get(search_column)

        value = request.args.get('value')
    
        if search_column and query:
            query = Stock.query.filter(query(value))
        else:
            query = Stock.query

        stock_data = pagination_helper(Stock, StockSchema, query)
        return success_response(stock_data, 'Stock successfully fetched')
    
    def validate_file(self, file):
        empty_file_names = ['3e9', '527']
        if not file or file and file.filename in empty_file_names:
            raise ValidationError({'message': 'No file uploaded'})
        extension = file.filename.split(".")[-1]
        if not extension == 'csv':
            raise ValidationError({'message': 'File type not supported'})
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
        return success_response(stock_data, 'Stocks successfully uploaded')