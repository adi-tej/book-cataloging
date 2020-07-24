# from .. import db
#
# class OrderItems(db.Model):
#     __tablename__ = 'orderitems'
#     belong_order = db.Column(db.String(100), db.ForeignKey('order.order_id'), primary_key=True)
#     item_id = db.Column(db.String(100), db.ForeignKey('book.book_id_local'), primary_key=True)
#     item_type_id = db.Column(db.Integer, db.ForeignKey('itemtype.item_type_id'))
#     quantity = db.Column(db.Integer)
#     single_price = db.Column(db.Float)
#     total_price = db.Column(db.Float)