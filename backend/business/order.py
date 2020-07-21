from flask import Blueprint, request, jsonify, make_response
from flask_restplus import Api, Resource, fields, Namespace
from datetime import datetime
from uuid import uuid5, NAMESPACE_URL
from ebaysdk.trading import Connection
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

order_api = Namespace(
    'order',
    description="order management for opshop as well as orders from ebay"
)

order = Blueprint('order', __name__)
from app import db
from model.models import *
from http_status import *
from authorization.auth import token_required

local_order_model = order_api.model('Order', {
    'opshop_id': fields.Integer,
    'order_status': fields.String,
    'book_id': fields.String,
    'item_type_id': fields.String,
    'quantity': fields.Integer,
    'single_price': fields.Float,
    'total_price': fields.Float,
    'status': fields.String,
})

comfirmation_order_model = order_api.model('comfirm_order', {
    'opshop_id': fields.Integer,
    'status': fields.String,
})

@order_api.route('/local/')
class Order(Resource):
    @order_api.doc(description="order from the in shop customer")
    @order_api.expect(local_order_model)
    @order_api.response(201, 'create order success')
    @order_api.response(401, 'unauthorized')
    @order_api.response(400, 'bad request')
    @token_required
    def post(self):
        data = json.loads(request.get_data())
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
        else:
            resp = make_response()
            resp.status_code = BAD_REQUEST
            resp.headers['message'] = 'bad request'
            return resp

@order_api.route('/orderlist/<string:order_id>')
@order_api.param('order_id')
class OrderList(Resource):
    @order_api.doc(description="retrive order information")
    @order_api.expect(comfirmation_order_model)
    @order_api.response(201, 'order confirmed success')
    @token_required
    def post(self, order_id):
        data = json.loads(request.get_data())
        order = Order.query.filter_by(order_id=order_id).first()
        if data['status'] == "comfirmed":
            order.status = "comfirmed"
        elif data['status'] == "cancelled":
            order.status = "cancelled"

        db.session.add(order)
        db.session.commit()

        resp = make_response()
        resp.status_code = POST_SUCCESS
        resp.headers['message'] = 'order ' + order.status + ' success'
        return resp

    @order_api.doc(description="retrive order information")
    @token_required
    @order_api.response(200, 'order information')
    @order_api.response(404, 'order not found')
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
    @order_api.response(200, 'order updation success')
    @order_api.response(404, 'order not found')
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
    @order_api.response(200, 'order deletion success')
    @order_api.response(404, 'order not found')
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
