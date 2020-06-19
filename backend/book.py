from flask import Blueprint
from flask_restplus import Api, Resource

books = Blueprint('book_api', __name__)

bookapi = Api(books)

@bookapi.route('/')
class Books(Resource):
    def get(self):
        return "all of the books"

# get barcode from frontend, search information of the book
# then store the information into our database, finally return
# the book information to frontend
@bookapi.route('/creation/')
class BooksCreation(Resource):
    def post(self):
        pass

# After frontend receive the book information, the staff/manager
# can confirm the information or do some updation or giveup
@bookapi.route('/updation/')
class BooksUpdation(Resource):
    def post(self):
        pass

# After user get the information, the user can list the books which
# the user want or list all of the books on opshop which are still
# not be listed to e-bay
@bookapi.route('/books-listing/')
class BooksListing(Resource):
    def post(self):
        pass

# this function may be not used at this stage, if staff/manager
# want to remove the book from our database permanently then this
# can should be implemented
@bookapi.route('/deletion/')
class Deletion(Resource):
    def post(self):
        pass