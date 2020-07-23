from flask_restplus import Namespace, fields

class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'user_id':fields.Integer,
        'opshop_id':fields.Integer,
        'role_id':fields.Integer,
        'register_email':fields.String,
        'user_name':fields.String,
        'password':fields.String
    })

class AuthDto:
    api = Namespace('auth', description='user authentication operations')
    user_auth = api.model('auth_info',{
        'email': fields.String,
        'password': fields.String
    })

class OrderDto:
    api = Namespace('order', description='order management operations')
    new_order_items = api.model('new_order_items', {
        'opshop_id':fields.Integer,
        'book_id':fields.List(fields.String),
        'quantity':fields.List(fields.Integer),
        'total_price':fields.List(fields.Float),
        'item_status':fields.List(fields.String)
    })

    confirmation_order_model = api.model('comfirm_order', {
        'opshop_id': fields.Integer,
        'status': fields.String,
    })

class BookDto:
    api = Namespace('book', description='book related operations')
    isbn_model = api.model('ISBN_10', {'ISBN': fields.Integer})

    book_model = api.model('Book', {
        'opshop_id': fields.Integer,
        'title': fields.String,
        'author': fields.String,
        'publisher': fields.String,
        'publish_date': fields.Date,
        'edition': fields.Integer,
        'pages_number': fields.Integer,
        'genre': fields.String,
        'cover': fields.String,
        'quantity': fields.Integer,
        'description': fields.String,
        'ISBN_10': fields.String,
        'ISBN_13': fields.String,
        'notes': fields.String,
        'condition_id': fields.Integer
    })

    list_model = api.model('Book list', {
        'book_id': fields.String,
        'purpose': fields.String
    })