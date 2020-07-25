from flask import request
from flask_restplus import Resource
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

@api.route('/')
class Books(Resource):
    @api.doc(description="get all the books")
    @api.response(200, 'get all books')
    @token_required
    def get(self):
        pass

    @api.doc(description="receive book information from scanning")
    @api.expect(isbn_model)
    @api.response(201, 'add book success', book_model)
    @token_required
    def post(self):
        data = json.loads(request.get_data())
        return retrive_book(data)

@api.route('/confirm/')
class BookConfirmation(Resource):
    def post(self):
        data = json.loads(request.get_data())
        return confirm_book(data)

@api.route('/<filter>/')
class RetriveBook(Resource):
    @api.doc(description="retrive book by title or ISBN, if nothing return all")
    @api.response(200, 'retrive book success')
    @api.response(404, 'not found')
    @api.header('isbn', description="take isbn in the header if you have")
    @api.header('title', description="take title in the header if you have")
    @token_required
    def get(self,filter):
        header_data = request.headers
        token = header_data['token']
        return get_book_by_params(header_data, token)

@api.route('/<string:book_id>/')
@api.param('book_id')
class BookActivities(Resource):
    # this function is used to correct and update the information with the info returned by staff, you can add more images too.
    @api.doc(description="updating the database and ebay with updated book data by the staff ")
    @api.response(201, 'add book success')
    @token_required
    def put(self, book_id):
        data = json.load(request.get_data())
        return update_book(data, book_id)

    @api.doc(description="retrive some book by book id")
    @api.response(201, 'retrive book information')
    @api.response(404, 'book not found')
    @token_required
    def get(self, book_id):
        return get_book(book_id)

    @api.doc(description="delete some book by book id")
    @token_required
    @api.response(201, 'book deletion success')
    @api.response(404, 'book not found')
    def delete(self, book_id):
        return delete_book(book_id)

@api.route('/list/')
class BookList(Resource):
    @api.doc(description="list some books to ebay or unlist books from ebay.")
    @api.expect(list_model)
    @api.response(201, 'all items list success')
    @api.response(400, 'some items list failed')
    @token_required
    def post(self):
        data = json.loads(request.get_data())
        return list_book(data)

@api.route('/unlist/')
class BookUnlist(Resource):
    @api.doc(description="unlist some books to ebay or unlist books from ebay.")
    @api.expect(unlist_model)
    @api.response(201, 'all items unlist success')
    @api.response(400, 'some items unlist failed')
    @token_required
    def post(self):
        data = json.loads(request.get_data())
        return unlist_book(data)
