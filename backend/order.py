from flask import Blueprint, request, jsonify, make_response
from flask_restplus import Api, Resource, fields
from datetime import datetime
from uuid import uuid5, NAMESPACE_URL

from app import opshop_api, db
from models import Order, OrderItems
from auth import token_required
from http_status import *

import json

order = Blueprint('order_api', __name__)

order_api = opshop_api.namespace(
    'order',
    description="order management process"
)

order_model = order_api.model('Order', {
    'opshop_id': fields.Integer,
    'customer_address': fields.String,
    'order_status': fields.String,
    'book_id': fields.List,
    'item_type_id': fields.List,
    'quantity': fields.Integer,
    'single_price': fields.Float,
    'total_price': fields.Float
})

# display some oders information to user
@order.route('/')
class Order(Resource):
    def get(self):
        pass

    @order_api.doc(description="order from the in shop customer")
    @order_api.expect(order_model)
    @token_required
    def post(self):
        data = json.loads(request.get_data())
        order = Order(
            order_id=uuid5(NAMESPACE_URL, 'v5_app'),
            opshop_id=data['opshop_id'],
            customer_address=data['customer_address'],
            order_date=datetime.now(),
            order_status='confirmed'
        )
        db.session.add(order)

        for item_id in data['bood_id']:
            order_item = OrderItems(
                order_id=order.order_id,
                item_id=item_id,
                item_type_id=data['item_type_id'],
                quantity=data['quantity'],
                single_price=data['single_price'],
                total_price=data['total_price']
            )
            db.session.add(order_item)
        db.session.commit()

        return make_response(jsonify({'order_status':'success', 'status':POST_SUCCESS}))


    def put(self):
        pass


# This is for in-shop customers, frontend send barcode or OCR to
# backend, backend firstly return the book information to frontend
# then frontend send confirm order to backend, backend should remove
# the related items from e-bay and update database
@order.route('/creation/')
class OrderCreation(Resource):
    def post(self):
        pass

# This confirmation is for e-bay order, after receiving order notification
# from e-bay, backend will pass this order information to frontend....
@order.route('/confirmation/')
class OrderConfirmation(Resource):
    def post(self):
        pass

# If users decide cancel some oders, frontend should send order id to backend
# and backend will find e-bay to cancell the order
@order.route('/cancellation/')
class OrderCancellation(Resource):
    def post(self):
        pass

