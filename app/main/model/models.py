import enum
from .. import db
from sqlalchemy import func, text


class RoleType(enum.Enum):
    ADMIN = 'admin'
    USER = 'user'


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(RoleType), default=RoleType.USER)
    users = db.relationship('User', backref='role', lazy='dynamic')


class Opshop(db.Model):
    __tablename__ = 'opshop'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    staff_count = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), nullable=False, default='active')
    users = db.relationship('User', backref='opshop', lazy='dynamic')
    books = db.relationship('Book', backref='opshop', lazy='dynamic')


class ItemTypeEnum(enum.Enum):
    BOOK = 'book'


class ItemType(db.Model):
    __tablename__ = 'itemtype'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(ItemTypeEnum))
    items = db.relationship('Book', backref='item_type', lazy='dynamic')


class OrderStatus(enum.Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    DELETED = 'deleted'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.String(100), primary_key=True)
    opshop_id = db.Column(db.Integer, db.ForeignKey('opshop.id'), nullable=False)
    customer_address = db.Column(db.String(100))
    customer_name = db.Column(db.String(100))
    customer_contact = db.Column(db.String(100))
    created_date = db.Column(db.DateTime, default=func.now())
    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    orderitems = db.relationship('OrderItem', backref='order', lazy='dynamic')


class ItemStatus(enum.Enum):
    LISTED = 'listed'  # listed on ebay
    INACTIVE = 'inactive'  # remove item
    SOLD_INSHOP = 'sold_inshop'   # in shop checkout
    SOLD_ONLINE = 'sold_online'  # from ebay order confirmed


class ItemCondition(enum.Enum):
    NEW = 1000
    LIKE_NEW = 2750
    USED = 3000
    VERY_GOOD = 4000
    GOOD = 5000
    ACCEPTABLE = 6000


class Book(db.Model):
    __tablename__ = 'book'
    # book_id_ebay should be from eBay
    id = db.Column(db.String(100), primary_key=True)
    book_id_ebay = db.Column(db.String(100))
    opshop_id = db.Column(db.Integer, db.ForeignKey('opshop.id'), nullable=False)
    item_type_id = db.Column(db.Integer, db.ForeignKey('itemtype.id'), nullable=False, default=1)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    publisher = db.Column(db.String(100))
    edition = db.Column(db.Integer, default=0)
    page_count = db.Column(db.Integer, default=0)
    genre = db.Column(db.String(20))
    cover = db.Column(db.String(300))  # AMZON S3 --> https://applicationurl/cover/1.jpg
    price = db.Column(db.Float, default=0.0)
    quantity = db.Column(db.Integer, default=1)
    description = db.Column(db.String(1000), nullable=False)
    created_date = db.Column(db.DateTime, server_default=func.now())
    updated_date = db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    status = db.Column(db.Enum(ItemStatus), default=ItemStatus.INACTIVE, nullable=False)
    ISBN_10 = db.Column(db.String(100))
    ISBN_13 = db.Column(db.String(100))
    notes = db.Column(db.String(300))
    condition = db.Column(db.Enum(ItemCondition), default=ItemCondition.NEW, nullable=False)
    images = db.relationship('Image', backref='item', lazy='dynamic')
    orderitems = db.relationship('OrderItem', backref='item', lazy='dynamic')


class OrderItem(db.Model):
    __tablename__ = 'orderitem'
    order_id = db.Column(db.String(100), db.ForeignKey('order.id'), primary_key=True)
    item_id = db.Column(db.String(100), db.ForeignKey('book.id'), primary_key=True)
    quantity = db.Column(db.Integer, default=1)
    single_price = db.Column(db.Float)
    total_price = db.Column(db.Float)


class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uri = db.Column(db.String(300), nullable=False)
    item_id = db.Column(db.String(100), db.ForeignKey('book.id'), nullable=False)
