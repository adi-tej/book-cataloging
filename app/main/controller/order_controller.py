from flask import request
from flask_restplus import Resource, marshal
import json

from app.main.service.order_service import *
from ..util.dto import OrderDto
from ..util.decorator import token_required

api = OrderDto.api
order_model = OrderDto.order_model
order_array_model = OrderDto.order_array_model
new_order_model = OrderDto.new_order_model
comfirmation_order_model = OrderDto.confirmation_order_model

@api.route('/')
class Order(Resource):
    @api.doc(description="retrive orders according to order status (not required)")
    @api.param('order_status', 'take the order status in the parameter')
    @api.response(200, 'order retrive success')
    @api.response(404, 'not found')
    @api.marshal_list_with(order_array_model)
    @token_required
    def get(self):
        order_status = request.args.get('order_status')
        token = header_data['token']

        order_list = retrive_order(order_status, token)

        if order_list:
            return order_list
        else:
            api.abort(404)

@api.route('/<string:order_id>/')
@api.param('order_id', description='retrive orders according to order_id (required parameter)')
class OrderList(Resource):
    @api.doc(description="retrive order information")
    @api.response(200, 'order information')
    @api.response(404, 'order not found')
    @api.marshal_with(order_model)
    @token_required
    def get(self, order_id):
        order = get_order(order_id)
        if order:
            return order
        else:
            api.abort(404)

    @api.doc(description="update order information")
    @api.response(201, 'order updation success')
    @api.response(404, 'order not found')
    @token_required
    def put(self, order_id):
        data = json.loads(request.get_data())
        order = update_order(data, order_id)
        if order:
            return marshal(order, order_model), POST_SUCCESS
        else:
            api.abort(404)

    @api.doc(description="delete some order information")
    @api.response(200, 'order deletion success')
    @api.response(404, 'order not found')
    @api.marshal_with(order_model)
    @token_required
    def delete(self, order_id):
        order = delete_order(order_id)
        if order:
            return order
        else:
            api.abort(404)

@api.route('/checkout/')
class OrderCheckout(Resource):
    @api.doc(description="order from the in shop customer")
    @api.expect(new_order_model, validate=True)
    @api.response(201, 'create order success', model=order_model)
    @api.response(401, 'unauthorized')
    @token_required
    def post(self):
        token = request.headers.get('token')
        data = json.loads(request.get_data())
        order = create_order(data, token)
        return marshal(order, order_model), POST_SUCCESS

@api.route('/confirmation/')
class OrderConfirmation(Resource):
    @api.doc(description="confirm the orders from ebay")
    @api.expect(order_array_model, validate=True)
    @api.response(201, 'order confirmation success', model=order_array_model)
    @api.response(401, 'unauthorized')
    @api.response(404, 'not found')
    @token_required
    def post(self):
        data = json.loads(request.get_data())
        order_list = confirm_order(data)
        order_array = {
            'orders': order_list
        }

        if order_list:
            return marshal(order_array, order_array_model), POST_SUCCESS
        else:
            api.abort(404)

@api.route('/cancellation/')
class OrderCancellation(Resource):
    @api.doc(description="cancel the orders from ebay")
    @api.expect(order_array_model, validate=True)
    @api.response(201, 'order cancellation success', model=order_array_model)
    @api.response(401, 'unauthorized')
    @api.response(404, 'not found')
    @token_required
    def post(self):
        data = json.loads(request.get_data())
        order_list = cancel_order(data)
        order_array = {
            'orders': order_list
        }

        if order_list:
            return marshal(order_array, order_array_model), POST_SUCCESS
        else:
            api.abort(404)
