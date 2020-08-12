from flask import request
from flask_restplus import Resource, marshal
from app.main.service.book_service import *
from ..util.dto import BookDto
from ..util.decorator import token_required
from ..http_status import *

api = BookDto.api
book_array_model = BookDto.book_array_model
book_response_model = BookDto.book_response_model


@api.route('')
class Books(Resource):
    @api.doc(description="Get all the listed books of the op-shop with optional parameters")
    @api.response(200, 'success', model=book_array_model)
    @api.response(401, 'unauthorized')
    @api.param('isbn', description="ISBN of the book - 10 or 13 digits")
    @api.param('title', description="Title of the book")
    @api.param('search', description="Search query to filter the books")
    @token_required
    def get(self, user):
        params = request.args
        book_list = get_all_books(params, user)
        book_array = {
            'books': book_list
        }
        return marshal(book_array, book_array_model), SUCCESS


@api.route('/autodescription/<isbn>')
class AutoDescription(Resource):
    @api.doc(description="Get book details using ISBN from google API or ISBN DB")
    @api.param('isbn', description="ISBN of the book - 10 0r 13 digits")
    @api.response(200, 'success', book_response_model)
    @api.response(401, 'unauthorized')
    @token_required
    def get(self, user, isbn):
        book = retrieve_book(isbn)
        return marshal(book, book_response_model), SUCCESS


@api.route('/<book_id>')
@api.param('book_id', 'book_id is required parameter if lookup books by id')
class BookActivities(Resource):
    @api.doc(description="updating the database and ebay with updated book data by the staff ")
    @api.response(200, 'success', model=book_response_model)
    @api.response(401, 'unauthorized')
    @token_required
    def put(self, user, book_id):
        data = request.form.to_dict()
        images = request.files
        book = update_book(data, images, book_id)
        return marshal(book, book_response_model), SUCCESS

    @api.doc(description="retrieve book by book id")
    @api.response(200, 'success', model=book_response_model)
    @api.response(401, 'unauthorized')
    @token_required
    def get(self, user, book_id):
        book = get_book(book_id)
        return marshal(book, book_response_model), SUCCESS

    @api.doc(description="delete some book by book id")
    @api.response(200, 'success', model=book_response_model)
    @api.response(401, 'unauthorized')
    @token_required
    def delete(self, user, book_id):
        book = unlist_book(book_id)
        return marshal(book, book_response_model), SUCCESS


@api.route('/list')
class BookList(Resource):
    @api.doc(description="List the book to ebay.")
    @api.response(200, 'success', model=book_response_model)
    @api.response(401, 'unauthorized')
    @token_required
    def post(self, user):
        data = request.form.to_dict()
        images = request.files
        book = create_book(data, images, user)
        return marshal(book, book_response_model), SUCCESS

# @api.route('/unlist/<book_id>')
# class BookUnlist(Resource):
#     @api.doc(description="unlist some books to ebay or unlist books from ebay.")
#     @api.response(200, 'success', model=book_model)
#     @api.response(401, 'unauthorized')
#     @api.param('book_id', description="take the book id as the parameter")
#     @token_required
#     def get(self, book_id):
#         book = unlist_book(book_id)
#         return marshal(book, book_model), GET_SUCCESS

# @api.route('/confirm')
# class BookConfirmation(Resource):
#     @api.doc(description="confirm book information from user")
#     @api.response(201, 'success', book_model)
#     @api.response(401, 'unauthorized')
#     def post(self):
#         # data = json.loads(request.get_data())
#         data = request.form
#         images = request.files
#         book = confirm_book(data, images)
#         return marshal(book, book_model), POST_SUCCESS
