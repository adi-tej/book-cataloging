from uuid import uuid1
from ebaysdk.trading import Connection
from ..model.models import *
from app.main.config import EbayConfig
from time import time, localtime, strftime
# from flask import _request_ctx_stack
#
#
# def get_session():
#     ctx = _request_ctx_stack.top
#     if ctx is not None:
#         return ctx.session
#

def create_order(data, user):
    """
        When there are new orders from opshop or ebay, this function
        will help to create new orders at the backend the add them
        to database, finally return the order information to user
    """
    # db.session.rollback()
    # db.session.flush()
    order = Order(
        id=str(uuid1()),
        opshop_id=user['opshop_id'],
        status=OrderStatus.CONFIRMED
    )
    db.session.add(order)
    db.session.commit()

    response = {
        'order_id': order.id,
        'status': order.status,
        'items': []
    }

    items = data['items']

    for item in items:

        book = Book.query.filter_by(id=item['item_id']).first()
        order_item = OrderItem(
            order_id=order.id,
            item_id=item['item_id'],
            quantity=item['quantity']
        )
        db.session.add(order_item)
        # Book.query.filter(item['item_id']).update({'status': ItemStatus.SOLD_INSHOP}, synchronize_session=False)
        # item_obj.status = ItemStatus.SOLD_INSHOP
        # db.session.add(item_obj)
        isbn = book.ISBN_10 if book.ISBN_10 else book.ISBN_13
        response['items'].append({
            'item_id': book.id,
            'title': book.title,
            'isbn': isbn,
            'cover': book.cover,
            'quantity': item['quantity'],
            'price': book.price
        })

        conn = Connection(config_file=EbayConfig.config_file, domain=EbayConfig.domain, debug=EbayConfig.debug)
        request = {
            "EndingReason": "LostOrBroken",
            "ItemID": book.book_id_ebay
        }
        conn.execute("EndItem", request)

    db.session.commit()
    return response


def get_order(order_id):
    """ retrive order by its id """

    order = Order.query.filter_by(id=order_id).first()
    order_items = {
        'order_id': order.id,
        'order_status': order.status,
        'items': []
    }
    order_items_list = OrderItem.query.filter_by(id=order_id).all()
    for item in order_items_list:
        order_items['items'].append({
            'item_id': item.item_id,
            'quantity': item.quantity,
            'total_price': item.total_price
        })
    return order_items


def retrieve_order(status, user):
    """ retrive orders by order status """

    response = {
        'orders': [],
    }
    retrieve_order_ebay()
    d = {'opshop_id': user['opshop_id']}
    if status:
        d['status'] = status
    order_list = Order.query.filter_by(**d).all()

    for order in order_list:
        order_obj = {
            'order_id': order.id,
            'status': order.status,
            'items': []
        }
        item_list = OrderItem.query.filter_by(order_id=order.id).all()
        for item in item_list:
            book = Book.query.filter_by(id=item.item_id).first()
            isbn = book.ISBN_10 if book.ISBN_10 else book.ISBN_13
            order_obj['items'].append({
                'item_id': item.item_id,
                'title': book.title,
                'isbn': isbn,
                'cover': book.cover,
                'quantity': item.quantity,
                'price': book.price,
                'total_price': item.total_price
            })
        response['orders'].append(order_obj)

    return response


def confirm_order(data):
    """ confirm order from ebay """

    order = Order.query.filter_by(id=data['order_id']).first()
    if order:
        # order_items = OrderItem.query.filter_by(order_id=order.id).all()
        # for order_item in order.orderitems:
        #     order_item.item.status = ItemStatus.SOLD_ONLINE

        order.status = OrderStatus.CONFIRMED
        db.session.commit()
        return data
    else:
        fake_data = {
            'order_id': order.id,
        }
        return fake_data


def retrieve_order_ebay():
    """ periodically retrive new orders from ebay """
    try:
        ebay_conn = Connection(config_file=EbayConfig.config_file, domain=EbayConfig.domain, debug=EbayConfig.debug)
        past_time = time() - 10 * 60 * 60 - 5 * 60
        past_time = strftime('%Y-%m-%d %H:%M:%S', localtime(past_time))
        cur_time = time() - 10 * 60 * 60
        cur_time = strftime('%Y-%m-%d %H:%M:%S', localtime(cur_time))
        request_info = {
            "CreateTimeFrom": past_time,
            "CreateTimeTo": cur_time,
            "IncludeFinalValueFee": True,
            "OrderRole": "Seller",
            "OrderStatus": OrderStatus.COMPLETED
        }

        resp = ebay_conn.execute("GetOrders", request_info)

        # order_items_array = {
        #     'order_items': [],
        # }

        if resp.dict()['ReturnedOrderCountActual'] != 0:
            all_orders = resp.dict()['OrderArray']['Order']

            for ebay_order in all_orders:
                order = Order()
                order.id = ebay_order['OrderID']
                order.customer_address = ebay_order['ShippingAddress']['CityName'] + " " \
                                         + ebay_order['ShippingAddress']['Street1'] + " " \
                                         + ebay_order['ShippingAddress']['PostalCode']
                order.customer_name = ebay_order['ShippingAddress']['Name']
                order.customer_contact = ebay_order['TranscationArray']['Transaction']['Buyer']['Email']
                seller_email = ebay_order['SellerEmail']
                order.date = ebay_order['TranscationArray']['Transaction']['CreateDate']
                order.status = OrderStatus.PENDING

                # order_items = {
                #     'order_id': order.id,
                #     'order_status': order.status,
                #     'items': []
                # }

                order_item_list = []
                # for one order, there may be many items, they are put into transactions(array)
                for transaction in ebay_order['TranscationArray']['Transaction']:
                    item_id = transaction['Item']['ItemID']
                    cur_item = Book.query.filter_by(book_id_ebay=item_id).first()
                    orderitem = OrderItem()
                    orderitem.order_id = order.id
                    orderitem.item_id = cur_item.id
                    orderitem.quantity = transaction['QuantityPurchased']
                    orderitem.total_price = transaction['TransactionPrice']['value']
                    orderitem.single_price = transaction['TransactionPrice']['value'] / \
                                             transaction['QuantityPurchased']
                    order_item_list.append(orderitem)

                    # order_items['items'].append({
                    #     'item_id': orderitem.item_id,
                    #     'quantity': orderitem.quantity,
                    #     'total_price': orderitem.total_price
                    # })

                db.session.add(order)
                db.session.add_all(order_item_list)
                db.session.commit()

                # order_items_array['order_items'].append(order_items)
    except Exception:
        pass
    # return order_items_array

