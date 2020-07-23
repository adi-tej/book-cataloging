from .. import db

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