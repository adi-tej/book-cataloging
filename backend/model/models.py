from app import db

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    opshop_id = db.Column(db.Integer, db.ForeignKey('opshop.opshop_id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)
    register_email = db.Column(db.String(50), unique=True, nullable=False)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Role(db.Model):
    __tablename__ = 'role'
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(20))
    users = db.relationship('User', backref='role', lazy='dynamic')

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

class ItemType(db.Model):
    __tablename__ = 'itemtype'
    item_type_id = db.Column(db.Integer, primary_key=True)
    item_type_name = db.Column(db.String(20))
    items = db.relationship('Book', backref='item_type', lazy='dynamic')

class Order(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.String(100), primary_key=True)
    opshop_id = db.Column(db.Integer, db.ForeignKey('opshop.opshop_id'), nullable=False)
    customer_address = db.Column(db.String(100))
    customer_name = db.Column(db.String(100))
    customer_contact = db.Column(db.String(100))
    order_date = db.Column(db.DateTime)
    order_status = db.Column(db.String(20))
    order_items = db.relationship('OrderItems', backref='order', lazy='dynamic')

class Book(db.Model):
    __tablename__ = 'book'
    # book_id should from eBay
    book_id_local = db.Column(db.String(100), primary_key=True)
    book_id_ebay = db.Column(db.String(100))
    opshop_id = db.Column(db.Integer, db.ForeignKey('opshop.opshop_id'), nullable=False)
    item_type_id = db.Column(db.Integer, db.ForeignKey('itemtype.item_type_id'), nullable=False)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    publisher = db.Column(db.String(100))
    publish_date = db.Column(db.DateTime)
    edition = db.Column(db.Integer)
    pages_number = db.Column(db.Integer)
    genre = db.Column(db.String(20))
    # all of the covers should be start with "https" NOT "http"
    cover1 = db.Column(db.String(100)) # AMZON S3 --> https://applicationurl/cover/1.jpg
    cover2 = db.Column(db.String(100))
    cover3 = db.Column(db.String(100))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    description = db.Column(db.String(300))
    create_date = db.Column(db.DateTime)
    update_date = db.Column(db.DateTime)
    status = db.Column(db.String(20))
    ISBN_10 = db.Column(db.String(100))
    ISBN_13 = db.Column(db.String(100))
    notes = db.Column(db.String(300))

class OrderItems(db.Model):
    __tablename__ = 'orderitems'
    belong_order = db.Column(db.String(100), db.ForeignKey('order.order_id'), primary_key=True)
    item_id = db.Column(db.String(100), db.ForeignKey('book.book_id_local'), primary_key=True)
    item_type_id = db.Column(db.Integer, db.ForeignKey('itemtype.item_type_id'))
    quantity = db.Column(db.Integer)
    single_price = db.Column(db.Float)
    total_price = db.Column(db.Float)