#
# def update_order(data, order_id):
#     """ update order information by id """
#
#     order = Order.query.filter_by(id=order_id).first()
#     data['order_id'] = order.id
#     if data:
#         if data['order_status'] == "pending":
#             order.status = OrderStatus.PENDING
#         elif data['order_status'] == "confirmed":
#             order.status = OrderStatus.CONFIRMED
#         elif data['order_status'] == "deleted":
#             order.status = OrderStatus.DELETED
#
#         db.session.commit()
#     return data
#
# def delete_order(order_id):
#     """ delete order by id """
#
#     order = Order.query.filter_by(id=order_id).first()
#     order.status = OrderStatus.DELETED
#     order_items = {
#         'order_id': order.id,
#         'order_status': order.status,
#         'items': []
#     }
#     order_items_list = OrderItem.query.filter_by(id=order_id).all()
#     for item in order_items_list:
#         order_items['items'].append({
#             'item_id': item.item_id,
#             'quantity': item.quantity,
#             'total_price': item.total_price
#         })
#
#     db.session.commit()
#     return order_items

#
# def cancel_order_ebay(order_id):
#     """ seller initially cancel the order from ebay """
#
#     url_1 = "https://api.sandbox.ebay.com/post-order/v2/cancellation/check_eligibility"
#     payload = {
#         "legacyOrderId": order_id,
#     }
#
#     headers = {
#         "Authorization": "AgAAAA**AQAAAA**aAAAAA**MIT1Xg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFk4aiC5WHogidj6x9nY+seQ**Ik0FAA**AAMAAA**Lm7FJsJKP/K5EffRdvx2QkLncSwRUXOcP1FZ+hgML466n1okjDBA1EyFa5wtHtBj1Oj3HThyw7qiPgzRmZTCqDaxzrOM9nzZHe2bDVj0Q3T2O+Cr73t7pn+UnoGTwWfQ1PqBizXT1hPGJlq3nfCiwKk9mG7vU1CPfnWbbe6cSwu6d/LvWs2dpvs7/tTydcZfhSvhGxmJ0avs7B2FLtyOyjycW/e3BKdW7ALJAQHzpJS+KIoGjrqmWkwWO0Zgez5A1jLZjJ74SMzcbuKMUDaNRufcWbUOVmaHqllo8FI9fssydiY43sX3nUW/JJksstgr92Ytqpjbcf1JnirdZz8XEeI70gxCc58vdSvgLxlL2avC3d4BimIN71X6iG0gaa/Le35i/YopsgWBWWx7J99JcLd6FDIVLIdxU6Z/iTAzsIL28Q0/tFGmt7yQxA+lv9uJyFtodcSoxuFJb4DjgIjHAaf70GCkzZMKM2+tZ4FEsPd9datfgAQjp1tC8YTaGmk9dCqnQ6Io9V3Vo50ZnIQU+H7EFYc1lqfwQL2SzYktV9wyqUf/zubzQU97N9mwkQchMjIjoIuAn+PdslO9OwQcy0/RBViBmYqqxn30v/c4m8vPYTYEV7C83sijbDmzujv+Ro+SGxtkohEfGXo7yhH8NIF0+zF23+UL/1pl2T0oYg+aw0jJg5rE6VA0Y+RY0aODnlEv+jH9J+moIQJLrkdON6jAORVrxfCaAriI32E+CJMSyThqHRR71XqE4USgBcFy",
#         "Content-Type": "application/json",
#         "X-EBAY-C-MARKETPLACE-ID": "EBAY_AU",
#         "Accept": "application/json"
#     }
#
#     resp = requests.post(url_1, data=json.dumps(payload), headers=headers)
#
#     cancelled = True
#
#     if resp['eligible']:
#         url_2 = "https://api.sandbox.ebay.com/post-order/v2/cancellation"
#         resp = requests.post(url_2, data=json.dumps(payload), headers=headers)
#         if not resp['cancellations']:
#             cancelled = False
#     else:
#         cancelled = False
#
#     return cancelled
#
#
# def cancel_order(data):
#     """ seller cancel the order from in shop buyers """
#
#     order = Order.query.filter_by(id=data['order_id']).first()
#     if order:
#         if cancel_order_ebay(order.id):
#             order.status = OrderStatus.CANCELLED
#             data['order_status'] = OrderStatus.CANCELLED
#             db.session.commit()
#             return data
#         else:
#             fake_data = {
#                 'order_id': '',
#                 'message': 'failed'
#             }
#     else:
#         fake_data = {
#             'order_id': order.id,
#             'message': 'not found'
#         }
#         return fake_data
#
