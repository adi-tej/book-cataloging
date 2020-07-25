from flask import request
from flask_restplus import Resource
import json

from app.main.service.order_service import *
from ..util.dto import OrderDto
from ..util.decorator import token_required

api = OrderDto.api
order_items_model = OrderDto.new_order_items
comfirmation_order_model = OrderDto.confirmation_order_model

@api.route('/checkout/')
class Order(Resource):
    @api.doc(description="order from the in shop customer")
    @api.expect(order_items_model, validate=True)
    @api.response(201, 'create order success')
    @api.response(401, 'unauthorized')
    @api.response(400, 'bad request')
    @token_required
    def post(self):
        data = json.loads(request.get_data())
        return create_order(data)

@api.route('/<string:order_id>/')
@api.param('order_id')
class OrderList(Resource):
    @api.doc(description="retrive order information")
    @api.expect(comfirmation_order_model)
    @api.response(201, 'order confirmed success')
    @token_required
    def post(self, order_id):
        data = json.loads(request.get_data())
        return confirm_order(data, order_id)

    @api.doc(description="retrive order information")
    @api.response(200, 'order information')
    @api.response(404, 'order not found')
    @token_required
    def get(self, order_id):
        return get_order(order_id)

    @api.doc(description="update order information")
    @api.response(200, 'order updation success')
    @api.response(404, 'order not found')
    @token_required
    def put(self, order_id):
        data = json.loads(request.get_data())
        return update_order(data, order_id)

    @api.doc(description="delete some order information")
    @api.response(200, 'order deletion success')
    @api.response(404, 'order not found')
    @token_required
    def delete(self, order_id):
        return delete_order(order_id)

@api.route('/retrive/')
class RetriveOrder(Resource):
    @api.doc(description="retrive orders according to order status")
    @api.header('order_status', 'take the order status in the header')
    @api.response(200, 'order retrive success')
    @api.response(404, 'not found')
    @token_required
    def get(self, order_status):
        header_data = request.headers
        token = header_data['token']
        return retrive_order(header_data, token)
