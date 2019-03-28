"""Module for User model."""

from api.models.base import BaseModel
from api.utilities.enums import IsAdmin

# Database
from .config import db




class User(BaseModel):
    """Class for user db table."""

    __tablename__ = 'users'

    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    is_admin = db.Column(db.Enum(IsAdmin), nullable=False, default='yes')

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'
