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
    @api.response(200, 'success', model=book_response_model)
    @api.response(401, 'unauthorized')
    @token_required
    def put(self, user, book_id):
        # data = json.load(request.get_data())
        data = request.form.to_dict()
        images = request.files
        book = update_book(data, images, book_id)
        return marshal(book, book_model), SUCCESS

    @api.doc(description="retrieve book by book id")
    @api.response(200, 'success', model=book_model)
    @api.response(401, 'unauthorized')
    @token_required
    def get(self, user, book_id):
        book = get_book(book_id)
        return marshal(book, book_model), SUCCESS

    @api.doc(description="delete some book by book id")
    @api.response(200, 'success', model=book_model)
    @api.response(401, 'unauthorized')
    @token_required
    def delete(self, user, book_id):
        book = unlist_book(book_id)
        return marshal(book, book_model), SUCCESS


@api.route('/list')
class BookList(Resource):
    @api.doc(description="List the book to ebay.")
    # @api.expect(book_model)
    @api.response(200, 'success', model=book_model)
    @api.response(401, 'unauthorized')
    @token_required
    def post(self, user):
        # data = json.loads(request.get_data())
        # token = request.headers.get('Authorization')
        '''
        '[
            {
            "id":0,
            "uri":"https://circexunsw.s3-ap-southeast-2.amazonaws.com/1f20210b-dc88-11ea-a58a-7085c2fa4e67/cover.png"
            },{
            "id":1,
            "uri":"file:///var/mobile/Containers/Data/Application/C99902B1-00AB-4616-9CC9-2C6A100BDDC1/Library/Caches/ExponentExperienceData/%2540anonymous%252Fexpo-testing-95428dcd-a5f8-46a1-af65-b5a15af46c9f/ImagePicker/83776967-4381-4D18-AE33-D07AC776BE59.jpg"},{"id":2,"uri":"file:///var/mobile/Containers/Data/Application/C99902B1-00AB-4616-9CC9-2C6A100BDDC1/Library/Caches/ExponentExperienceData/%2540anonymous%252Fexpo-testing-95428dcd-a5f8-46a1-af65-b5a15af46c9f/ImagePicker/9CA18A32-44F5-4DA6-BE8C-3B4A4200D8A6.jpg"
            }
        ]'
        '''
        data = request.form.to_dict()
        images = request.files
        book = create_book(data, images, user)
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
