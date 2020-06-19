from flask import Blueprint
from flask_restplus import Api, Resource

from app import opshop_api
from http_status import *

order = Blueprint('order_api', __name__)

@order.route('/')
class Oder(Resource):
    def get(self):
        pass

@order.route('/creation/')
class OrderCreation(Resource):
    def post(self):
        pass

@order.route('/confirmation/')
class OrderConfirmation(Resource):
    def post(self):
        pass

@order.route('/cancellation/')
class OrderCancellation(Resource):
    def post(self):
        pass

