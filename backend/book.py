from flask import request, jsonify, make_response, Blueprint
from flask_restplus import fields, Resource
from uuid import uuid5, NAMESPACE_OID
from datetime import datetime
from ebaysdk.trading import Connection

from auth import token_required
from models import *
from app import db, opshop_api
from http_status import *

import json

# --> === Books part spec === <---
# For books, you have basic CRUD operations, not sure about how frontend handle 'cover'.
# condition_id is the conditionID comply with ebay, I will samepage this with frontend
# the status of book should be listed, unlisted. When you add new book to database, the
# default status is unlisted, only after listing to eBay it will be changed to listed

# For listing books to ebay
# Backend expect receive a list of book id from frontend, then the backend will make list
# request to ebay site, backend will return frontend the result of listing, if some books
# are listed failed there will be a failed list to frontend, otherwise, success!!

# For payment part
# At this satge I just input my own PayPal account to make sure everthing can work, in the
# future CircEx need to changed it to CirecEx Payment method

# -- Wei Song

books = Blueprint('book_bp', __name__)

books_api = opshop_api.namespace(
    'books',
    description="books management process"
)

books_list_api = opshop_api.namespace(
    'book list&unlist',
    description="book list to ebay and unlist from ebay management"
)

isbn_model=books_api.model('ISBN_10',{'ISBN':fields.Integer})

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
    'notes':fields.String,
    'condition_id':fields.Integer
})

# Backend expect list of book id from frontend
list_model = books_api.model('Book list',{
    'books':fields.List,
    'number':fields.Integer,
    'purpose':fields.String
})

def extract_data_google_api(ISBN,book): 
    API_KEY = "AIzaSyD6-khCY5wCvJbq0JYCIyw75gfxTtgHt_o"  # google api key
    google_url_book = "https://www.googleapis.com/books/v1/volumes?q=isbn:{}&key={}".format(ISBN,API_KEY)     #9781925483598
    response = requests.get(google_url_book)
    data = response.text

    parsed = json.loads(data)

    book_data={} # empty dictionary

    if parsed['totalItems']==0:
        print("item not found in google api ")
        return  ## what should we return when item not found?

    book_info=parsed['items'][0]


    book_data['title']=book_info['volumeInfo']['title']
    book_data['author']=book_info['volumeInfo']['authors'][0]
    book_data['genre']=book_info['volumeInfo']['categories'][0]
    book_data["publisher"]=book_info['volumeInfo']['publisher']
    book_data["publish_date"]=book_info['volumeInfo']['publishedDate']
    book_data["pages_number"]=book_info['volumeInfo']['pageCount']
    book_data["description"]=book_info['volumeInfo']['description']
    book_data['cover']=book_info['volumeInfo']['imageLinks']['thumbnail']
    book_data["ISBN_10"]=book_info['volumeInfo']['industryIdentifiers'][0]['identifier']
    book_data["ISBN_13"]=book_info['volumeInfo']["industryIdentifiers"][1]['identifier']

    book.__dict__=book_data

    return book # return book object



@books.route('/')
class Books(Resource):
    @books_api.doc(description="receive book information from scanning")
    #@books_api.expect(books_model)
    @books_api.expect(isbn_model)
    @token_required
    def post(self):
        data = json.load(request.get_data())
        book = Book()
        
        book_data=extract_data_google_api(data["ISBN"],book)
        book_data['book_id_local'] = book_id_local=uuid5(NAMESPACE_OID, 'v5app')
        book_data['book_id_ebay'] = ''
        book_data['item_type_id'] = 1
        book_data['create_date'] = datetime.now()
        book_data['update_date'] = datetime.now()
        book_data['status'] = 'unlisted'

        book.__dict__=book_data

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
            db.session.add(book)
            db.session.commit()
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
            db.session.remove(book)
            db.session.commit()
            resp.status_code = GET_SUCCESS
            resp.headers['message'] = 'book deletion success'
            return resp

@books.route('/list/')
class BookList(Resource):
    @books_list_api.doc(description="a list of books will be listed")
    @books_list_api.expect(list_model)
    @token_required
    def post(self):
        data = json.loads(request.get_data())
        fail_list, fail_unlist = [], []
        if data['books'] and data['purpose'] == "list":
            for book_id in data['books']:
                book = Book.query.filter_by(book_local_id=book_id).first()
                if not book:
                    fail_list.append(book_id)
                else:
                    # build connection with ebay
                    # make request body to ebay
                    # execute request to ebay and get response
                    ebay_conn = Connection(config_file="ebay.yaml", domain="api.sandbox.ebay.com", debug=True)
                    request_info = {
                        "Item": {
                            "Title":book.title,
                            "Country":"AU",
                            "Location":"Sydney",
                            "Site":"AU",
                            "ConditionID":book.condition_id,
                            "PaymentMethods":"PayPal",
                            "PayPalEmailAddress":"weisong301@gmail.com",
                            "Description":book.description,
                            "ListingDuration":"Days_30",
                            "ListingType":"FixedPriceItem",
                            "Currency":"AUD",
                            "ReturnPolicy": {
                                "ReturnsAcceptedOption": "ReturnsAccepted",
                                "RefundOption": "MoneyBack",
                                "ReturnsWithinOption": "Days_30",
                                "Description": "If you are not satisfied, please return.",
                                "ShippingCostPaidByOption": "Buyer"
                            },
                            "ShippingDetails": {
                                "ShippingServiceOptions": {
                                    "FreeShipping": "True",
                                    "ShippingService": "USPSMedia"
                                }
                            },
                            "DispatchTimeMax": "3"
                        },
                    }
                    response_ebay = ebay_conn.execute("AddItem", request_info)
                    # book list failed
                    if not response_ebay['Category2ID']:
                        fail_list.append(book_id)
                    else:
                        book.__dict__['status'] = 'listed'
                        book.__dict__['book_id_ebay'] = response_ebay['ItemID']
                        db.session.add(book)
                        db.session.commit()

            if fail_list:
                fail_dict = {'failed':fail_list, 'operation':'list'}
                resp = make_response(jsonify(fail_dict))
                resp.status_code = BAD_REQUEST
                resp.headers['message'] = 'some items list failed'
                return resp
            else:
                resp = make_response()
                resp.status_code = POST_SUCCESS
                resp.headers['message'] = 'all items list success'
                return resp
        elif data['books'] and data['purpose'] == "unlist":
            for book_id in data['books']:
                book = Book.query.filter_by(book_local_id=book_id).first()
                if not book:
                    fail_unlist.append(book_id)
                else:
                    ebay_conn = Connection(config_file="ebay.yaml", domain="api.sandbox.ebay.com", debug=True)
                    request_info = {
                        "EndingReason":"LostOrBroken",
                        "ItemID":book.book_id_ebay
                    }
                    response_ebay = ebay_conn.execute("EndItem", request_info)
            if fail_unlist:
                fail_dict = {'failed':fail_unlist, 'operation':'unlist'}
                resp = make_response(jsonify(fail_dict))
                resp.status_code = BAD_REQUEST
                resp.headers['message'] = 'some items unlist failed'
                return resp
            else:
                resp = make_response()
                resp.status_code = POST_SUCCESS
                resp.headers['message'] = 'all items unlist success'
                return resp
        else:
            resp = make_response()
            resp.status_code = BAD_REQUEST
            resp.headers['message'] = 'no book found'
            return resp
