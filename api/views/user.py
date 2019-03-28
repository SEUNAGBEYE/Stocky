from flask import request
from flask_restplus import Resource

from main import api
from ..schemas.user_schema import RegistrationSchema, LoginSchema
from ..utilities.responses.success_response import success_response
from ..middlewares.token_required import token_required
from ..middlewares.is_admin import is_admin


@api.route('/users/register')
class UserRegistration(Resource):
    
    def post(self):
        request_data = request.get_json()
        registration_schema = RegistrationSchema()
        user_data = registration_schema.load_object_into_schema(request_data)
        new_user = registration_schema.register(user_data)
        return success_response(new_user, 'User successfully created', 201)
    
    def get(self):
        return 'Make a post request to create a user'

@api.route('/users/login')
class UserLogin(Resource):
    
    def post(self):
        request_data = request.get_json()
        login_schema = LoginSchema()
        user_data = login_schema.load_object_into_schema(request_data)
        logged_in_user = login_schema.login()
        return success_response(logged_in_user, 'User successfully logged in')
    
    def get(self):
        return 'Make a post request to login'


@api.route('/users')
class UserRetrievealUpdate(Resource):

    @token_required
    def patch(self):
        return 'Authorized'

    @token_required
    @is_admin
    def delete(self):
        return 'Authorized'