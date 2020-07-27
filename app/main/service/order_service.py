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
    if user:
        order = Order(
            order_id=str(uuid5(NAMESPACE_URL, 'v5_app')),
            opshop_id=user.opshop.opshop_id,
            order_date=datetime.now(),
            order_status='confirmed'
        )
        db.session.add(order)
        db.session.commit()

        order_items = {
            'order_id': order.order_id,
            'order_status': order.order_status,
            'items': []
        }

        items = data['items']

        for item in items:
            order_item = OrderItems(
                order_id=order.order_id,
                item_id=item['item_id'],
                quantity=item['quantity'],
                single_price=item['total_price'],
                total_price=item['total_price']
            )
            db.session.add(order_item)

            order_items['items'].append({
                'item_id': order_item.item_id,
                'quantity': order_item.quantity,
                'total_price': order_item.total_price
            })

            try:
                item_obj = Book.query.filter_by(book_id=item['item_id']).first()
                conn = Connection(config_file="../ebay_config.yaml", domain="api.sandbox.ebay.com", debug=True)
                request = {
                    "EndingReason":"LostOrBroken",
                    "ItemID":item_obj.book_id_ebay
                }
                conn.execute("EndItem", request)
            except Exception:
                pass

        db.session.commit()

        return order_items
    else:
        fake_data = {
            'order_id':'',
        }
        return fake_data

def get_order(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    order_items = {
        'order_id': order.order_id,
        'order_status': order.order_status,
        'items': []
    }
    order_items_list = OrderItems.query.filter_by(order_id=order_id).all()
    for item in order_items_list:
        order_items['items'].append({
            'item_id': item.item_id,
            'quantity': item.quantity,
            'total_price': item.total_price
        })
    return order_items

def update_order(data, order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    data['order_id'] = order.order_id
    if data:
        if data['order_status'] == "pending":
            order.order_status = "pending"
        elif data['order_status'] == "confirmed":
            order.order_status = "pending"
        elif data['order_status'] == "deleted":
            order.order_status = "deleted"

        db.session.commit()
    return data

def delete_order(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    order.order_status = "deleted"
    order_items = {
        'order_id': order.order_id,
        'order_status': order.order_status,
        'items': []
    }
    order_items_list = OrderItems.query.filter_by(order_id=order_id).all()
    for item in order_items_list:
        order_items['items'].append({
            'item_id': item.item_id,
            'quantity': item.quantity,
            'total_price': item.total_price
        })

    db.session.commit()
    return order_items


def retrive_order(order_status, token):
    payload = TOKEN.serializer.loads(token.encode())
    user = User.query.filter_by(user_id=payload['user_id']).first()
    if user:
        order_items_array = {
            'order_items':[],
        }
        order_list = []
        if order_status:
            order_list = Order.query.filter_by(order_status=order_status, opshop_id=user.opshop.opshop_id)
        else:
            order_list = Order.query.filter_by(opshop_id=user.opshop.opshop_id)

        for order in order_list:
            order_items = {
                'order_id': order.order_id,
                'order_status': order.order_status,
                'items': []
            }
            item_list = OrderItems.query.filter_by(order_id=order.order_id).all()
            for item in item_list:
                order_items['items'].append({
                    'item_id': item.item_id,
                    'quantity': item.quantity,
                    'total_price': item.total_price
                })
            order_items_array['order_items'].append(order_items)

        return order_items_array
    else:
        fake_data = {
            'order_items':[],
        }
        return fake_data

def confirm_order(data):
    order = Order.query.filter_by(order_id=data['order_id']).first()
    if order:
        order.order_status = "confirmed"
        data['order_status'] = "confirmed"
        db.session.commit()
        return data
    else:
        fake_data = {
            'order_id':order.order_id,
        }
        return fake_data

def cancel_order(data):
    order = Order.query.filter_by(order_id=data['order_id']).first()
    if order:
        order.order_status = "cancelled"
        data['order_status'] = "cancelled"
        db.session.commit()
        return data
    else:
        fake_data = {
            'order_id':order.order_id,
        }
        return fake_data
