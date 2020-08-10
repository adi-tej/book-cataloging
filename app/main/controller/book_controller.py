from flask import request
from flask_restplus import Resource, marshal
from app.main.service.book_service import *
from ..util.dto import BookDto
from ..util.decorator import token_required
from ..http_status import *

api = BookDto.api
isbn_model = BookDto.isbn_model
book_model = BookDto.book_model
book_array_model = BookDto.book_array_model


@api.route('')
class Books(Resource):
    @api.doc(description="get all books according to parameters'")
    @api.response(200, 'success', model=book_array_model)
    @api.response(401, 'unauthorized')
    @api.param('isbn', description="take isbn in the parameter if you have")
    @api.param('title', description="take title in the parameter if you have")
    @token_required
    def get(self):
        params = request.args
        token = request.headers.get('Authorization')
        book_list = get_book_by_params(params, token)
        book_array = {
            'books': book_list
        }
        return marshal(book_array, book_array_model), SUCCESS


@api.route('/autodescription/<isbn>')
class AutoDescription(Resource):
    @api.doc(description="book autodescription")
    @api.param('isbn', description="take isbn in the parameter if you have")
    @api.response(200, 'success', book_model)
    @api.response(401, 'unauthorized')
    @token_required
    def get(self, isbn):
        book = retrive_book(isbn)
        return marshal(book, book_model), SUCCESS


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

@api.route('/<book_id>')
@api.param('book_id', 'book_id is required parameter if lookup books by id')
class BookActivities(Resource):
    # this function is used to correct and update the information with the info returned by staff, you can add more images too.
    @api.doc(description="updating the database and ebay with updated book data by the staff ")
    @api.response(201, 'success', model=book_model)
    @api.response(401, 'unauthorized')
    @token_required
    def put(self, book_id):
        # data = json.load(request.get_data())
        data = request.form.to_dict()
        images = request.files
        book = update_book(data, images, book_id)
        return marshal(book, book_model), SUCCESS

    @api.doc(description="retrieve book by book id")
    @api.response(200, 'success', model=book_model)
    @api.response(401, 'unauthorized')
    @token_required
    def get(self, book_id):
        book = get_book(book_id)
        return marshal(book, book_model), SUCCESS

    @api.doc(description="delete some book by book id")
    @api.response(200, 'success', model=book_model)
    @api.response(401, 'unauthorized')
    @token_required
    def delete(self, book_id):
        book = unlist_book(book_id)
        return marshal(book, book_model), SUCCESS


@api.route('/list')
class BookList(Resource):
    @api.doc(description="list some books to ebay.")
    # @api.expect(book_model)
    @api.response(200, 'success', model=book_model)
    @api.response(401, 'unauthorized')
    @token_required
    def post(self):
        # data = json.loads(request.get_data())
        data = request.form.to_dict()
        images = request.files
        book = list_book(data, images)
        return marshal(book, book_model), SUCCESS

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
