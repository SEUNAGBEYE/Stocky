""" Module for base marshmallow schema. """
from marshmallow import Schema, fields

from ..middlewares.base_validator import ValidationError


class BaseSchema(Schema):
    """Base marshmallow schema with common attributes."""
    
    id = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True, dump_to='createdAt')
    updated_at = fields.DateTime(dump_only=True, dump_to='updatedAt')
    created_by = fields.String(dump_only=True, dump_to='createdBy')
    updated_by = fields.String(dump_only=True, dump_to='updatedBy')

    def load_json_into_schema(self, data):
        """Helper function to load raw json request data into schema"""
        data, errors = self.loads(data)

        if errors:
            raise ValidationError(
                dict(errors=errors, message='An error occurred'), 400)

        return data

    def load_object_into_schema(self, data, partial=False):
        """Helper function to load python objects into schema"""
        data, errors = self.load(data, partial=partial)

        if errors:
            raise ValidationError(
                dict(errors=errors, message='An error occurred'), 400)

        return data
