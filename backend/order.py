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
        resp.headers['status'] = POST_SUCCESS
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
        resp = make_response()
        if not order:
            resp.headers['status'] = NOT_FOUND
            resp.headers['message'] = 'order not found'
            return resp
        else:
            order_info = json.dumps(order.__dict__)
            resp.headers['status'] = GET_SUCCESS
            resp.headers['message'] = 'order information'
            resp = jsonify(order_info)
            return resp

    @order_api.doc(description="update order information")
    @token_required
    def put(self, order_id):
        data = json.loads(request.get_data())
        order = Order.query.filter_by(order_id=order_id).first()
        resp = make_response()
        if not order:
            resp.headers['status'] = NOT_FOUND
            resp.headers['message'] = 'order not found'
            return resp
        else:
            order.__dict__ = data
            db.session.add(order)
            db.session.commit()

            resp.headers['status'] = GET_SUCCESS
            resp.headers['message'] = 'order updation success'
            return resp

    @order_api.doc(description="delete some order information")
    @token_required
    def delete(self, order_id):
        order = Order.query.filter_by(order_id=order_id).first()
        resp = make_response()
        if not order:
            resp.headers['status'] = NOT_FOUND
            resp.headers['message'] = 'order not found'
            return resp
        else:
            db.session.delete(order)
            db.session.commit()
            resp.headers['status'] = GET_SUCCESS
            resp.headers['message'] = 'order deletion success'
            return resp

