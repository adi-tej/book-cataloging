from flask import Blueprint
from flask_restplus import Api, Resource

order = Blueprint('order_api', __name__)

orderapi = Api(order)

@orderapi.route('/')
class Oder(Resource):
    def get(self):
        pass

@orderapi.route('/creation/')
class OrderCreation(Resource):
    def post(self):
        pass

@orderapi.route('/confirmation/')
class OrderConfirmation(Resource):
    def post(self):
        pass

@orderapi.route('/cancellation/')
class OrderCancellation(Resource):
    def post(self):
        pass

