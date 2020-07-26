from flask import request
from flask_restplus import Resource, marshal
import json

from app.main.service.book_service import *
from ..util.dto import BookDto
from ..util.decorator import token_required
from app.main.service.user_service import TOKEN

api = BookDto.api
isbn_model = BookDto.isbn_model
book_model = BookDto.book_model
list_model = BookDto.list_model
unlist_model = BookDto.unlist_model
book_array_model = BookDto.book_array_model

@api.route('/')
class Books(Resource):
    @api.doc(description="get all the books")
    @api.response(200, description='get all books accoring to the parameters', model=book_array_model)
    @api.response(404, description='not found')
    @api.param('isbn', description="take isbn in the parameter if you have")
    @api.param('title', description="take title in the parameter if you have")
    @api.marshal_list_with(book_array_model)
    @token_required
    def get(self):
        params = request.args
        token = header_data['token']
        book_list = get_book_by_params(params, token)
        if book_list:
            return book_list
        else:
            api.abort(404)

    @api.doc(description="receive book information from scanning")
    @api.expect(isbn_model)
    @api.response(201, 'book auto description success', book_model)
    @api.response(404, 'not found')
    @token_required
    def post(self):
        data = json.loads(request.get_data())
        book = retrive_book(data)
        return marshal(book, book_model), POST_SUCCESS

@api.route('/confirm/')
class BookConfirmation(Resource):
    def post(self):
        data = json.loads(request.get_data())
        book = confirm_book(data)
        return marshal(book, book_model), POST_SUCCESS

@api.route('/<string:book_id>/')
@api.param('book_id', 'book_id is required parameter if lookup books by id')
class BookActivities(Resource):
    # this function is used to correct and update the information with the info returned by staff, you can add more images too.
    @api.doc(description="updating the database and ebay with updated book data by the staff ")
    @api.response(200, 'update book success', model=book_model)
    @api.response(404, 'not found')
    @api.marshal_with(book_model)
    @token_required
    def put(self, book_id):
        data = json.load(request.get_data())
        book = update_book(data, book_id)
        if book:
            return book
        else:
            api.abort(404)

    @api.doc(description="retrive some book by book id")
    @api.response(200, 'book information', model=book_model)
    @api.response(404, 'not found')
    @api.marshal_with(book_model)
    @token_required
    def get(self, book_id):
        book = get_book(book_id)
        if book:
            return book
        else:
            api.abort(404)

    @api.doc(description="delete some book by book id")
    @api.response(200, 'book deletion success', model=book_model)
    @api.response(404, 'book not found')
    @api.marshal_with(book_model)
    @token_required
    def delete(self, book_id):
        book = delete_book(book_id)
        if book:
            return book
        else:
            api.abort(404)

@api.route('/list/')
class BookList(Resource):
    @api.doc(description="list some books to ebay or unlist books from ebay.")
    @api.expect(book_model)
    @api.response(201, 'book list success', model=book_model)
    @api.response(400, 'book list failed')
    @api.marshal_with(book_model)
    @token_required
    def post(self):
        data = json.loads(request.get_data())
        book = list_book(data)
        if book:
            return book
        else:
            api.abort(404)

@api.route('/unlist/')
class BookUnlist(Resource):
    @api.doc(description="unlist some books to ebay or unlist books from ebay.")
    @api.expect(unlist_model)
    @api.response(201, 'book unlist success', model=book_model)
    @api.response(400, 'book unlist failed')
    @api.marshal_with(book_model)
    @token_required
    def post(self):
        data = json.loads(request.get_data())
        book = unlist_book(data)
        if book:
            return book
        else:
            api.abort(404)
