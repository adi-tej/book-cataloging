from flask import jsonify, make_response
from uuid import uuid5, NAMESPACE_URL
from datetime import datetime
from ebaysdk.trading import Connection
import json

from .. import db
from ..http_status import *
from ..model.models import *
from ..model.user import User
from ..util.decorator import TOKEN

def create_order(data, token):
    payload = TOKEN.serializer.loads(token.encode())
    user = User.query.filter_by(user_id=str(payload['user_id'])).first()
    order = Order(
        order_id=str(uuid5(NAMESPACE_URL, 'v5_app')),
        opshop_id=user.opshop.opshop_id,
        order_date=datetime.now(),
        order_status='confirmed'
    )
    db.session.add(order)
    db.session.commit()

    items = data['items']

    for item in items:
        order_item = OrderItems(
            order_id=order.order_id,
            item_id=item['item_id'],
            quantity=1,
            single_price=item['price'],
            total_price=item['price']
        )
        db.session.add(order_item)

        if item['item_status'] == "listed":
            item_obj = Book.query.filter_by(book_id=item['item_id']).first()
            conn = Connection(config_file="ebay_config.yaml", domain="api.sandbox.ebay.com", debug=True)
            request = {
                "EndingReason":"LostOrBroken",
                "ItemID":item_obj.book_id_ebay
            }
            conn.execute("EndItem", request)

    db.session.commit()

    return order

def get_order(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    return order

def update_order(data, order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    if data:
        if data['order_status'] == "pending":
            order.order_status = "pending"
        elif data['order_status'] == "confirmed":
            order.order_status = "pending"
        db.session.commit()
    return order

def delete_order(order_id):
    order = Order.query.filter_by(order_id=order_id).first()

    order.order_status = "deleted"
    db.session.commit()

    return order

def retrive_order(order_status, token):
    payload = TOKEN.serializer.loads(token.encode())
    user = User.query.filter_by(user_id=payload['user_id']).first()
    order_list = []
    if order_status:
        order_list = Order.query.filter_by(order_status=order_status, opshop_id=user.opshop.opshop_id)
    else:
        order_list = Order.query.filter_by(opshop_id=user.opshop.opshop_id)

    return order_list

def confirm_order(data):
    order_list = data['orders']
    confirmed_order_list = []

    for order in order_list:
        old_order = Order.query.filter_by(order_id=order['order_id']).first()
        old_order.order_status = "confirmed"

        confirmed_order_list.append(old_order)
    db.session.commit()

    return  confirmed_order_list

def cancel_order(data):
    order_list = data['orders']
    cancelled_order_list = []

    for order in order_list:
        old_order = Order.query.filter_by(order_id=order['order_id']).first()
        old_order.order_status = "cancelled"

        db.session.add(old_order)
        cancelled_order_list.append(old_order)
    db.session.commit()

    return cancelled_order_list
