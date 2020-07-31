from .. import db


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    users = db.relationship('User', backref='role', lazy='dynamic')

class Opshop(db.Model):
    __tablename__ = 'opshop'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(100))
    staff_count = db.Column(db.Integer)
    status = db.Column(db.String(20))
    users = db.relationship('User', backref='opshop', lazy='dynamic')
    books = db.relationship('Book', backref='opshop', lazy='dynamic')

class ItemType(db.Model):
    __tablename__ = 'itemtype'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    items = db.relationship('Book', backref='item_type', lazy='dynamic')

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.String(100), primary_key=True)
    opshop_id = db.Column(db.Integer, db.ForeignKey('opshop.id'), nullable=False)
    customer_address = db.Column(db.String(100))
    customer_name = db.Column(db.String(100))
    customer_contact = db.Column(db.String(100))
    date = db.Column(db.DateTime)
    status = db.Column(db.String(20))

class Book(db.Model):
    __tablename__ = 'book'
    # book_id should from eBay
    id = db.Column(db.String(100), primary_key=True)
    book_id_ebay = db.Column(db.String(100))
    opshop_id = db.Column(db.Integer, db.ForeignKey('opshop.id'), nullable=False)
    item_type_id = db.Column(db.Integer, db.ForeignKey('itemtype.id'), nullable=False)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    publisher = db.Column(db.String(100))
    edition = db.Column(db.Integer)
    page_count = db.Column(db.Integer)
    genre = db.Column(db.String(20))
    cover = db.Column(db.String(100)) # AMZON S3 --> https://applicationurl/cover/1.jpg
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    description = db.Column(db.String(300))
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime)
    status = db.Column(db.String(20))
    ISBN_10 = db.Column(db.String(100))
    ISBN_13 = db.Column(db.String(100))
    notes = db.Column(db.String(300))
    condition = db.Column(db.Integer)

class OrderItems(db.Model):
    __tablename__ = 'orderitem'
    order_id = db.Column(db.String(100), db.ForeignKey('order.id'), primary_key=True)
    item_id = db.Column(db.String(100), db.ForeignKey('book.id'), primary_key=True)
    quantity = db.Column(db.Integer)
    single_price = db.Column(db.Float)
    total_price = db.Column(db.Float)

class Image(db.Model):
    __tablename__='image'
    id = db.Column(db.Integer, primary_key=True)
    aws_link = db.Column(db.String(100))
    item_id = db.Column(db.String(100), db.ForeignKey('book.id'))