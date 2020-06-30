from flask import Blueprint, request, jsonify, make_response
from flask_restplus import Api, Resource, fields
from ebaysdk.trading import Connection

from app import opshop_api, db
from models import *

import json

# Receive notifications from eBay and make the right response

notification = Blueprint('notification_api', __name__)

notification_api = opshop_api.namespace(
    'notification',
    description="notifications management process"
)

