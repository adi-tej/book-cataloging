from flask_login import UserMixin

from app import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    opshop_id = db.Column(db.Integer, db.ForeignKey('Opshop.opshop_id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('Role.role_id'), nullable=False)
    register_email = db.Column(db.String(50), unique=True, nullable=False)
    user_name = db.Column(db.String(50), unique=False, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def get_user(self, _user_id):
        return User.query.filter_by(user_id=_user_id).first()

class Role(db.Model):
    __tablename__ = 'role'
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(20))

class Opshop(db.Model):
    __tablename__ = 'opshop'
    opshop_id = db.Column(db.Integer, primary_key=True)
    opshop_name = db.Column(db.String(20), nullable=True)
    opshop_address = db.Column(db.String(100))
    staff_number = db.Column(db.Integer)
    opshop_status = db.Column(db.String(20))

class ItemType(db.Model):
    __tablename__ = 'itemtype'
    item_type_id = db.Column(db.Integer, primary_key=True)
    item_type_name = db.Column(db.String(20))

class Order(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, primary_key=True)
    opshop_id = db.Column(db.Integer, db.ForeignKey('Opshop.opshop_id'), nullable=False)
    customer_address = db.Column(db.String(100))
    order_date = db.Column(db.Date)
    order_status = db.Column(db.String(20))

class OrderItems(db.Model):
    __tablename__ = 'orderitems'
    order_id = db.Column(db.Integer, db.ForeignKey('Order.order_id'), nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)
    item_type_id = db.Column(db.Integer, db.ForeignKey('ItemType.item_type_+id'))
    order_date = db.Column(db.Date)
    order_status = db.Column(db.String(20))

class Book(db.Model):
    __tablename__ = 'book'
    book_id = db.Column(db.String(100), primary_key=True)
    opshop_id = db.Column(db.Integer, db.ForeignKey('Opshop.opshop_id'), nullable=False)
    item_type_id = db.Column(db.Integer, db.ForeignKey('ItemType.item_type_id'), nullable=False)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    publisher = db.Column(db.String(100))
    publish_date = db.Column(db.Date)
    edition = db.Column(db.Integer)
    pages_number = db.Column(db.Integer)
    genre = db.Column(db.String(20))
    cover =db.Column(db.String(100))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    description = db.Column(db.String(100))
    create_date = db.Column(db.Date)
    update_date = db.Column(db.Date)
    status = db.Column(db.String(20))
    ISBN = db.Column(db.String(100))
    notes = db.Column(db.String(100))
