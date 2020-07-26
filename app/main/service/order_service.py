from flask import jsonify, make_response
from uuid import uuid5, NAMESPACE_URL
from datetime import datetime
from ebaysdk.trading import Connection
import json

from .. import db
from ..http_status import *
from ..model.models import *

def create_order(data, token):
    payload = TOKEN.serializer.loads(token.encode())
    user = User.query.filter_by(user_id=payload['user_id']).first()
    order = Order(
        order_id=uuid5(NAMESPACE_URL, 'v5_app'),
        opshop_id=user.opshop.opshop_id,
        order_date=datetime.now(),
        order_status='confirmed'
    )
    db.session.add(order)

    items = data['items']

    for item in items:
        order_item = OrderItems(
            order_id=order.order_id,
            item_id=item.item_id,
            quantity=1,
            single_price=item.price,
            total_price=item.price
        )
        db.session.add(order_item)

        if item.status == "listed":
            item_obj = Book.query.filter_by(book_id=item.item_id).first()
            conn = Connection(config_file="ebay_config.yaml", domain="api.sandbox.ebay.com", debug=True)
            request = {
                "EndingReason":"LostOrBroken",
                "ItemID":item_obj.book_id_ebay
            }
            conn.execute("EndItem", request)

    db.session.commit()

    return order

def confirm_order(data, order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    if data['status'] == "comfirmed":
        order.status = "comfirmed"
    elif data['status'] == "cancelled":
        order.status = "cancelled"

    db.session.add(order)
    db.session.commit()

    resp = make_response(order.__dict__)
    resp.status_code = POST_SUCCESS
    return resp

def get_order(order_id):
    if not order:
        resp = make_response(jsonify({'message':'order not found'}))
        resp.status_code = NOT_FOUND
        return resp
    else:
        resp = make_response(jsonify(order.__dict__))
        resp.status_code = GET_SUCCESS
        return resp

def update_order(data, order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    if not order:
        resp = make_response(jsonify({'message':'order not found'}))
        resp.status_code = NOT_FOUND
        return resp
    else:
        order.__dict__ = data
        resp = make_response(jsonify(order.__dict__))
        db.session.add(order)
        db.session.commit()

        resp.status_code = POST_SUCCESS
        return resp

def delete_order(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    if not order:
        resp = make_response(jsonify({'message':'order not found'}))
        resp.status_code = NOT_FOUND
        return resp
    else:
        resp = make_response(jsonify(order.__dict__))
        db.session.delete(order)
        db.session.commit()
        resp.status_code = GET_SUCCESS
        return resp

def retrive_order(header_data, token):
    payload = TOKEN.serializer.loads(token.encode())
    user = User.query.filter_by(user_id=payload['user_id']).first()
    order_list = []
    if header_data['order_status']:
        order_list = Order.query.filter_by(order_status=header_data['order_status'], opshop_id=user.opshop.opshop_id)
    else:
        order_list = Order.query.filter_by(opshop_id=user.opshop.opshop_id)

    if order_list:
        resp = make_response(jsonify(json.dumps(order_list)))
        resp.status_code = GET_SUCCESS
        return resp
    else:
        resp = make_response(jsonify({'message':'not found'}))
        resp.status_code = NOT_FOUND
        return resp
