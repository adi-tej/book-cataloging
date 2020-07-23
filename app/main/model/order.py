from .. import db

class Order(db.Model):
    """
    order table information
    """
    __tablename__ = 'order'

    order_id = db.Column(db.String(100), primary_key=True)
    opshop_id = db.Column(db.Integer, db.ForeignKey('opshop.opshop_id'), nullable=False)
    customer_address = db.Column(db.String(100))
    customer_name = db.Column(db.String(100))
    customer_contact = db.Column(db.String(100))
    order_date = db.Column(db.DateTime)
    order_status = db.Column(db.String(20))
    order_items = db.relationship('OrderItems', backref='order', lazy='dynamic')
