# Ammie: 2/06/2020 For Dev only
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask import request, jsonify, make_response
from auth import token_required

from models import *
from app import db, opshop_api
from flask import Blueprint

books = Blueprint('book_bp', __name__)

books_api = opshop_api.namespace(
    'books',
    description="books management process"
)

books_model = books_api.model('Book', {

})

@books.route('/')
class Books():
    @books_api.doc(description="receive book information from scanning")
    @books_api.expect(books_model)
    @token_required
    def post(self):
        pass

@books.route('/list/<int:book_id>')
class BookList():
    @books_api.doc(description="retrive some book by book id")
    @token_required
    def get(self, book_id):
        pass

    @books_api.doc(description="update some book by book id")
    @token_required
    def put(self, book_id):
        pass

    @books_api.doc(description="delete some book by book id")
    @token_required
    def delete(self, book_id):
        pass


@book_bp.route('/book/creation', methods = ['POST'])
def create():
    data = request.get_json()
    book_schema = BookSchema()
    product = book_schema.load(data)
    result = book_schema.dump(product.create())
    return make_response(jsonify({"book": result}),200)

@book_bp.route('/book/updation/<int:id>', methods = ['PUT'])
def update_book_by_id(id):
    data = request.get_json()
    get_book = Book.query.get(id)

    if data.get('opshop_id'):
        get_book.opshop_id = data['opshop_id']
    if data.get('item_type_id'):
        get_book.item_type_id = data['item_type_id']
    if data.get('title'):
        get_book.title = data['title']
    if data.get('author'):
        get_book.author = data['author']
    if data.get('publisher'):
        get_book.publisher = data['publisher']
    if data.get('publish_date'):
        get_book.publish_date = data['publish_date']
    if data.get('edition'):
        get_book.edition = data['edition']
    if data.get('pages_number'):
        get_book.pages_number= data['pages_number']
    if data.get('genre'):
        get_book.genre = data['genre']
    if data.get('cover'):
        get_book.cover = data['cover']
    if data.get('price'):
        get_book.price = data['price']
    if data.get('quantity'):
        get_book.quantity = data['quantity']
    if data.get('description'):
        get_book.description = data['description']
    if data.get('status'):
        get_book.status = data['status']
    if data.get('ISBN'):
        get_book.ISBN = data['ISBN']
    if data.get('ISBN_10'):
        get_book.ISBN_10 = data['ISBN_10']
    if data.get('ISBN_13'):
        get_book.ISBN_13 = data['ISBN_13']
    if data.get('condition'):
        get_book.condition = data['condition']
    if data.get('notes'):
        get_book.notes = data['notes']
    if data.get('update_date'):
        get_book.update_date = data['update_date']

    db.session.add(get_book)
    db.session.commit()

    book_schema = BookSchema(only=['book_id','opshop_id','item_type_id','title','author','publisher','publish_date','edition'\
        ,'pages_number','genre','cover','price','quantity','description','status','ISBN','ISBN_10','ISBN_13',\
                                   'condition','notes','update_date'])

    book = book_schema.dump(get_book)

    return make_response(jsonify({"book": book}))


@book_bp.route('/book/deletion/<int:id>', methods = ['DELETE'])
def delete_book_by_id(id):
    get_book = Book.query.get(id)
    db.session.delete(get_book)
    db.session.commit()
    return make_response("delete",200)