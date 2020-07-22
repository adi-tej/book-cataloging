from flask import Blueprint, request, jsonify, make_response
from flask_restplus import Api, Resource, fields, Namespace
from ebaysdk.trading import Connection
from time import time, strftime, localtime

from app import db
from model.models import *
from authorization.auth import token_required
from http_status import *
import json

# ----- notifications spec ------
# Receive notifications from eBay and make the right response
# For this part, the backend need the frontend to make the request periodically, which is
# required by ebay. My idea is we need to let the frontend make a notification request to
# the backend every 2-3 minutes, if the backend can find the new orders, then it will parse
# them and forward to the frontend, and for now every order --> every item id (not limited
# by the id), but I am still not solved how to use one order for many item ids

# For order cancellation, it should be done by frontend which ebay has provided us the restful
# api POST request, the cancellation process should be:
# 1. backend request new 'Completed' order from ebay, and forward this order to frontend
# 2. if frontend want to cancel, then front need to make a requst:
#       POST https://api.sandbox.ebay.com/post-order/v2/cancellation/check_eligibility
#       the headers:
#           Authorization: TOKEN <OAuth token>
#           Content-Type: application/json
#           X-EBAY-C-MARKETPLACE-ID: EBAY_AU
#           Accept: application/json
#       the payload:
#           {
#               "legacyOrderId": order_id
#           }
# 3. After making this request to ebay, frontend shall receive a response:
# {
#     "eligible": ture/false,
#     "failureReason": [
#         "INVALID_ORDER"
#     ]
# }
# 4. if the order to be cancelled is 'eligible', then make a cancellation request:
#       POST https://api.sandbox.ebay.com/post-order/v2/cancellation
#       the headers:
#           Authorization: TOKEN <OAuth token>
#           Content-Type: application/json
#           X-EBAY-C-MARKETPLACE-ID: EBAY_AU
#           Accept: application/json
#       the payload:
#           {
#               "legacyOrderId": order_id
#           }
# 5. The response if the cancellation is success:
# {
#     "cancellations": [
#         {
#             "cancelId": "5000018282",
#             "marketplaceId": "EBAY_AU",
#             "legacyOrderId": "170007292461-9190794007",
#             "requestorType": "SELLER",
#             "cancelReason": "OUT_OF_STOCK_OR_CANNOT_FULFILL",
#             "cancelState": "CLOSED",
#             "cancelStatus": "CANCEL_CLOSED_WITH_REFUND",
#             "cancelCloseReason": "FULL_REFUNDED",
#             "paymentStatus": "UNKNOWN",
#             "requestRefundAmount": {
#                 "value": 0,
#                 "currency": "AUD"
#             },
#             "cancelRequestDate": {
#                 "value": "2015-05-18T22:42:11.000Z",
#             },
#             "cancelCloseDate": {
#                 "value": "2015-05-18T22:42:11.000Z",
#             }
#         },
#         {
#             "cancelId": "5000020253",
#             "marketplaceId": "EBAY_AU",
#             "legacyOrderId": "170007591793-9351013007",
#             "requestorType": "SELLER",
#             "cancelReason": "OUT_OF_STOCK_OR_CANNOT_FULFILL",
#             "cancelState": "CLOSED",
#             "cancelStatus": "CANCEL_CLOSED_WITH_REFUND",
#             "cancelCloseReason": "FULL_REFUNDED",
#             "paymentStatus": "PAYPAL_PAID",
#             "requestRefundAmount": {
#                 "value": 2.46,
#                 "currency": "AUD"
#             },
#             "cancelRequestDate": {
#                 "value": "2015-06-13T00:32:09.000Z",
#             },
#             "cancelCloseDate": {
#                 "value": "2015-06-13T00:37:06.000Z",
#             }
#         }
#     ],
#     "total": 2,
#     "paginationOutput": {
#         "offset": 1,
#         "limit": 6,
#         "totalPages": 1,
#         "totalEntries": 2
#     }
# }
#
# 6. Finally, frontend need to make a request to the backend to tell
# the frontend has cancelled the order..
# -- Wei Song

