"""Module for Stock model."""

from datetime import datetime

from api.models.base import BaseModel

# Database
from .config import db


class Stock(BaseModel):
    """Class for stock db table."""

    __tablename__ = 'stocks'

    stock_name = db.Column(db.String(60), nullable=False)
    opening_price = db.Column(db.Float(), nullable=False)
    closing_price = db.Column(db.Float(), nullable=False)
    highest_price = db.Column(db.Float(), nullable=False)
    lowest_price = db.Column(db.Float(), nullable=False)
    number_of_shares = db.Column(db.Integer(), nullable=False)
    price_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<Stock {self.stock_name}>'
