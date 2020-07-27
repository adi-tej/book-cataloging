from flask_restplus import Namespace, fields

class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'user_id':fields.Integer,
        'opshop_id':fields.Integer,
        'role_id':fields.Integer,
        'email':fields.String,
        'username':fields.String,
    })

class AuthDto:
    api = Namespace('auth', description='user authentication operations')
    user_auth = api.model('auth_info',{
        'email': fields.String,
        'password': fields.String
    })

class OrderDto:
    api = Namespace('order', description='order management operations')

    order_model = api.model('order', {
        'order_id': fields.String,
        'opshop_id': fields.Integer,
        'order_date': fields.DateTime,
        'order_status': fields.String,
    })

    order_array_model = api.model('order_array', {
        'orders': fields.List(fields.Nested(order_model)),
    })

    ordered_item_model = api.model('ordered_item', {
        'item_id': fields.String,
        'price': fields.Float,
        'item_status': fields.String,
    })

    order_items_model = api.model('order_items', {
        'order_id': fields.String,
        'items': fields.List(fields.Nested(ordered_item_model))
    })

    order_items_array_model = api.model('order_items_array', {
        'order_items': fields.List(fields.Nested(order_items_model))
    })

    new_order_model = api.model('new_order', {
        'items': fields.List(fields.Nested(ordered_item_model)),
    })

    confirmation_order_model = api.model('comfirm_order', {
        'opeartion': fields.String,
        'orders': fields.List(fields.Nested(order_model)),
    })

class BookDto:
    api = Namespace('book', description='book related operations')
    isbn_model = api.model('ISBN_10', {'ISBN': fields.Integer})

    book_model = api.model('book', {
        'book_id_local': fields.String,
        'book_id_ebay': fields.String,
        'opshop_id': fields.Integer,
        'title': fields.String,
        'author': fields.String,
        'publisher': fields.String,
        'edition': fields.Integer,
        'pages_number': fields.Integer,
        'genre': fields.String,
        'cover': fields.String,
        'quantity': fields.Integer,
        'description': fields.String,
        'create_date': fields.DateTime,
        'update_date': fields.DateTime,
        'status' :fields.String,
        'ISBN_10': fields.String,
        'ISBN_13': fields.String,
        'notes': fields.String,
        'condition': fields.Integer
    })

    book_array_model = api.model('book_array', {
        'books': fields.List(fields.Nested(book_model)),
    })
