from flask import Blueprint, request, jsonify, make_response
from flask_restplus import Api, Resource, fields
from ebaysdk.trading import Connection
from time import time, strftime, localtime

from app import opshop_api, db
from models import *
from auth import token_required
from http_status import *

import json

# ----- notifications spec ------
# Receive notifications from eBay and make the right response
# For this part, the backend need the frontend to make the request periodically, which is
# required by ebay. My idea is we need to let the frontend make a notification request to
# the backend every 2-3 minutes, if the backend can find the new orders, then it will parse
# them and forward to the frontend, and for now every order --> every item id (not limited
# by the id), but I am still not solved how to use one order for many item ids

# -- Wei Song

notification = Blueprint('notification_api', __name__)

notification_api = opshop_api.namespace(
    'notification',
    description="notifications management process"
)

@notification.route('/messages/<user_id>')
class Notifications(Resource):
    @notification_api.doc(description="retrive latest order in real time")
    @token_required
    def get(self, user_id):
        api = Connection(config_file="ebay.yaml", domain="api.sandbox.ebay.com", debug=True)
        past_time = time() - 10 * 60 * 60 - 1*60
        past_time = strftime('%Y-%m-%d %H:%M:%S', localtime(past_time))
        cur_time = time() - 10 * 60 * 60
        cur_time = strftime('%Y-%m-%d %H:%M:%S', localtime(cur_time))
        request_info = {
            "CreateTimeFrom": past_time,
            "CreateTimeTo": cur_time,
            "IncludeFinalValueFee": True,
            "OrderRole": "Seller",
        }

        resp = api.execute("GetOrders", request_info)

        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            resp = make_response()
            resp.status_code = UNAUTHORIZED
            resp.headers['message'] = 'user not exist'
            return resp

        current_opshop_email = user.opshop.opshop_ebay_email

        # use opshop email to confirm if there is new order for some opshop

        # need to think of multiple simultaneous requests from different opshops

        # counter

        if resp.dict()['ReturnedOrderCountActual'] != 0:
            all_orders = resp.dict()['OrderArray']['Order']
            item_data, order_data = [], []
            counter = 0
            for ebay_order in all_orders:
                order = Order()
                order.order_id = ebay_order['OrderID']
                order.customer_address = ebay_order['ShippingAddress']['CityName'] + " " \
                    + ebay_order['ShippingAddress']['Street1'] + " " \
                    + ebay_order['ShippingAddress']['PostalCode']
                order.customer_name = ebay_order['ShippingAddress']['Name']
                order.customer_contact = ebay_order['TranscationArray']['Transaction']['Buyer']['Email']
                item_id = ebay_order['TranscationArray']['Transaction']['Item']['ItemID']
                seller_email = ebay_order['SellerEmail']
                order.order_date = ebay_order['TranscationArray']['Transaction']['CreateDate']
                order.order_status = 'pending'
                order_data.append(order.__dict__)
                db.session.add(order)
                # discriminate different opshops
                item = Book.query.filter_by(book_id_ebay=item_id).first()
                if item:
                    item_data.append(item.__dict__)
                else:
                    # This case is not possible
                    pass
            db.session.commit()

            resp_payload = {
                'total':counter,
                'order':order_data,
                'items':item_data
            }

            resp = make_response(jsonify(resp_payload))
            resp.status_code = GET_SUCCESS
            resp.headers['message'] = 'orders from ebay'
            resp.headers['number'] = counter
            return resp
        else:
            resp = make_response()
            resp.status_code = GET_SUCCESS
            resp.headers['message'] = 'no orders from ebay'
            resp.headers['number'] = 0
            return resp

