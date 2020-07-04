from flask import Blueprint, request, jsonify, make_response
from flask_restplus import Api, Resource, fields
from datetime import datetime
from uuid import uuid5, NAMESPACE_URL
from ebaysdk.trading import Connection

from app import opshop_api, db
from models import Order, OrderItems
from auth import token_required
from http_status import *

import json

# ======= order spec =========
# There are two kinds of orders, one is the in shop customer(local) and another is
# online order from eBay. There are some difference between them

# --> local order
# 1. user can create local order (local post)
# 2. user can retrive some order information
# 3. user can update some order information
# 4. user can delete some order information

# --> online order
# 1. user can retrive some order from eBay
# 2. user can confirm some order from eBay
# 3. user can cancel(remove/delete) some order from eBay

# For Order resource, it is only designed for the local order creation
# For OrderList resouce, it is designed for both local and online CRUD

# -- Wei Song

order = Blueprint('order_api', __name__)

order_api = opshop_api.namespace(
    'order',
    description="local order management process"
)

local_order_model = order_api.model('Order', {
    'opshop_id': fields.Integer,
    'order_status': fields.String,
    'book_id': fields.List,
    'item_type_id': fields.List,
    'quantity': fields.Integer,
    'single_price': fields.Float,
    'total_price': fields.Float,
    'status': fields.List
})

@order.route('/local/')
class Order(Resource):
    @order_api.doc(description="order from the in shop customer")
    @order_api.expect(local_order_model)
    @token_required
    def post(self):
        data = json.loads(request.get_data())
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
                item_type_id=data['item_type_id'][i],
                quantity=data['quantity'],
                single_price=data['single_price'],
                total_price=data['total_price']
            )
            db.session.add(order_item)

            if data['status'][i] == "listed":
                conn = Connection(config_file="ebay.yaml", domain="api.sandbox.ebay.com", debug=True)
                request = {
                    "EndingReason":"LostOrBroken",
                    "ItemID":order_item.item_id
                }
                response = conn.execute("EndItem", request)

        db.session.commit()
        resp = make_response()
        resp.status_code = POST_SUCCESS
        resp.headers['message'] = 'order creation success'

        return resp

@order.route('/orderlist/<string:order_id>')
class OrderList():
    # this post method will be used as confirmation from frontend
    @order_api.doc(description="retrive order information")
    @token_required
    def post(self, order_id):
        pass

    @order_api.doc(description="retrive order information")
    @token_required
    def get(self, order_id):
        order = Order.query.filter_by(order_id=order_id).first()
        if not order:
            resp = make_response()
            resp.status_code = NOT_FOUND
            resp.headers['message'] = 'order not found'
            return resp
        else:
            resp = make_response(jsonify(order.__dict__))
            resp.status_code = GET_SUCCESS
            resp.headers['message'] = 'order information'
            return resp

    @order_api.doc(description="update order information")
    @token_required
    def put(self, order_id):
        data = json.loads(request.get_data())
        order = Order.query.filter_by(order_id=order_id).first()
        if not order:
            resp = make_response()
            resp.status_code = NOT_FOUND
            resp.headers['message'] = 'order not found'
            return resp
        else:
            order.__dict__ = data
            resp = make_response(jsonify(order.__dict__))
            db.session.add(order)
            db.session.commit()

            resp.status_code = POST_SUCCESS
            resp.headers['message'] = 'order updation success'
            return resp

    @order_api.doc(description="delete some order information")
    @token_required
    def delete(self, order_id):
        order = Order.query.filter_by(order_id=order_id).first()
        if not order:
            resp = make_response()
            resp.status_code = NOT_FOUND
            resp.headers['message'] = 'order not found'
            return resp
        else:
            resp = make_response(jsonify(order.__dict__))
            db.session.delete(order)
            db.session.commit()
            resp.status_code = GET_SUCCESS
            resp.headers['message'] = 'order deletion success'
            return resp

