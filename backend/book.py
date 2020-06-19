from flask import Blueprint
from flask_restplus import Api, Resource

from app import opshop_api
from http_status import *

books = Blueprint('book_api', __name__)

@books.route('/')
class Books(Resource):
    def get(self):
        return "all of the books"

# get barcode from frontend, search information of the book
# then store the information into our database, finally return
# the book information to frontend
@books.route('/creation/')
class BooksCreation(Resource):
    def post(self):
        pass

# After frontend receive the book information, the staff/manager
# can confirm the information or do some updation or giveup
@books.route('/updation/')
class BooksUpdation(Resource):
    def post(self):
        pass

# After user get the information, the user can list the books which
# the user want or list all of the books on opshop which are still
# not be listed to e-bay
@books.route('/books-listing/')
class BooksListing(Resource):
    def post(self):
        pass

# this function may be not used at this stage, if staff/manager
# want to remove the book from our database permanently then this
# can should be implemented
@books.route('/deletion/')
class Deletion(Resource):
    def post(self):
        pass