notification = Blueprint('notify', __name__)
notification_api = Namespace(
    'notifications',
    description="receive and manage notifications from ebay, like listing, order.."
)

@notification_api.route('/messages/<opshop_id>')
class Notifications(Resource):
    @notification_api.doc(description="retrive latest order in real time")
    @notification_api.param('opshop_id')
    @notification_api.response(200, 'orders from ebay')
    @notification_api.response(404, 'no orders found')
    @token_required
    def get(self, opshop_id):
        api = Connection(config_file="ebay.yaml", domain="api.sandbox.ebay.com", debug=True)
        # get order on ebay created on period: past time point --> current time point
        past_time = time() - 10 * 60 * 60 - 1*60
        past_time = strftime('%Y-%m-%d %H:%M:%S', localtime(past_time))
        cur_time = time() - 10 * 60 * 60
        cur_time = strftime('%Y-%m-%d %H:%M:%S', localtime(cur_time))
        request_info = {
            "CreateTimeFrom": past_time,
            "CreateTimeTo": cur_time,
            "IncludeFinalValueFee": True,
            "OrderRole": "Seller",
            "OrderStatus": "Completed"
        }

        resp = api.execute("GetOrders", request_info)
        opshop = Opshop.query.filter_by(opshop_id=opshop_id).first()
        current_opshop_email = opshop.opshop_ebay_email

        if resp.dict()['ReturnedOrderCountActual'] != 0:
            all_orders = resp.dict()['OrderArray']['Order']
            order_array = []
            counter = 0
            for ebay_order in all_orders:
                item_id_list, order_item_list, item_data = [], [], []
                counter += 1
                order = Order()
                order.order_id = ebay_order['OrderID']
                order.customer_address = ebay_order['ShippingAddress']['CityName'] + " " \
                    + ebay_order['ShippingAddress']['Street1'] + " " \
                    + ebay_order['ShippingAddress']['PostalCode']
                order.customer_name = ebay_order['ShippingAddress']['Name']
                order.customer_contact = ebay_order['TranscationArray']['Transaction']['Buyer']['Email']
                seller_email = ebay_order['SellerEmail']
                order.order_date = ebay_order['TranscationArray']['Transaction']['CreateDate']
                order.order_status = 'pending'

                # for one order, there may be many items, they are put into transactions(array)
                for transaction in ebay_order['TranscationArray']['Transaction']:
                    item_id = transaction['Item']['ItemID']
                    item_id_list.append(item_id)
                    orderitem = OrderItems()
                    orderitem.belong_order = order.order_id
                    orderitem.item_id = item_id
                    orderitem.item_type_id = 1
                    orderitem.quantity = transaction['QuantityPurchased']
                    orderitem.total_price = transaction['TransactionPrice']['value']
                    orderitem.single_price = transaction['TransactionPrice']['value'] / \
                             transaction['QuantityPurchased']
                    order_item_list.append(orderitem)

                order_data.append(order.__dict__)
                db.session.add(order)
                db.session.add_all(order_item_list)

                for item_id in item_id_list:
                    item = Book.query.filter_by(book_id_ebay=item_id).first()
                    if item:
                        item_data.append(item.__dict__)
                order_array.append({'order_id': order.order_id, 'items': item_data})

            if counter != 0:
                db.session.commit()

            resp_payload = {
                'order_number': len(order_array),
                'order_array': order_array
            }

            resp = make_response(jsonify(resp_payload))
            resp.status_code = GET_SUCCESS
            resp.headers['message'] = 'orders from ebay'
            return resp
        else:
            resp = make_response()
            resp.status_code = NOT_FOUND
            resp.headers['message'] = 'no orders from ebay'
            return resp
