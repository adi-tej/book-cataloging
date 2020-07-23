from .. import db

class Opshop(db.Model):
    __tablename__ = 'opshop'
    opshop_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    opshop_ebay_email = db.Column(db.String(100), nullable=False)
    opshop_name = db.Column(db.String(100), nullable=True)
    opshop_address = db.Column(db.String(100))
    staff_number = db.Column(db.Integer)
    opshop_status = db.Column(db.String(20))
    users = db.relationship('User', backref='opshop', lazy='dynamic')
    books = db.relationship('Book', backref='opshop', lazy='dynamic')