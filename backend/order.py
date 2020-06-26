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

order = Blueprint('order_api', __name__)

local_order_api = opshop_api.namespace(
    'local order',
    description="local order management process"
)

online_order_api = opshop_api.namespace(
    'online order',
    description="online order management process"
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

# Local order is for customer in-shop
@order.route('/local/')
class LocalOrder(Resource):
    @local_order_api.doc(description="order from the in shop customer")
    @local_order_api.expect(local_order_model)
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

        return make_response(jsonify({'order_status':'success', 'status':POST_SUCCESS}))

@order.route('/local/<string:order_id>')
class LocalOrderList():
    @local_order_api.doc(description="retrive order information")
    @token_required
    def get(self, order_id):
        order = Order.query.filter_by(order_id=order_id).first()
        if not order:
            return make_response(jsonify({'error':'invalid order', 'status':NOT_FOUND}))
        else:
            order_info = json.dumps(order.__dict__)
            return make_response(jsonify({'order':order_info, 'status':GET_SUCCESS}))

    @local_order_api.doc(description="update order information")
    @token_required
    def put(self, order_id):
        data = json.loads(request.get_data())
        order = Order.query.filter_by(order_id=order_id).first()
        if not order:
            return make_response(jsonify({'error':'invalid order', 'status':NOT_FOUND}))
        else:
            order.__dict__ = data
            return make_response(jsonify({'update order':'success', 'status':GET_SUCCESS}))

    @local_order_api.doc(description="delete some order information")
    @token_required
    def delete(self, order_id):
        order = Order.query.filter_by(order_id=order_id).first()
        if not order:
            return make_response(jsonify({'error':'invalid order', 'status':NOT_FOUND}))
        else:
            db.session.delete(order)
            db.session.commit()
            return make_response(jsonify({'delete':'success', 'status':GET_SUCCESS}))

# on-line order is order management for eBay order
@Order.route('/online/')
class OrderOnline():
    def post(self):
        pass

@Order.route('/online/<string:order_id>')
class OnlineOrderList():
    def get(self, order_id):
        pass

    def put(self, order_id):
        pass

    def delete(self, order_id):
        pass

@Order.route('/online/notification/')
class OnlineOrderNotifications():
    def post(self):
        pass

