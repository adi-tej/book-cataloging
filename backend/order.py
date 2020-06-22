from flask import Blueprint
from flask_restplus import Api, Resource

from app import opshop_api
from http_status import *

order = Blueprint('order_api', __name__)

# display some oders information to user
@order.route('/')
class Oder(Resource):
    def get(self):
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

