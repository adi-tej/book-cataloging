from flask import Blueprint, request, jsonify, make_response
from flask_restplus import Api, Resource, fields
from ebaysdk.trading import Connection
from time import time, strftime, localtime

from app import opshop_api, db
from models import *
from auth import token_required

import json

# Receive notifications from eBay and make the right response

notification = Blueprint('notification_api', __name__)

notification_api = opshop_api.namespace(
    'notification',
    description="notifications management process"
)

@notification.route('/order/')
class Notifications(Resource):
    @notification_api.doc(description="retrive latest order in real time")
    @token_required
    def get(self):
        api = Connection(config_file="ebay.yaml", domain="api.sandbox.ebay.com", debug=True)
        past_time = time() - 10 * 60 * 60 - 1*60
        past_time = strftime('%Y-%m-%d %H:%M:%S', localtime(past_time))
        cur_time = time() - 10 * 60 * 60
        cur_time = strftime('%Y-%m-%d %H:%M:%S', localtime(cur_time))
        request_info = {
            "CreateTimeFrom": past_time,
            "CreateTimeTo": cur_time,
            "IncludeFinalValueFee": True,
            "OrderRole": "Seller",
        }
        # two plans
        resp = api.execute("GetOrders", request_info)
