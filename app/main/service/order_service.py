from flask import jsonify, make_response
from uuid import uuid5, NAMESPACE_URL
from datetime import datetime
from ebaysdk.trading import Connection

from .. import db
from ..http_status import *

def create_order(data):
    if data:
        order = Order(
            order_id=uuid5(NAMESPACE_URL, 'v5_app'),
            opshop_id=data['opshop_id'],
            order_date=datetime.now(),
            order_status='confirmed'
        )
        db.session.add(order)

        for i in range(len(data['book_id'])):
            order_item = OrderItems(
                order_id=order.order_id,
                item_id=data['book_id'][i],
                quantity=data['quantity'][i],
                total_price=data['total_price'][i]
            )
            db.session.add(order_item)

            if data['item_status'][i] == "listed":
                conn = Connection(config_file="ebay_config.yaml", domain="api.sandbox.ebay.com", debug=True)
                request = {
                    "EndingReason":"LostOrBroken",
                    "ItemID":order_item.item_id
                }
                conn.execute("EndItem", request)

        db.session.commit()
        resp = make_response(jsonify({'message':'order creation success'}))
        resp.status_code = POST_SUCCESS

        return resp
    else:
        resp = make_response(jsonify({'message':'bad request'}))
        resp.status_code = BAD_REQUEST
        return resp

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