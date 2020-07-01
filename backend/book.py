from flask import request, jsonify, make_response, Blueprint
from flask_restplus import fields, Resource
from uuid import uuid5, NAMESPACE_OID
from datetime import datetime

from auth import token_required
from models import *
from app import db, opshop_api
from http_status import *

import json

books = Blueprint('book_bp', __name__)

books_api = opshop_api.namespace(
    'books',
    description="books management process"
)

books_model = books_api.model('Book', {
    'opshop_id':fields.Integer,
    'title':fields.String,
    'author':fields.String,
    'publisher':fields.String,
    'publish_date':fields.Date,
    'edition':fields.Integer,
    'pages_number':fields.Integer,
    'genre':fields.String,
    # 'cover': Not sure about the cover
    'quantity':fields.Integer,
    'description':fields.String,
    'ISBN_10':fields.String,
    'ISBN_13':fields.String,
    'notes':fields.String
})

@books.route('/')
class Books(Resource):
    @books_api.doc(description="receive book information from scanning")
    @books_api.expect(books_model)
    @token_required
    def post(self):
        data = json.load(request.get_data())
        book = Book()
        data['book_id_local'] = book_id_local=uuid5(NAMESPACE_OID, 'v5app')
        data['book_id_ebay'] = ''
        data['item_type_id'] = 1
        data['create_date'] = datetime.now()
        data['update_date'] = datetime.now()
        data['status'] = 'unlisted'
        book.__dict__ = data

        db.session.add(book)
        db.session.commit()

        resp = make_response()
        resp.status_code = POST_SUCCESS
        resp.headers['message'] = 'add book success'

        return resp

@books.route('/avtivities/<string:book_id>')
class BookActivities(Resource):
    @books_api.doc(description="retrive some book by book id")
    @token_required
    def get(self, book_id):
        book = Book.query.filter_by(book_id_loacl=book_id).first()
        if not book:
            resp = make_response()
            resp.status_code = NOT_FOUND
            resp.headers['message'] = 'book not found'
            return resp
        else:
            book_info = json.dumps(book.__dict__)
            resp = make_response(jsonify(book_info))
            resp.status_code = GET_SUCCESS
            resp.headers['message'] = 'retrive book information'
            return resp

    @books_api.doc(description="update some book by book id")
    @token_required
    def put(self, book_id):
        data = json.loads(request.get_data())
        book = Book.query.filter_by(book_id_loacl=book_id).first()
        if not book:
            resp = make_response()
            resp.status_code = NOT_FOUND
            resp.headers['message'] = 'book not found'
            return resp
        else:
            book.__dict__ = data
            resp = make_response(jsonify(book.__dict__))
            resp.status_code = POST_SUCCESS
            resp.headers['message'] = 'book updation success'
            return resp

    @books_api.doc(description="delete some book by book id")
    @token_required
    def delete(self, book_id):
        book = Book.query.filter_by(book_id_loacl=book_id).first()
        if not book:
            resp = make_response()
            resp.status_code = NOT_FOUND
            resp.headers['message'] = 'book not found'
            return resp
        else:
            resp = make_response(jsonify(book.__dict__))
            resp.status_code = GET_SUCCESS
            resp.headers['message'] = 'book deletion success'
            return resp

@books.route('/list/')
class BookList(Resource):
    def post(self):
        pass