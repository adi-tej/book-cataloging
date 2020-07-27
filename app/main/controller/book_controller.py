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
book_array_model = BookDto.book_array_model

@api.route('/')
class Books(Resource):
    @api.doc(description="get all books accoring to parameters'")
    @api.response(200, 'success', model=book_array_model)
    @api.response(404, 'not found')
    @api.response(401, 'unauthorized')
    @api.param('isbn', description="take isbn in the parameter if you have")
    @api.param('title', description="take title in the parameter if you have")
    @token_required
    def get(self):
        params = request.args
        token = request.headers.get('token')
        book_list = get_book_by_params(params, token)
        book_array = {
            'books': book_list,
        }
        if book_list:
            return marshal(book_array, book_array_model), GET_SUCCESS
        else:
            api.abort(404, 'nothing found')

@api.route('/autodescription/<isbn>/')
class AutoDescription(Resource):
    @api.doc(description="book autodescription")
    @api.param('isbn', description="take isbn in the parameter if you have")
    @api.response(200, 'success', book_model)
    @api.response(404, 'not found')
    @api.response(401, 'unauthorized')
    @token_required
    def get(self, isbn):
        book = retrive_book(isbn)
        return marshal(book, book_model), GET_SUCCESS

@api.route('/confirm/')
class BookConfirmation(Resource):
    @api.doc(description="confirm book information from user")
    @api.expect(isbn_model)
    @api.response(201, 'success', book_model)
    @api.response(404, 'not found')
    @api.response(401, 'unauthorized')
    def post(self):
        # data = json.loads(request.get_data())
        data = request.form
        images = request.files
        book = confirm_book(data, images)
        return marshal(book, book_model), POST_SUCCESS

@api.route('/<string:book_id>/')
@api.param('book_id', 'book_id is required parameter if lookup books by id')
class BookActivities(Resource):
    # this function is used to correct and update the information with the info returned by staff, you can add more images too.
    @api.doc(description="updating the database and ebay with updated book data by the staff ")
    @api.response(201, 'success', model=book_model)
    @api.response(404, 'not found')
    @api.response(401, 'unauthorized')
    @token_required
    def put(self, book_id):
        # data = json.load(request.get_data())
        data = request.form
        images = request.files
        book = update_book(data, images, book_id)
        if book:
            return marshal(book, book_model), POST_SUCCESS
        else:
            api.abort(404, 'not found, book id not exist')

    @api.doc(description="retrive some book by book id")
    @api.response(200, 'success', model=book_model)
    @api.response(404, 'not found')
    @api.response(401, 'unauthorized')
    @token_required
    def get(self, book_id):
        book = get_book(book_id)
        if book:
            return marshal(book, book_model), GET_SUCCESS
        else:
            api.abort(404, 'not found, book id not exist')

    @api.doc(description="delete some book by book id")
    @api.response(200, 'success', model=book_model)
    @api.response(404, 'not found')
    @api.response(401, 'unauthorized')
    @token_required
    def delete(self, book_id):
        book = delete_book(book_id)
        if book:
            return marshal(book, book_model), GET_SUCCESS
        else:
            api.abort(404, 'not found, book id not exist')

@api.route('/list/<book_id>/')
class BookList(Resource):
    @api.doc(description="list some books to ebay or unlist books from ebay.")
    @api.response(200, 'success', model=book_model)
    @api.response(404, 'not found')
    @api.response(401, 'unauthorized')
    @api.param('book_id', description="take the book id as the parameter")
    @token_required
    def get(self):
        data = json.loads(request.get_data())
        book = list_book(data)
        if book:
            return marshal(book, book_model), GET_SUCCESS
        else:
            api.abort(404, 'not found, book id not exist')

@api.route('/unlist/<book_id>/')
class BookUnlist(Resource):
    @api.doc(description="unlist some books to ebay or unlist books from ebay.")
    @api.response(200, 'success', model=book_model)
    @api.response(404, 'not found')
    @api.response(401, 'unauthorized')
    @api.param('book_id', description="take the book id as the parameter")
    @token_required
    def get(self, book_id):
        book = unlist_book(book_id)
        if book:
            return marshal(book, book_model), GET_SUCCESS
        else:
            api.abort(404, 'not found, book id not exist')
