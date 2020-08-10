from flask import request
from flask_restplus import Resource, marshal
import json

from app.main.service.order_service import *
from ..util.dto import OrderDto
from ..util.decorator import token_required

api = OrderDto.api
order_items_model = OrderDto.order_model
order_items_array_model = OrderDto.order_array_model
new_order_model = OrderDto.new_order_model

@api.route('')
class Order(Resource):
    @api.doc(description="retrive orders according to order status (not required)")
    @api.param('order_status', 'take the order status in the parameter')
    @api.response(200, 'success', order_items_array_model)
    @api.response(404, 'not found')
    @api.response(401, 'unauthorized')
    @token_required
    def get(self):
        order_status = request.args.get('order_status')
        token = request.headers.get('Authorization')

        order_items_array = retrive_order(order_status, token)

        if order_items_array['order_items']:
            return marshal(order_items_array, order_items_array_model), GET_SUCCESS
        else:
            api.abort(404, 'order not found')

@api.route('/<string:order_id>')
@api.param('order_id', description='retrive orders according to order_id (required parameter)')
class OrderList(Resource):
    @api.doc(description="retrive order information")
    @api.response(200, 'success', model=order_items_model)
    @api.response(404, 'not found')
    @api.response(401, 'unauthorized')
    @token_required
    def get(self, order_id):
        order_items = get_order(order_id)
        if order_items['order_id']:
            return marshal(order_items, order_items_model), GET_SUCCESS
        else:
            api.abort(404, 'orders not found')

    @api.doc(description="update order information")
    @api.expect(order_items_model, validate=True)
    @api.response(201, 'success', model=order_items_model)
    @api.response(404, 'not found')
    @api.response(401, 'unauthorized')
    @token_required
    def put(self, order_id):
        data = json.loads(request.get_data())
        order_items = update_order(data, order_id)
        if order_items['order_id']:
            return marshal(order_items, order_items_model), POST_SUCCESS
        else:
            api.abort(404, 'orders not found')

    @api.doc(description="delete some order information")
    @api.response(200, 'success', order_items_model)
    @api.response(404, 'not found')
    @api.response(401, 'unauthorized')
    @token_required
    def delete(self, order_id):
        order_items = delete_order(str(order_id))
        if order_items['order_id']:
            return marshal(order_items, order_items_model), GET_SUCCESS
        else:
            api.abort(404, 'orders not found')

@api.route('/checkout')
class OrderCheckout(Resource):
    @api.doc(description="order from the in shop customer")
    @api.expect(new_order_model, validate=True)
    @api.response(201, 'success', model=order_items_model)
    @api.response(401, 'unauthorized')
    @token_required
    def post(self):
        token = request.headers.get('token')
        data = json.loads(request.get_data())
        order_items = create_order(data, token)
        return marshal(order_items, order_items_model), POST_SUCCESS

@api.route('/ebayorders')
class EbayOrders(Resource):
    @api.doc(description="get all orders from ebay")
    @api.response(200, 'success', model=order_items_array_model)
    @api.response(404, 'not found')
    @api.response(401, 'unauthorized')
    @token_required
    def get(self):
        order_items_array = retrive_order_ebay()

        if order_items_array['order_items']:
            return marshal(order_items_array, order_items_array_model), GET_SUCCESS
        else:
            api.abort(404, 'order not found')

@api.route('/confirmation')
class OrderConfirmation(Resource):
    @api.doc(description="confirm the orders from ebay")
    @api.expect(order_items_model, validate=True)
    @api.response(201, 'success', model=order_items_model)
    @api.response(401, 'unauthorized')
    @api.response(404, 'not found')
    @token_required
    def post(self):
        data = json.loads(request.get_data())
        order_items = confirm_order(data)

        if order_items['order_id']:
            return marshal(order_array, order_array_model), POST_SUCCESS
        else:
            api.abort(404, 'orders not found')

@api.route('/cancellation')
class OrderCancellation(Resource):
    @api.doc(description="cancel the orders from ebay")
    @api.expect(order_items_model, validate=True)
    @api.response(201, 'success', model=order_items_model)
    @api.response(401, 'unauthorized')
    @api.response(404, 'not found')
    @token_required
    def post(self):
        data = json.loads(request.get_data())
        order_items = cancel_order(data)

        if order_items['order_id']:
            return marshal(order_array, order_array_model), POST_SUCCESS
        else:
            if order_items['message'] == "failed":
                api.abort(401, 'have no eligibility to cancel')
            elif order_items['message'] == "not found":
                api.abort(404, 'orders not found')
