""" Module with user model schemas. """

# Third Party
from marshmallow import (fields, post_load, validates, ValidationError, validates_schema)
from marshmallow_enum import EnumField

from ..utilities.validators.email_validator import email_validator
from ..utilities.validators.string_length_validators import string_length_validator
from ..utilities.enums import IsAdmin
from ..models import User

# Schemas
from .base_schema import BaseSchema

class UserSchema(BaseSchema):
    email = fields.String(required=True, validate=email_validator)
    token = fields.String(dump_only=True)
    password = fields.String(required=True, validate=(string_length_validator(60)))

class RegistrationSchema(UserSchema):
    """User model schema. """

    first_name = fields.String(
        required=True,
        dump_to='firstName',
        load_from='firstName',
        validate=(string_length_validator(60)),
        )
    last_name = fields.String(
        required=True, 
        validate=(string_length_validator(60)),
        dump_to='lastName',
        load_from='lastName'
    )
    is_admin = EnumField(
        IsAdmin, 
        required=True, 
        load_by=EnumField.VALUE,
        dump_by=EnumField.VALUE, 
        error='Please provide one of {values}',
        dump_to='isAdmin',
        load_from='isAdmin'
        )
    
    @validates('email')
    def validate_email(self, value):
        user = User.query.filter_by(email=value).first()
        if user:
            raise ValidationError('User Already exists')


    def register(self, data):
        user = User(**data).save()
        return self.dump(user).data

class LoginSchema(UserSchema):

    @post_load
    def validate(self, data):
        from manage import bcrypt

        user = User.query.filter_by(email=data['email']).first()
        if not user or not bcrypt.check_password_hash(user.password, data['password']):
            raise ValidationError({'error': 'Incorrect password or email'})
        
        self.context['user'] = user

    def login(self):
        return self.dump(self.context.get('user')).data

    