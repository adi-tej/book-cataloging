from flask_restplus import Namespace, fields

from app.main.model.models import ItemCondition, ItemStatus, OrderStatus


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'id': fields.Integer,
        'opshop_id': fields.Integer,
        'role_id': fields.Integer,
        'email': fields.String,
        'name': fields.String,
    })


class AuthDto:
    api = Namespace('auth', description='user authentication operations')
    user_auth = api.model('auth_info', {
        'email': fields.String,
        'password': fields.String
    })


class OrderDto:
    api = Namespace('order', description='order management operations')

    item_model = api.model('ordered_item', {
        'item_id': fields.String,
        'title': fields.String,
        'isbn': fields.String,
        'cover': fields.String,
        'quantity': fields.Integer,
        'price': fields.Float,
        'total_price': fields.Float,
    })
    item_checkout = api.model('checkout_item', {
        'item_id': fields.String,
        'quantity': fields.Integer
    })

    order_model = api.model('order', {
        'order_id': fields.String,
        'status': fields.String(enum=[x.value for x in OrderStatus], attribute='status.value'),
        'items': fields.List(fields.Nested(item_model))
    })

    order_array_model = api.model('order_array', {
        'orders': fields.List(fields.Nested(order_model))
    })

    order_checkout_model = api.model('checkout_order_array', {
        'items': fields.List(fields.Nested(item_checkout))
    })
    order_confirm_model = api.model('confirm order', {
        'order_id': fields.String
    })
    new_order_model = api.model('new_order', {
        'items': fields.List(fields.Nested(item_model)),
    })


class BookDto:
    api = Namespace('book', description='book related operations')
    isbn_model = api.model('ISBN_10', {'ISBN': fields.Integer})

    book_response_model = api.model('book', {
        'id': fields.String,
        'title': fields.String(default=''),
        'author': fields.String(default=''),
        'publisher': fields.String(default=''),
        'edition': fields.Integer,
        'page_count': fields.Integer,
        'price': fields.Integer(default=0),
        'genre': fields.String,
        'cover': fields.String,
        'quantity': fields.Integer(default=1),
        'description': fields.String(default=''),
        'status': fields.String(enum=[x.value for x in ItemStatus], attribute='status.value'),
        'isbn': fields.String,
        'notes': fields.String,
        'condition': fields.Integer(enum=[x.value for x in ItemCondition], attribute='condition.value', default=ItemCondition.NEW.value)
    })
    book_model = api.model('book', {
        'id': fields.String,
        'book_id_ebay': fields.String,
        'opshop_id': fields.Integer,
        'title': fields.String,
        'author': fields.String,
        'publisher': fields.String,
        'edition': fields.Integer,
        'page_count': fields.Integer,
        'price': fields.Integer,
        'genre': fields.String,
        'cover': fields.String,
        'price': fields.Float,
        'quantity': fields.Integer,
        'price': fields.Integer,
        'description': fields.String,
        'created_date': fields.DateTime,
        'updated_date': fields.DateTime,
        'status': fields.String(enum=[x.value for x in ItemStatus], attribute='status.value'),
        'ISBN_10': fields.String,
        'ISBN_13': fields.String,
        'notes': fields.String,
        'condition': fields.Integer(enum=[x.value for x in ItemCondition], attribute='condition.value')
    })

    book_array_model = api.model('book_array', {
        'books': fields.List(fields.Nested(book_response_model)),
    })
