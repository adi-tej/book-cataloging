
from .. import db

class ItemType(db.Model):
    __tablename__ = 'itemtype'
    item_type_id = db.Column(db.Integer, primary_key=True)
    item_type_name = db.Column(db.String(20))
    items = db.relationship('Book', backref='item_type', lazy='dynamic')