from flask import jsonify, make_response
from uuid import uuid5, NAMESPACE_URL
from datetime import datetime
from ebaysdk.trading import Connection
import json
import requests

from .. import db
from ..http_status import *
from ..model.models import *
from ..model.user import User
from ..util.decorator import TOKEN
from app.main.config import EbayConfig

def create_order(data, token):
    payload = TOKEN.serializer.loads(token.encode())
    user = User.query.filter_by(id=str(payload['user_id'])).first()
    if user:
        order = Order(
            id=str(uuid5(NAMESPACE_URL, 'v5_app')),
            opshop_id=user.opshop.id,
            date=datetime.now(),
            status='confirmed'
        )
        db.session.add(order)
        db.session.commit()

        order_items = {
            'order_id': order.id,
            'order_status': order.status,
            'items': []
        }

        items = data['items']

        for item in items:
            order_item = OrderItems(
                order_id=order.id,
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
                item_obj = Book.query.filter_by(id=item['item_id']).first()
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
    order = Order.query.filter_by(id=order_id).first()
    order_items = {
        'order_id': order.id,
        'order_status': order.status,
        'items': []
    }
    order_items_list = OrderItems.query.filter_by(id=order_id).all()
    for item in order_items_list:
        order_items['items'].append({
            'item_id': item.item_id,
            'quantity': item.quantity,
            'total_price': item.total_price
        })
    return order_items

def update_order(data, order_id):
    order = Order.query.filter_by(id=order_id).first()
    data['order_id'] = order.id
    if data:
        if data['order_status'] == "pending":
            order.status = "pending"
        elif data['order_status'] == "confirmed":
            order.status = "pending"
        elif data['order_status'] == "deleted":
            order.status = "deleted"

        db.session.commit()
    return data

def delete_order(order_id):
    order = Order.query.filter_by(id=order_id).first()
    order.status = "deleted"
    order_items = {
        'order_id': order.id,
        'order_status': order.status,
        'items': []
    }
    order_items_list = OrderItems.query.filter_by(id=order_id).all()
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
    user = User.query.filter_by(id=payload['user_id']).first()
    if user:
        order_items_array = {
            'order_items':[],
        }
        order_list = []
        if order_status:
            order_list = Order.query.filter_by(status=order_status, opshop_id=user.opshop.id)
        else:
            order_list = Order.query.filter_by(opshop_id=user.opshop.id)

        for order in order_list:
            order_items = {
                'order_id': order.id,
                'order_status': order.status,
                'items': []
            }
            item_list = OrderItems.query.filter_by(order_id=order.id).all()
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
    order = Order.query.filter_by(id=data['order_id']).first()
    if order:
        order.status = "confirmed"
        data['order_status'] = "confirmed"
        db.session.commit()
        return data
    else:
        fake_data = {
            'order_id':order.id,
        }
        return fake_data

def cancel_order_ebay(order_id):
    url_1 = "https://api.sandbox.ebay.com/post-order/v2/cancellation/check_eligibility"
    payload = {
        "legacyOrderId": order_id,
    }

    headers = {
          "Authorization": "AgAAAA**AQAAAA**aAAAAA**MIT1Xg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFk4aiC5WHogidj6x9nY+seQ**Ik0FAA**AAMAAA**Lm7FJsJKP/K5EffRdvx2QkLncSwRUXOcP1FZ+hgML466n1okjDBA1EyFa5wtHtBj1Oj3HThyw7qiPgzRmZTCqDaxzrOM9nzZHe2bDVj0Q3T2O+Cr73t7pn+UnoGTwWfQ1PqBizXT1hPGJlq3nfCiwKk9mG7vU1CPfnWbbe6cSwu6d/LvWs2dpvs7/tTydcZfhSvhGxmJ0avs7B2FLtyOyjycW/e3BKdW7ALJAQHzpJS+KIoGjrqmWkwWO0Zgez5A1jLZjJ74SMzcbuKMUDaNRufcWbUOVmaHqllo8FI9fssydiY43sX3nUW/JJksstgr92Ytqpjbcf1JnirdZz8XEeI70gxCc58vdSvgLxlL2avC3d4BimIN71X6iG0gaa/Le35i/YopsgWBWWx7J99JcLd6FDIVLIdxU6Z/iTAzsIL28Q0/tFGmt7yQxA+lv9uJyFtodcSoxuFJb4DjgIjHAaf70GCkzZMKM2+tZ4FEsPd9datfgAQjp1tC8YTaGmk9dCqnQ6Io9V3Vo50ZnIQU+H7EFYc1lqfwQL2SzYktV9wyqUf/zubzQU97N9mwkQchMjIjoIuAn+PdslO9OwQcy0/RBViBmYqqxn30v/c4m8vPYTYEV7C83sijbDmzujv+Ro+SGxtkohEfGXo7yhH8NIF0+zF23+UL/1pl2T0oYg+aw0jJg5rE6VA0Y+RY0aODnlEv+jH9J+moIQJLrkdON6jAORVrxfCaAriI32E+CJMSyThqHRR71XqE4USgBcFy",
          "Content-Type": "application/json",
          "X-EBAY-C-MARKETPLACE-ID": "EBAY_AU",
          "Accept": "application/json"
    }

    resp = requests.post(url_1, data=json.dumps(payload), headers=headers)

    cancelled = True

    if resp['eligible']:
        url_2 = "https://api.sandbox.ebay.com/post-order/v2/cancellation"
        resp = requests.post(url_2, data=json.dumps(payload), headers=headers)
        if not resp['cancellations']:
            cancelled = False
    else:
        cancelled = False

    return cancelled

def cancel_order(data):
    order = Order.query.filter_by(id=data['order_id']).first()
    if order:
        if cancel_order_ebay(order.id):
            order.status = "cancelled"
            data['order_status'] = "cancelled"
            db.session.commit()
            return data
        else:
            fake_data = {
                'order_id': '',
                'message': 'failed'
            }
    else:
        fake_data = {
            'order_id':order.id,
            'message': 'not found'
        }
        return fake_data

def retrive_order_ebay():
    ebay_conn = Connection(config_file=EbayConfig.config_file, domain=EbayConfig.domain, debug=EbayConfig.debug)
    past_time = time() - 10 * 60 * 60 - 5 * 60
    past_time = strftime('%Y-%m-%d %H:%M:%S', localtime(past_time))
    cur_time = time() - 10 * 60 * 60
    cur_time = strftime('%Y-%m-%d %H:%M:%S', localtime(cur_time))
    request_info = {
        "CreateTimeFrom": past_time,
        "CreateTimeTo": cur_time,
        "IncludeFinalValueFee": True,
        "OrderRole": "Seller",
        "OrderStatus": "Completed"
    }

    resp = ebay_conn.execute("GetOrders", request_info)

    order_items_array = {
        'order_items': [],
    }

    if resp.dict()['ReturnedOrderCountActual'] != 0:
        all_orders = resp.dict()['OrderArray']['Order']

        for ebay_order in all_orders:
            order = Order()
            order.id = ebay_order['OrderID']
            order.customer_address = ebay_order['ShippingAddress']['CityName'] + " " \
                                     + ebay_order['ShippingAddress']['Street1'] + " " \
                                     + ebay_order['ShippingAddress']['PostalCode']
            order.customer_name = ebay_order['ShippingAddress']['Name']
            order.customer_contact = ebay_order['TranscationArray']['Transaction']['Buyer']['Email']
            seller_email = ebay_order['SellerEmail']
            order.date = ebay_order['TranscationArray']['Transaction']['CreateDate']
            order.status = 'pending'

            order_items = {
                'order_id': order.id,
                'order_status': order.status,
                'items': []
            }

            order_item_list = []
            # for one order, there may be many items, they are put into transactions(array)
            for transaction in ebay_order['TranscationArray']['Transaction']:
                item_id = transaction['Item']['ItemID']
                cur_item = Book.query.filter_by(book_id_ebay=item_id).first()
                orderitem = OrderItems()
                orderitem.order_id = order.id
                orderitem.item_id = cur_item.id
                orderitem.quantity = transaction['QuantityPurchased']
                orderitem.total_price = transaction['TransactionPrice']['value']
                orderitem.single_price = transaction['TransactionPrice']['value'] / \
                                         transaction['QuantityPurchased']
                order_item_list.append(orderitem)

                order_items['items'].append({
                    'item_id': orderitem.item_id,
                    'quantity': orderitem.quantity,
                    'total_price': orderitem.total_price
                })

            db.session.add(order)
            db.session.add_all(order_item_list)
            db.session.commit()

            order_items_array['order_items'].append(order_items)

    return order_items_array
