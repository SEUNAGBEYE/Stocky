"""Module for User model."""

import jwt
from os import getenv

from sqlalchemy.event import listens_for

from api.models.base import BaseModel
from api.utilities.enums import IsAdmin

# Database
from .config import db


class User(BaseModel):
    """Class for user db table."""

    __tablename__ = 'users'

    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    is_admin = db.Column(db.Enum(IsAdmin), nullable=False, default='yes')

    def _generate_jwt_token(self):
        """
        Generates a JWT with user's id to expire in 60 days
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.id,
            'exp': int(dt.strftime('%s'))
        }, getenv('JWT_SECRET_KEY'), algorithm='HS256')

        return token.decode('utf-8')

    
    @property # makes this method available via user.token
    def token(self):
        """
        Generates JWT for user
        """
        return self._generate_jwt_token()

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'

@listens_for(User, 'before_insert')
def hash_password(mapper, connection, target):
    from manage import bcrypt
    target.password = bcrypt.generate_password_hash(target.password).decode('utf-8')
